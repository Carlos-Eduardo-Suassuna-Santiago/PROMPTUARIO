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

from .models import User, DoctorProfile, AttendantProfile, DoctorSchedule, DoctorAbsence


class LoginView(BaseLoginView):
    """View de login customizada."""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal do sistema."""
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Dados específicos por tipo de usuário
        if user.is_doctor():
            from appointments.models import Appointment
            context['today_appointments'] = Appointment.objects.filter(
                doctor__user=user,
                scheduled_date=timezone.now().date()
            ).select_related('patient__user')
        
        elif user.is_patient():
            from appointments.models import Appointment
            context['upcoming_appointments'] = Appointment.objects.filter(
                patient__user=user,
                scheduled_date__gte=timezone.now().date()
            ).select_related('doctor__user')[:5]
        
        elif user.is_attendant():
            from appointments.models import Appointment
            context['pending_appointments'] = Appointment.objects.filter(
                status='scheduled'
            ).select_related('patient__user', 'doctor__user')[:10]
        
        return context


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja administrador."""
    
    def test_func(self):
        return self.request.user.is_admin()


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Lista de usuários (apenas admin)."""
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.GET.get('type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """Detalhes de um usuário."""
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Criação de novo usuário."""
    model = User
    template_name = 'accounts/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 
              'cpf', 'phone', 'birth_date', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Atualização de usuário."""
    model = User
    template_name = 'accounts/user_form.html'
    fields = ['email', 'first_name', 'last_name', 'phone', 'birth_date', 
              'address', 'city', 'state', 'zip_code', 'is_active']
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Exclusão de usuário."""
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuário excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class DoctorListView(LoginRequiredMixin, ListView):
    """Lista de médicos."""
    model = DoctorProfile
    template_name = 'accounts/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 20


class DoctorScheduleView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """Gerenciamento de horários do médico."""
    template_name = 'accounts/doctor_schedule.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(DoctorProfile, pk=kwargs['pk'])
        context['doctor'] = doctor
        context['schedules'] = doctor.schedules.all()
        return context


class DoctorAbsenceCreateView(LoginRequiredMixin, CreateView):
    """Cadastro de ausência de médico."""
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


class ProfileView(LoginRequiredMixin, DetailView):
    """Visualização do perfil do usuário logado."""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_obj'
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Atualização do perfil do usuário logado."""
    model = User
    template_name = 'accounts/profile_form.html'
    fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


# ========== VIEWS DE REGISTRO ==========

from .forms import (
    PatientRegistrationForm,
    DoctorRegistrationForm,
    AttendantRegistrationForm
)


class PatientRegistrationView(CreateView):
    """View de registro público para pacientes."""
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/register_patient.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Cadastro realizado com sucesso! Faça login para acessar o sistema.'
        )
        return response


class DoctorRegistrationView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """View de registro de médicos (apenas admin)."""
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'accounts/register_doctor.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Médico cadastrado com sucesso!')
        return response


class AttendantRegistrationView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """View de registro de atendentes (apenas admin)."""
    model = User
    form_class = AttendantRegistrationForm
    template_name = 'accounts/register_attendant.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Atendente cadastrado com sucesso!')
        return response


class RegistrationChoiceView(TemplateView):
    """View para escolher o tipo de cadastro (apenas admin)."""
    template_name = 'accounts/register_choice.html'
