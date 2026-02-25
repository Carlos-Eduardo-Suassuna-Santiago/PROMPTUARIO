from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Appointment

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient__user', 'doctor__user')
        user = self.request.user
        
        if user.is_doctor():
            # Médicos veem apenas seus próprios agendamentos
            queryset = queryset.filter(doctor=user.doctor_profile).order_by('scheduled_date', 'scheduled_time')
        elif user.is_patient():
            # Pacientes veem apenas seus próprios agendamentos
            queryset = queryset.filter(patient=user.patient_profile).order_by('scheduled_date', 'scheduled_time')
        elif user.is_attendant() or user.is_admin():
            # Atendentes e Admins veem todos os agendamentos
            queryset = queryset.order_by('scheduled_date', 'scheduled_time')
            
        return queryset

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'

from .forms import PatientAppointmentForm, AttendantAppointmentForm
from patients.models import Patient

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """View para criar um novo agendamento."""
    model = Appointment
    template_name = 'appointments/appointment_form.html'
    
    def get_form_class(self):
        user = self.request.user
        if user.is_patient():
            return PatientAppointmentForm
        elif user.is_attendant() or user.is_admin():
            return AttendantAppointmentForm
        # Médicos não agendam consultas para si mesmos, mas podem agendar para pacientes
        # Por simplicidade, vamos usar o formulário de atendente para médicos que queiram agendar
        elif user.is_doctor():
            return AttendantAppointmentForm
        return super().get_form_class()

    def get_success_url(self):
        return reverse_lazy('appointments:appointment_list')

    def form_valid(self, form):
        user = self.request.user
        
        if user.is_patient():
            # Paciente só pode agendar para si mesmo
            patient = get_object_or_404(Patient, user=user)
            form.save(patient=patient)
        elif user.is_attendant() or user.is_admin() or user.is_doctor():
            # Atendente, Admin e Médico escolhem o paciente no formulário
            form.save()
        
        messages.success(self.request, 'Consulta agendada com sucesso!')
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_patient():
            context['form_title'] = 'Agendar Minha Consulta'
        else:
            context['form_title'] = 'Agendar Consulta para Paciente'
        return context

class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.cancel(reason=request.POST.get('reason', ''), user=request.user):
            messages.success(request, 'Consulta cancelada com sucesso!')
        else:
            messages.error(request, 'Não é possível cancelar esta consulta.')
        return redirect('appointments:appointment_detail', pk=pk)


class AppointmentRescheduleView(LoginRequiredMixin, CreateView):
    """View para remarcar uma consulta."""
    model = Appointment
    template_name = 'appointments/appointment_reschedule.html'
    
    def get_form_class(self):
        user = self.request.user
        if user.is_patient():
            return PatientAppointmentForm
        elif user.is_attendant() or user.is_admin():
            return AttendantAppointmentForm
        elif user.is_doctor():
            return AttendantAppointmentForm
        return super().get_form_class()
    
    def get_object(self):
        """Retorna o agendamento original a ser remarcado."""
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        original_appointment = self.get_object()
        context['original_appointment'] = original_appointment
        context['form_title'] = 'Remarcar Consulta'
        
        user = self.request.user
        if user.is_patient():
            context['form_title'] = 'Remarcar Minha Consulta'
        else:
            context['form_title'] = f'Remarcar Consulta de {original_appointment.patient.user.get_full_name()}'
        
        return context
    
    def form_valid(self, form):
        """Cria novo agendamento e cancela o antigo."""
        original_appointment = self.get_object()
        user = self.request.user
        
        # Validar permissões
        if user.is_patient() and original_appointment.patient.user != user:
            messages.error(self.request, 'Você não tem permissão para remarcar esta consulta.')
            return self.form_invalid(form)
        
        # Salvar novo agendamento
        if user.is_patient():
            patient = get_object_or_404(Patient, user=user)
            new_appointment = form.save(commit=False)
            new_appointment.patient = patient
            new_appointment.doctor = original_appointment.doctor  # Manter mesmo médico
            new_appointment.save()
        else:
            new_appointment = form.save(commit=False)
            new_appointment.patient = original_appointment.patient  # Manter mesmo paciente
            # Médico será escolhido no formulário
            new_appointment.save()
        
        # Cancelar agendamento original
        original_appointment.cancel(reason='Consulta remarcada para: ' + 
                                   f"{new_appointment.scheduled_date.strftime('%d/%m/%Y')} às "
                                   f"{new_appointment.scheduled_time.strftime('%H:%M')}", 
                                   user=user)
        
        messages.success(self.request, f'Consulta remarcada com sucesso para {new_appointment.scheduled_date.strftime("%d/%m/%Y")} às {new_appointment.scheduled_time.strftime("%H:%M")}!')
        return redirect('appointments:appointment_detail', pk=new_appointment.pk)


