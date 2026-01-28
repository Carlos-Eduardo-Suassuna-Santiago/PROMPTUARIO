from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from accounts.utils import log_access
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
import json
from .models import Patient, Allergy, Vaccine, Medication
from .forms import AllergyForm, VaccineForm, MedicationForm


def parse_quill_delta(delta_json):
    """Converte Quill Delta JSON para texto legível."""
    if not delta_json:
        return "N/A"
    
    try:
        if isinstance(delta_json, str):
            data = json.loads(delta_json)
        else:
            data = delta_json
        
        text = ""
        if isinstance(data, dict) and 'ops' in data:
            for op in data.get('ops', []):
                if 'insert' in op:
                    text += op['insert']
        
        return text.strip() if text.strip() else "N/A"
    except (json.JSONDecodeError, TypeError, KeyError):
        return "N/A"

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
        medical_records = patient.medical_records.all().order_by('-created_at')
        
        # Processar cada prontuário para converter Quill Delta
        records_with_text = []
        for record in medical_records:
            records_with_text.append({
                'record': record,
                'chief_complaint_text': parse_quill_delta(record.chief_complaint),
                'diagnosis_text': parse_quill_delta(record.diagnosis),
            })
        
        context['medical_records'] = records_with_text
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


from django.views import View
from django.http import JsonResponse

from django.views import View
from django.http import JsonResponse

class PatientSearchJsonView(LoginRequiredMixin, View):
    """API JSON para busca dinâmica de pacientes."""
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        # Verificar permissões
        if not (request.user.is_doctor() or request.user.is_attendant() or request.user.is_admin()):
            return JsonResponse([], safe=False)
        
        if len(query) < 2:
            return JsonResponse([], safe=False)
        
        # Buscar pacientes
        patients = Patient.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__cpf__icontains=query) |
            Q(user__email__icontains=query)
        ).select_related('user').values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__cpf',
            'user__email'
        )[:10]  # Limitar a 10 resultados
        
        # Formatar resposta
        results = []
        for patient in patients:
            results.append({
                'id': patient['id'],
                'name': f"{patient['user__first_name']} {patient['user__last_name']}",
                'cpf': patient['user__cpf'] or '',
                'email': patient['user__email'] or '',
            })
        
        return JsonResponse(results, safe=False)


# ============== ALERGIAS ==============

class AllergyCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """View para criar nova alergia."""
    model = Allergy
    form_class = AllergyForm
    template_name = 'patients/allergy_form.html'
    
    def get_patient(self):
        """Obtém o paciente da URL."""
        return get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
    
    def test_func(self):
        """Apenas médicos, atendentes e o próprio paciente podem adicionar alergias."""
        patient = self.get_patient()
        user = self.request.user
        
        if user.is_patient():
            return patient.user == user
        return user.is_doctor() or user.is_attendant() or user.is_admin()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.get_patient()
        return context
    
    def form_valid(self, form):
        """Associa a alergia ao paciente."""
        form.instance.patient = self.get_patient()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patients:patient_detail', kwargs={'pk': self.kwargs['patient_pk']})


# ============== VACINAS ==============

class VaccineCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """View para criar nova vacina."""
    model = Vaccine
    form_class = VaccineForm
    template_name = 'patients/vaccine_form.html'
    
    def get_patient(self):
        """Obtém o paciente da URL."""
        return get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
    
    def test_func(self):
        """Apenas médicos, atendentes e o próprio paciente podem adicionar vacinas."""
        patient = self.get_patient()
        user = self.request.user
        
        if user.is_patient():
            return patient.user == user
        return user.is_doctor() or user.is_attendant() or user.is_admin()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.get_patient()
        return context
    
    def form_valid(self, form):
        """Associa a vacina ao paciente."""
        form.instance.patient = self.get_patient()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patients:patient_detail', kwargs={'pk': self.kwargs['patient_pk']})


# ============== MEDICAMENTOS ==============

class MedicationCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """View para criar novo medicamento."""
    model = Medication
    form_class = MedicationForm
    template_name = 'patients/medication_form.html'
    
    def get_patient(self):
        """Obtém o paciente da URL."""
        return get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
    
    def test_func(self):
        """Apenas médicos e atendentes podem adicionar medicamentos."""
        user = self.request.user
        return user.is_doctor() or user.is_attendant() or user.is_admin()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.get_patient()
        return context
    
    def form_valid(self, form):
        """Associa o medicamento ao paciente."""
        form.instance.patient = self.get_patient()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patients:patient_detail', kwargs={'pk': self.kwargs['patient_pk']})
