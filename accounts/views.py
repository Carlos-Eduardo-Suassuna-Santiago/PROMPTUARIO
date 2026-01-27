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
from django.db.models import Q
from .forms import DoctorProfileUpdateForm, AttendantProfileUpdateForm
from django.contrib import messages
from django.utils import timezone

from .models import User, DoctorProfile, AttendantProfile, DoctorSchedule, DoctorAbsence, AccessLog
from .forms import UserUpdateForm
from .forms import DoctorProfileUpdateForm, AttendantProfileUpdateForm, UserUpdateForm




class LoginView(BaseLoginView):
    """View de login customizada."""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal do sistema."""
    
    def get_template_names(self):
        user = self.request.user
        if user.is_admin():
            return ['accounts/dashboard_admin.html']
        elif user.is_doctor():
            return ['accounts/dashboard_doctor.html']
        elif user.is_attendant():
            return ['accounts/dashboard_attendant.html']
        elif user.is_patient():
            return ['accounts/dashboard_patient.html']
        return ['accounts/dashboard.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Dados específicos por tipo de usuário
        if user.is_doctor():
            from appointments.models import Appointment
            context['today_appointments'] = Appointment.objects.filter(
                doctor=user.doctor_profile,
                scheduled_date=timezone.now().date()
            ).select_related('patient__user')
        
        elif user.is_patient():
            from appointments.models import Appointment
            context['upcoming_appointments'] = Appointment.objects.filter(
                patient=user.patient_profile,
                scheduled_date__gte=timezone.now().date()
            ).select_related('doctor__user')[:5]
            
            # Adicionar link para agendamento
            context['appointment_create_url'] = reverse_lazy('appointments:appointment_create')
        
        elif user.is_attendant():
            from appointments.models import Appointment
            context['today_appointments'] = Appointment.objects.filter(
                scheduled_date=timezone.now().date()
            ).select_related('patient__user', 'doctor__user').order_by('scheduled_time')
            
            context['pending_appointments'] = Appointment.objects.filter(
                status='scheduled'
            ).select_related('patient__user', 'doctor__user')[:10]
            
        elif user.is_admin():
            from accounts.models import User
            from patients.models import Patient
            from accounts.models import DoctorProfile
            context['total_users'] = User.objects.count()
            context['total_doctors'] = DoctorProfile.objects.count()
            context['total_patients'] = Patient.objects.count()

            # ➕ ADICIONADO: TOTAL DE ADMINS E ATENDENTES
            context['total_admins'] = User.objects.filter(user_type='admin').count()
            context['total_attendants'] = User.objects.filter(user_type='attendant').count()
        
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
    paginate_by = 10
    
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


class AccessLogListView(AdminRequiredMixin, ListView):
    """Visualização de lista para Logs de Acesso (LGPD)."""
    model = AccessLog
    template_name = 'accounts/access_log_list.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')
        query = self.request.GET.get('q')
        action = self.request.GET.get('action')

        if query:
            queryset = queryset.filter(
                Q(user__username__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(details__icontains=query) |
                Q(ip_address__icontains=query)
            )
        
        if action:
            queryset = queryset.filter(action=action)
            
        return queryset


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_patient():
            context['patient_profile'] = user.patient_profile
        elif user.is_doctor():
            context['doctor_profile'] = user.doctor_profile
        elif user.is_attendant():
            context['attendant_profile'] = user.attendant_profile
            
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Atualização do perfil do usuário logado."""
    model = User
    template_name = 'accounts/profile_form.html'
    form_class = UserUpdateForm  # ✔ agora inclui foto

    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_patient():
            from patients.forms import PatientProfileUpdateForm
            context['patient_form'] = PatientProfileUpdateForm(instance=user.patient_profile)
        elif user.is_doctor():
            from .forms import DoctorProfileUpdateForm
            context['doctor_form'] = DoctorProfileUpdateForm(instance=user.doctor_profile)
        elif user.is_attendant():
            from .forms import AttendantProfileUpdateForm
            context['attendant_form'] = AttendantProfileUpdateForm(instance=user.attendant_profile)
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Processa tanto dados quanto arquivos (foto de perfil)."""
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            user = form.save()
            
            # Processar perfis extras
            if user.is_patient():
                from patients.forms import PatientProfileUpdateForm
                patient_form = PatientProfileUpdateForm(request.POST, instance=user.patient_profile)
                if patient_form.is_valid():
                    patient_form.save()
                else:
                    messages.error(request, 'Erro ao atualizar informações médicas.')
                    return self.render_to_response(self.get_context_data(form=form, patient_form=patient_form))
            
            elif user.is_doctor():
                doctor_form = DoctorProfileUpdateForm(request.POST, instance=user.doctor_profile)
                if doctor_form.is_valid():
                    doctor_form.save()
                else:
                    messages.error(request, 'Erro ao atualizar informações do médico.')
                    return self.render_to_response(self.get_context_data(form=form, doctor_form=doctor_form))
            
            elif user.is_attendant():
                attendant_form = AttendantProfileUpdateForm(request.POST, instance=user.attendant_profile)
                if attendant_form.is_valid():
                    attendant_form.save()
                else:
                    messages.error(request, 'Erro ao atualizar informações do atendente.')
                    return self.render_to_response(self.get_context_data(form=form, attendant_form=attendant_form))
            
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect(self.get_success_url())

        return self.form_invalid(form)

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
    
class PatientRegistrationAttendantView(CreateView):
    """View de registro público para pacientes."""
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/register_patient_attendant.html'
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