class AppointmentCheckInView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_attendant() or self.request.user.is_admin()
    """View para realizar o check-in de uma consulta (apenas atendente/admin)."""
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        user = request.user
        

            
        if appointment.status == 'scheduled':
            appointment.status = 'checked_in'
            appointment.save()
            messages.success(request, f'Check-in do paciente {appointment.patient.user.get_full_name()} realizado com sucesso! Status atualizado para "Confirmada".')
        else:
            messages.error(request, f'Não é possível realizar o check-in. O status atual é "{appointment.get_status_display()}".')
            
        return redirect('accounts:dashboard')


class AppointmentCheckOutView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_attendant() or self.request.user.is_admin()
    """View para realizar o check-out de uma consulta (apenas atendente/admin)."""
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        user = request.user
        

            
        if appointment.status == 'checked_in':
            # O check-out indica que o paciente saiu, mas a consulta pode não ter sido concluída
            # pelo médico (prontuário). Vamos mudar para 'in_progress' para indicar que o médico
            # pode começar o atendimento, e o médico mudará para 'completed' ao criar o prontuário.
            # No entanto, para o fluxo do atendente, vamos assumir que o check-out é a saída.
            # O status 'completed' é definido na criação do prontuário.
            # Para o atendente, o check-out pode ser apenas para liberar a sala de espera.
            # Vamos manter o status como 'checked_in' e deixar o médico mudar para 'completed'.
            # Ou, se o médico não atendeu, o atendente pode marcar como 'no_show'.
            # Para simplificar o fluxo do atendente, vamos apenas redirecionar para o dashboard.
            messages.info(request, f'Check-out do paciente {appointment.patient.user.get_full_name()} registrado. O médico deve finalizar o prontuário.')
        else:
            messages.error(request, f'Não é possível realizar o check-out. O status atual é "{appointment.get_status_display()}".')
            
        return redirect('accounts:dashboard')

class AppointmentCalendarView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_calendar.html'
    context_object_name = 'appointments'
    paginate_by = 20 # Para o caso de não usar o calendário FullCalendar

    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient__user', 'doctor__user')
        user = self.request.user
        
        # Filtra agendamentos futuros
        queryset = queryset.filter(scheduled_date__gte=timezone.now().date()).order_by('scheduled_date', 'scheduled_time')
        
        if user.is_doctor():
            queryset = queryset.filter(doctor=user.doctor_profile)
        elif user.is_patient():
            queryset = queryset.filter(patient=user.patient_profile)
            
        return queryset


class AppointmentListJsonView(LoginRequiredMixin, View):
    """API JSON para listar agendamentos (para o calendário FullCalendar)."""
    def get(self, request):
        user = request.user
        queryset = Appointment.objects.select_related('patient__user', 'doctor__user')
        
        # Filtrar por permissões
        if user.is_doctor():
            queryset = queryset.filter(doctor=user.doctor_profile)
        elif user.is_patient():
            queryset = queryset.filter(patient=user.patient_profile)
        elif not (user.is_attendant() or user.is_admin()):
            # Usuários sem permissão não veem nada
            return JsonResponse([])
        
        # Ordenar por data e hora
        queryset = queryset.order_by('scheduled_date', 'scheduled_time')
        
        # Construir lista de eventos
        events = []
        for appointment in queryset:
            events.append({
                'id': appointment.id,
                'patient_name': appointment.patient.user.get_full_name(),
                'doctor_name': appointment.doctor.user.get_full_name(),
                'scheduled_date': appointment.scheduled_date.isoformat(),
                'scheduled_time': appointment.scheduled_time.strftime('%H:%M'),
                'status': appointment.status,
                'reason': appointment.reason or '',
            })
        
        return JsonResponse(events, safe=False)
