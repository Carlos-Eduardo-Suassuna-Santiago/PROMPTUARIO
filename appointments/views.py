from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Appointment
from .forms import PatientAppointmentForm, AttendantAppointmentForm
from patients.models import Patient

# --- Views de Gerenciamento de Consultas ---

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient__user', 'doctor__user')
        user = self.request.user
        if user.is_doctor():
            queryset = queryset.filter(doctor=user.doctor_profile).order_by('scheduled_date', 'scheduled_time')
        elif user.is_patient():
            queryset = queryset.filter(patient=user.patient_profile).order_by('scheduled_date', 'scheduled_time')
        else:
            queryset = queryset.order_by('scheduled_date', 'scheduled_time')
        return queryset

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'appointments/appointment_form.html'
    
    def get_form_class(self):
        user = self.request.user
        return PatientAppointmentForm if user.is_patient() else AttendantAppointmentForm

    def form_valid(self, form):
        user = self.request.user
        if user.is_patient():
            patient = get_object_or_404(Patient, user=user)
            form.save(patient=patient)
        else:
            form.save()
        messages.success(self.request, 'Consulta agendada com sucesso!')
        return redirect('appointments:appointment_list')

class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.cancel(reason=request.POST.get('reason', ''), user=request.user):
            messages.success(request, 'Consulta cancelada com sucesso!')
        else:
            messages.error(request, 'Erro ao cancelar consulta.')
        return redirect('appointments:appointment_detail', pk=pk)

class AppointmentRescheduleView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'appointments/appointment_reschedule.html'
    
    def get_form_class(self):
        user = self.request.user
        return PatientAppointmentForm if user.is_patient() else AttendantAppointmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['original_appointment'] = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        return context

# --- Views de Operação (Check-in/Out) ---

class AppointmentCheckInView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = 'checked_in'
        appointment.save()
        messages.success(request, 'Check-in realizado!')
        return redirect('appointments:appointment_list')

class AppointmentCheckOutView(LoginRequiredMixin, View):
    def post(self, request, pk):
        messages.info(request, 'Check-out registrado.')
        return redirect('appointments:appointment_list')

# --- Calendário e API ---

class AppointmentCalendarView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_calendar.html'

class AppointmentListJsonView(LoginRequiredMixin, View):
    def get(self, request):
        return JsonResponse([], safe=False)

# --- Sistema de Booking (Agendamento Direto) ---

class PatientBookingDoctorListView(LoginRequiredMixin, ListView):
    template_name = 'appointments/patient_booking_doctors.html'
    context_object_name = 'doctors'
    def get_queryset(self):
        from accounts.models import Doctor
        return Doctor.objects.filter(user__is_active=True)

class PatientBookingAvailabilityView(LoginRequiredMixin, TemplateView):
    template_name = 'appointments/patient_booking_availability.html'

class PatientBookingConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'appointments/patient_booking_confirm.html'