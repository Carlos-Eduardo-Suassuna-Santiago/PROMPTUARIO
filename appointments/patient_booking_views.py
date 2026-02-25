"""
Views para agendamento de consultas pelo paciente.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, time
from accounts.models import DoctorProfile, DoctorSchedule, DoctorAbsence
from patients.models import Patient
from .models import Appointment


class PatientRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja um paciente."""
    def test_func(self):
        return self.request.user.is_patient()


class PatientBookingDoctorListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    """
    Lista de médicos disponíveis para agendamento pelo paciente.
    """
    model = DoctorProfile
    template_name = 'appointments/patient_booking_doctor_list.html'
    context_object_name = 'doctors'
    
    def get_queryset(self):
        queryset = DoctorProfile.objects.filter(
            user__is_active=True,
            is_available=True
        ).select_related('user').order_by('specialty', 'user__first_name')
        
        # Filtro por especialidade (opcional)
        specialty = self.request.GET.get('specialty')
        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de especialidades únicas para filtro
        context['specialties'] = DoctorProfile.objects.values_list('specialty', flat=True).distinct().order_by('specialty')
        context['selected_specialty'] = self.request.GET.get('specialty', '')
        return context


class PatientBookingAvailabilityView(LoginRequiredMixin, PatientRequiredMixin, TemplateView):
    """
    Exibe os horários disponíveis de um médico específico.
    """
    template_name = 'appointments/patient_booking_availability.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.kwargs.get('doctor_id')
        doctor = get_object_or_404(DoctorProfile, pk=doctor_id, is_available=True)
        
        context['doctor'] = doctor
        
        # Gerar próximos 14 dias de disponibilidade
        today = timezone.now().date()
        available_slots = []
        
        for day_offset in range(1, 15):  # Próximos 14 dias (começando amanhã)
            date = today + timedelta(days=day_offset)
            weekday = date.weekday()  # 0=Monday, 6=Sunday
            
            # Verificar se o médico trabalha neste dia da semana
            schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                weekday=weekday,
                is_active=True
            )
            
            if not schedules.exists():
                continue
            
            # Verificar se o médico tem ausência neste dia
            has_absence = DoctorAbsence.objects.filter(
                doctor=doctor,
                start_datetime__date__lte=date,
                end_datetime__date__gte=date
            ).exists()
            
            if has_absence:
                continue
            
            # Gerar slots de horário (intervalos de 30 minutos)
            for schedule in schedules:
                current_time = datetime.combine(date, schedule.start_time)
                end_time = datetime.combine(date, schedule.end_time)
                
                day_slots = []
                while current_time < end_time:
                    slot_time = current_time.time()
                    
                    # Verificar se já existe agendamento neste horário
                    is_booked = Appointment.objects.filter(
                        doctor=doctor,
                        scheduled_date=date,
                        scheduled_time=slot_time,
                        status__in=['scheduled', 'confirmed', 'in_progress']
                    ).exists()
                    
                    if not is_booked:
                        day_slots.append({
                            'time': slot_time,
                            'datetime': current_time,
                            'available': True
                        })
                    
                    current_time += timedelta(minutes=30)
                
                if day_slots:
                    available_slots.append({
                        'date': date,
                        'weekday_name': date.strftime('%A'),
                        'slots': day_slots
                    })
        
        context['available_slots'] = available_slots
        return context


class PatientBookingConfirmView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    """
    Confirmação e criação do agendamento pelo paciente.
    """
    model = Appointment
    template_name = 'appointments/patient_booking_confirm.html'
    fields = ['reason']
    success_url = reverse_lazy('appointments:appointment_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.kwargs.get('doctor_id')
        date_str = self.request.GET.get('date')
        time_str = self.request.GET.get('time')
        
        context['doctor'] = get_object_or_404(DoctorProfile, pk=doctor_id)
        context['selected_date'] = datetime.strptime(date_str, '%Y-%m-%d').date()
        context['selected_time'] = datetime.strptime(time_str, '%H:%M:%S').time()
        
        return context
    
    def form_valid(self, form):
        doctor_id = self.kwargs.get('doctor_id')
        date_str = self.request.GET.get('date')
        time_str = self.request.GET.get('time')
        
        doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
        scheduled_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        scheduled_time = datetime.strptime(time_str, '%H:%M:%S').time()
        
        # Verificar novamente se o horário ainda está disponível
        is_booked = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            status__in=['scheduled', 'confirmed', 'in_progress']
        ).exists()
        
        if is_booked:
            messages.error(self.request, 'Este horário acabou de ser reservado. Por favor, escolha outro horário.')
            return redirect('appointments:patient_booking_availability', doctor_id=doctor_id)
        
        # Criar o agendamento
        patient = get_object_or_404(Patient, user=self.request.user)
        
        appointment = form.save(commit=False)
        appointment.patient = patient
        appointment.doctor = doctor
        appointment.scheduled_date = scheduled_date
        appointment.scheduled_time = scheduled_time
        appointment.status = 'scheduled'
        appointment.appointment_type = 'first_visit'
        appointment.created_by = self.request.user
        appointment.save()
        
        messages.success(
            self.request, 
            f'Consulta agendada com sucesso para {scheduled_date.strftime("%d/%m/%Y")} às {scheduled_time.strftime("%H:%M")} com Dr(a). {doctor.user.get_full_name()}!'
        )
        
        return redirect(self.success_url)
