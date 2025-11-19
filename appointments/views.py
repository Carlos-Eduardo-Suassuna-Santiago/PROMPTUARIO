from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Appointment

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = "appointments/appointment_form.html"
    # o form deve permitir escolher doctor, scheduled_date, scheduled_time, reason
    fields = ["doctor", "reason", "scheduled_date", "scheduled_time"]
    success_url = reverse_lazy("appointments:appointment_list")

    def dispatch(self, request, *args, **kwargs):
        # opcional: apenas pacientes logados podem agendar por aqui
        if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
            messages.error(request, "Somente pacientes autenticados podem agendar consultas.")
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # atribui o patient automaticamente
        form.instance.patient = self.request.user.patient_profile
        return super().form_valid(form)

class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.cancel(reason=request.POST.get('reason', ''), user=request.user):
            messages.success(request, 'Consulta cancelada com sucesso!')
        else:
            messages.error(request, 'Não é possível cancelar esta consulta.')
        return redirect('appointments:appointment_detail', pk=pk)

class AppointmentCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'appointments/appointment_calendar.html'
