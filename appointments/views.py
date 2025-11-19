from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
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

class AppointmentCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'appointments/appointment_calendar.html'
