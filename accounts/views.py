"""
Views para o app accounts.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from .models import (
    User, DoctorProfile, AttendantProfile,
    DoctorSchedule, DoctorAbsence, AccessLog
)
from .forms import (
    UserUpdateForm,
    DoctorProfileUpdateForm,
    AttendantProfileUpdateForm,
    DoctorAbsenceForm,
    PatientRegistrationForm,
    DoctorRegistrationForm,
    AttendantRegistrationForm
)


# ================= AUTH =================

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


# ================= DASHBOARD =================

class DashboardView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        user = self.request.user
        if user.is_admin():
            return ['accounts/dashboard_admin.html']
        if user.is_doctor():
            return ['accounts/dashboard_doctor.html']
        if user.is_attendant():
            return ['accounts/dashboard_attendant.html']
        if user.is_patient():
            return ['accounts/dashboard_patient.html']
        return ['accounts/dashboard.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        from appointments.models import Appointment
        from patients.models import Patient

        if user.is_doctor():
            context['today_appointments'] = Appointment.objects.filter(
                doctor=user.doctor_profile,
                scheduled_date=timezone.now().date()
            ).select_related('patient__user')

        elif user.is_patient():
            context['upcoming_appointments'] = Appointment.objects.filter(
                patient=user.patient_profile,
                scheduled_date__gte=timezone.now().date()
            ).select_related('doctor__user')[:5]
            context['appointment_create_url'] = reverse_lazy(
                'appointments:appointment_create'
            )

        elif user.is_attendant():
            context['today_appointments'] = Appointment.objects.filter(
                scheduled_date=timezone.now().date()
            ).select_related(
                'patient__user', 'doctor__user'
            ).order_by('scheduled_time')

            context['pending_appointments'] = Appointment.objects.filter(
                status='scheduled'
            ).select_related(
                'patient__user', 'doctor__user'
            )[:10]

        elif user.is_admin():
            context['total_users'] = User.objects.count()
            context['total_doctors'] = DoctorProfile.objects.count()
            context['total_patients'] = Patient.objects.count()
            context['total_admins'] = User.objects.filter(user_type='admin').count()
            context['total_attendants'] = User.objects.filter(user_type='attendant').count()

        return context


# ================= MIXINS =================

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin()


# ================= USERS =================

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        user_type = self.request.GET.get('type')
        if user_type:
            qs = qs.filter(user_type=user_type)
        return qs


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = [
        'username', 'email', 'first_name', 'last_name', 'user_type',
        'cpf', 'phone', 'birth_date', 'address', 'city', 'state', 'zip_code'
    ]
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_form.html'
    fields = [
        'email', 'first_name', 'last_name', 'phone', 'birth_date',
        'address', 'city', 'state', 'zip_code', 'is_active'
    ]
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


# ================= LOGS =================

class AccessLogListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AccessLog
    template_name = 'accounts/access_log_list.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('user')
        q = self.request.GET.get('q')
        action = self.request.GET.get('action')

        if q:
            qs = qs.filter(
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(details__icontains=q) |
                Q(ip_address__icontains=q)
            )

        if action:
            qs = qs.filter(action=action)

        return qs


# ================= DOCTORS =================

class DoctorListView(LoginRequiredMixin, ListView):
    model = DoctorProfile
    template_name = 'accounts/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 20


class DoctorScheduleView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'accounts/doctor_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(DoctorProfile, pk=kwargs['pk'])
        context['doctor'] = doctor
        context['schedules'] = doctor.schedules.all()
        context['absences'] = doctor.absences.filter(
            end_datetime__gte=timezone.now()
        ).order_by('start_datetime')
        return context


class DoctorAbsenceCreateView(LoginRequiredMixin, CreateView):
    model = DoctorAbsence
    form_class = DoctorAbsenceForm
    template_name = 'accounts/doctor_absence_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(DoctorProfile, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.doctor = get_object_or_404(
            DoctorProfile, pk=self.kwargs['pk']
        )
        messages.success(self.request, 'Ausência cadastrada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'accounts:doctor_schedule',
            kwargs={'pk': self.kwargs['pk']}
        )


# ================= PROFILE =================

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_obj'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile_form.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            user = form.save()

            if user.is_patient():
                from patients.forms import PatientProfileUpdateForm
                patient_form = PatientProfileUpdateForm(
                    request.POST, instance=user.patient_profile
                )
                if patient_form.is_valid():
                    patient_form.save()
                else:
                    messages.error(request, 'Erro ao atualizar perfil de paciente.')
                    return self.form_invalid(form)

            elif user.is_doctor():
                doctor_form = DoctorProfileUpdateForm(
                    request.POST, instance=user.doctor_profile
                )
                if doctor_form.is_valid():
                    doctor_form.save()
                else:
                    messages.error(request, f'Erro ao atualizar perfil de médico: {doctor_form.errors}')
                    return self.form_invalid(form)

            elif user.is_attendant():
                attendant_form = AttendantProfileUpdateForm(
                    request.POST, instance=user.attendant_profile
                )
                if attendant_form.is_valid():
                    attendant_form.save()
                else:
                    messages.error(request, 'Erro ao atualizar perfil de atendente.')
                    return self.form_invalid(form)

            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect(self.success_url)

        return self.form_invalid(form)


# ================= REGISTRATION =================

class PatientRegistrationView(CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/register_patient.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Cadastro realizado com sucesso! Faça login para acessar o sistema.'
        )
        return super().form_valid(form)


class PatientRegistrationAttendantView(CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/register_patient_attendant.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Cadastro realizado com sucesso! Faça login para acessar o sistema.'
        )
        return super().form_valid(form)


class DoctorRegistrationView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'accounts/register_doctor.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Médico cadastrado com sucesso!')
        return super().form_valid(form)


class AttendantRegistrationView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = AttendantRegistrationForm
    template_name = 'accounts/register_attendant.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Atendente cadastrado com sucesso!')
        return super().form_valid(form)


class RegistrationChoiceView(TemplateView):
    template_name = 'accounts/register_choice.html'
# ================= END OF FILE =================