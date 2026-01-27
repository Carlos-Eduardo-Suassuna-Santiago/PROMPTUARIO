"""
Views for patient appointment booking process.
"""

from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import Appointment
from accounts.models import DoctorProfile
from patients.models import Patient


class PatientBookingDoctorListView(LoginRequiredMixin, ListView):
    """
    View for patients to select a doctor for booking an appointment.
    """
    model = DoctorProfile
    template_name = 'appointments/patient_booking_doctors.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        # Only show available doctors
        return DoctorProfile.objects.filter(is_available=True).select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Escolher Médico'
        return context


class PatientBookingAvailabilityView(LoginRequiredMixin, TemplateView):
    """
    View for patients to select available time slots for a specific doctor.
    """
    template_name = 'appointments/patient_booking_availability.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.kwargs['doctor_id']
        doctor = get_object_or_404(DoctorProfile, pk=doctor_id, is_available=True)

        # Generate available time slots for the next 30 days
        available_slots = self.get_available_slots(doctor)

        context.update({
            'doctor': doctor,
            'available_slots': available_slots,
            'title': f'Horários Disponíveis - Dr(a). {doctor.user.get_full_name()}'
        })
        return context

    def get_available_slots(self, doctor):
        """
        Generate available time slots for the doctor.
        This is a simplified version - in a real app, you'd have doctor schedules.
        """
        slots = []
        today = timezone.now().date()
        end_date = today + timedelta(days=30)

        # Assume working hours: 8:00 to 17:00, 30-minute slots
        working_hours = [
            (time(8, 0), time(12, 0)),  # Morning
            (time(13, 0), time(17, 0))  # Afternoon
        ]

        current_date = today + timedelta(days=1)  # Start from tomorrow

        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday
                for start_time, end_time in working_hours:
                    current_time = datetime.combine(current_date, start_time)
                    end_datetime = datetime.combine(current_date, end_time)

                    while current_time < end_datetime:
                        slot_time = current_time.time()
                        slot_datetime = datetime.combine(current_date, slot_time)

                        # Check if slot is available (no existing appointment)
                        if not Appointment.objects.filter(
                            doctor=doctor,
                            scheduled_date=current_date,
                            scheduled_time=slot_time,
                            status__in=['scheduled', 'confirmed']
                        ).exists():
                            slots.append({
                                'date': current_date,
                                'time': slot_time,
                                'datetime': slot_datetime,
                                'formatted_date': current_date.strftime('%d/%m/%Y'),
                                'formatted_time': slot_time.strftime('%H:%M')
                            })

                        current_time += timedelta(minutes=30)

            current_date += timedelta(days=1)

        return slots[:50]  # Limit to 50 slots


class PatientBookingConfirmView(LoginRequiredMixin, CreateView):
    """
    View for patients to confirm and create an appointment.
    """
    model = Appointment
    template_name = 'appointments/patient_booking_confirm.html'
    fields = ['reason']
    success_url = reverse_lazy('appointments:appointment_list')

    def get_doctor(self):
        return get_object_or_404(DoctorProfile, pk=self.kwargs['doctor_id'], is_available=True)

    def get_patient(self):
        return get_object_or_404(Patient, user=self.request.user)

    def get_slot_datetime(self):
        date_str = self.request.GET.get('date')
        time_str = self.request.GET.get('time')
        if not date_str or not time_str:
            return None

        try:
            slot_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            slot_time = datetime.strptime(time_str, '%H:%M').time()
            return slot_date, slot_time
        except ValueError:
            return None

    def get(self, request, *args, **kwargs):
        doctor = self.get_doctor()
        slot_info = self.get_slot_datetime()

        if not slot_info:
            messages.error(request, 'Informações do horário inválidas.')
            return redirect('appointments:patient_booking_doctors')

        slot_date, slot_time = slot_info

        # Verify slot is still available
        if Appointment.objects.filter(
            doctor=doctor,
            scheduled_date=slot_date,
            scheduled_time=slot_time,
            status__in=['scheduled', 'confirmed']
        ).exists():
            messages.error(request, 'Este horário não está mais disponível.')
            return redirect('appointments:patient_booking_availability', doctor_id=doctor.pk)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_doctor()
        patient = self.get_patient()
        slot_date, slot_time = self.get_slot_datetime()

        context.update({
            'doctor': doctor,
            'patient': patient,
            'slot_date': slot_date,
            'slot_time': slot_time,
            'formatted_date': slot_date.strftime('%d/%m/%Y'),
            'formatted_time': slot_time.strftime('%H:%M'),
            'title': 'Confirmar Agendamento'
        })
        return context

    def form_valid(self, form):
        doctor = self.get_doctor()
        patient = self.get_patient()
        slot_date, slot_time = self.get_slot_datetime()

        # Double-check availability
        if Appointment.objects.filter(
            doctor=doctor,
            scheduled_date=slot_date,
            scheduled_time=slot_time,
            status__in=['scheduled', 'confirmed']
        ).exists():
            messages.error(self.request, 'Este horário não está mais disponível.')
            return redirect('appointments:patient_booking_availability', doctor_id=doctor.pk)

        # Create appointment
        appointment = form.save(commit=False)
        appointment.patient = patient
        appointment.doctor = doctor
        appointment.scheduled_date = slot_date
        appointment.scheduled_time = slot_time
        appointment.appointment_type = 'first_visit'  # Default
        appointment.status = 'scheduled'
        appointment.save()

        messages.success(self.request, 'Consulta agendada com sucesso!')
        return redirect(self.success_url)