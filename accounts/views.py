"""
Views para o app accounts.
"""

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse

from .models import User, DoctorProfile, AttendantProfile, DoctorSchedule, DoctorAbsence
from patients.models import Patient
from appointments.models import Appointment

# ==========================================================
# LOGIN
# ==========================================================

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')

# ==========================================================
# DASHBOARD
# ==========================================================

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_doctor():
            context['today_appointments'] = Appointment.objects.filter(
                doctor__user=user,
                scheduled_date=timezone.now().date()
            ).select_related('patient__user')
        
        elif user.is_patient():
            context['upcoming_appointments'] = Appointment.objects.filter(
                patient__user=user,
                scheduled_date__gte=timezone.now().date()
            )[:5]
        
        elif user.is_attendant():
            context['pending_appointments'] = Appointment.objects.filter(
                status='scheduled'
            )[:10]
        
        return context

# ==========================================================
# MIXINS
# ==========================================================

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin()

# ==========================================================
# CRUD DE USUÁRIOS (ADMIN)
# ==========================================================

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    paginate_by = 20
    context_object_name = 'users'

    def get_queryset(self):
        qs = super().get_queryset()
        t = self.request.GET.get('type')
        return qs.filter(user_type=t) if t else qs


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 
              'cpf', 'phone', 'birth_date', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = ['email', 'first_name', 'last_name', 'phone', 'birth_date', 
              'address', 'city', 'state', 'zip_code', 'is_active']
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuário excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# ==========================================================
# MÉDICOS – LISTAGEM / HORÁRIOS / AUSÊNCIAS
# ==========================================================

class DoctorListView(LoginRequiredMixin, ListView):
    model = DoctorProfile
    template_name = 'accounts/doctor_list.html'
    context_object_name = 'doctors'


class DoctorScheduleView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'accounts/doctor_schedule.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        doctor = get_object_or_404(DoctorProfile, pk=kwargs['pk'])
        ctx['doctor'] = doctor
        ctx['schedules'] = doctor.schedules.all()
        return ctx


class DoctorAbsenceCreateView(LoginRequiredMixin, CreateView):
    model = DoctorAbsence
    template_name = 'accounts/doctor_absence_form.html'
    fields = ['start_datetime', 'end_datetime', 'reason', 'is_full_day']
    
    def form_valid(self, form):
        doctor = get_object_or_404(DoctorProfile, pk=self.kwargs['pk'])
        form.instance.doctor = doctor
        messages.success(self.request, 'Ausência cadastrada com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('accounts:doctor_schedule', kwargs={'pk': self.kwargs['pk']})

# ==========================================================
# PERFIL DO USUÁRIO
# ==========================================================

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_obj'
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile_update.html'
    fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)

# ==========================================================
# REGISTRO (PACIENTE / MÉDICO / ATENDENTE)
# ==========================================================

from .forms import (
    PatientRegistrationForm,
    DoctorRegistrationForm,
    AttendantRegistrationForm
)
class PatientRegistrationView(CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/register_patient.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        msg = 'Cadastro realizado com sucesso! Faça login.'
        messages.success(self.request, msg)
        return super().form_valid(form)


class DoctorRegistrationView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'accounts/register_doctor.html'
    success_url = reverse_lazy('accounts:user_list')


class AttendantRegistrationView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = AttendantRegistrationForm
    template_name = 'accounts/register_attendant.html'
    success_url = reverse_lazy('accounts:user_list')


class RegistrationChoiceView(TemplateView):
    template_name = 'accounts/register_choice.html'

# ==========================================================
# FUNCIONALIDADES DO MÉDICO
# ==========================================================

# 1 — Agenda do dia
class DoctorAgendaView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/doctor_agenda.html"

    def dispatch(self, req, *a, **kw):
        if not req.user.is_doctor():
            return redirect('accounts:dashboard')
        return super().dispatch(req, *a, **kw)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        today = timezone.now().date()
        ctx["today"] = today
        ctx["appointments"] = Appointment.objects.filter(
            doctor=self.request.user.doctor_profile,
            scheduled_date=today,
            status="scheduled"
        ).select_related("patient__user")
        return ctx

# 2 — Listar prontuários
class DoctorMedicalRecordsView(LoginRequiredMixin, ListView):
    template_name = "accounts/doctor_records.html"
    model = Patient
    context_object_name = "patients"

    def dispatch(self, req, *a, **kw):
        if not req.user.is_doctor():
            return redirect('accounts:dashboard')
        return super().dispatch(req, *a, **kw)

# 2.1 — Detalhar prontuário
class DoctorRecordDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/doctor_record_detail.html"
    model = Patient
    context_object_name = "patient"

    def dispatch(self, req, *a, **kw):
        if not req.user.is_doctor():
            return redirect("accounts:dashboard")
        return super().dispatch(req, *a, **kw)

# 3 — Buscar prontuário por nome
class DoctorMedicalRecordSearchView(LoginRequiredMixin, ListView):
    template_name = "accounts/doctor_record_search.html"
    context_object_name = "patients"
    model = Patient

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        return Patient.objects.filter(user__first_name__icontains=q)

# 4 — Listar pacientes
class DoctorPatientListView(LoginRequiredMixin, ListView):
    template_name = "accounts/doctor_patient_list.html"
    model = Patient
    context_object_name = "patients"

# 4.1 — Detalhes do paciente
class DoctorPatientDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/doctor_patient_detail.html"
    model = Patient
    context_object_name = "patient"

# 5 — Listar consultas
class DoctorAppointmentListView(LoginRequiredMixin, ListView):
    template_name = "accounts/doctor_appointments.html"
    context_object_name = "appointments"
    model = Appointment

    def get_queryset(self):
        return Appointment.objects.filter(
            doctor=self.request.user.doctor_profile
        )

# 5.1 — Criar consulta
class DoctorAppointmentCreateView(LoginRequiredMixin, CreateView):
    template_name = "accounts/doctor_appointment_form.html"
    model = Appointment
    fields = ["patient", "reason", "scheduled_date", "scheduled_time"]
    success_url = reverse_lazy("accounts:doctor_appointments")

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor_profile
        return super().form_valid(form)

# 6 — Gerar relatórios
class DoctorReportView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/doctor_reports.html"

def generate_doctor_report(request):
    if not request.user.is_doctor():
        return redirect('accounts:dashboard')

    appointments = Appointment.objects.filter(
        doctor=request.user.doctor_profile
    )

    from reportlab.pdfgen import canvas
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=relatorio.pdf"

    pdf = canvas.Canvas(response)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 820, f"Relatório de Consultas - Dr(a). {request.user.get_full_name()}")

    y = 780
    for a in appointments:
        pdf.drawString(50, y, f"{a.scheduled_date} - {a.patient.user.get_full_name()}")
        y -= 20
        if y < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 800

    pdf.save()
    return response
