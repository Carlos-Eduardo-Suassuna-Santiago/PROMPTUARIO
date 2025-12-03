from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from accounts.utils import log_access
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from .models import Patient, Allergy, Vaccine, Medication

class PatientDetailView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        # Chama get_object() para garantir que o objeto está carregado e a permissão verificada
        patient = self.get_object()
        
        # Registra o acesso ao prontuário
        log_access(request, 'view_patient', f'Visualizou o paciente {patient.user.get_full_name()} (ID: {patient.pk})')
        
        return super().get(request, *args, **kwargs)
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_object(self, queryset=None):
        """
        Garante que o paciente só pode ver seu próprio prontuário,
        ou que médicos/atendentes podem ver qualquer prontuário.
        """
        user = self.request.user
        
        if user.is_patient():
            # Paciente só pode ver o próprio prontuário
            return get_object_or_404(Patient, user=user)
        
        # Médicos, Atendentes e Admins podem ver qualquer prontuário
        if user.is_doctor() or user.is_attendant() or user.is_admin():
            pk = self.kwargs.get(self.pk_url_kwarg)
            return get_object_or_404(Patient, pk=pk)
            
        raise Http404("Acesso negado.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object
        
        # Adicionar dados do prontuário
        context['medical_records'] = patient.medical_records.all().order_by('-created_at')
        context['allergies'] = patient.allergies.filter(is_active=True)
        context['vaccines'] = patient.vaccines.all().order_by('-application_date')
        context['medications'] = patient.medications.filter(is_active=True).order_by('-start_date')
        
        return context

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = 'patients/patient_form.html'
    fields = ['blood_type', 'height', 'weight', 'emergency_contact_name', 'emergency_contact_phone', 'medical_notes']
    success_url = reverse_lazy('patients:patient_list')

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patients/patient_form.html'
    fields = ['blood_type', 'height', 'weight', 'emergency_contact_name', 'emergency_contact_phone', 'medical_notes']
    success_url = reverse_lazy('patients:patient_list')

class AllergyListView(LoginRequiredMixin, ListView):
    model = Allergy
    template_name = 'patients/allergy_list.html'
    context_object_name = 'allergies'

class VaccineListView(LoginRequiredMixin, ListView):
    model = Vaccine
    template_name = 'patients/vaccine_list.html'
    context_object_name = 'vaccines'

class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'patients/medication_list.html'
    context_object_name = 'medications'


from django.contrib.auth.mixins import UserPassesTestMixin

class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lista de pacientes (acessível por médicos, atendentes e administradores)."""
    
    def test_func(self):
        user = self.request.user
        return user.is_doctor() or user.is_attendant() or user.is_admin()
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__cpf__icontains=query)
            )
        return queryset
