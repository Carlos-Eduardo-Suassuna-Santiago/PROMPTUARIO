from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Patient, Allergy, Vaccine, Medication
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20


class PatientDetailView(LoginRequiredMixin, DetailView):
    """
    Exibe o prontuário completo do paciente:
    - informações pessoais
    - alergias
    - vacinas
    - medicamentos
    - observações médicas
    """
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        patient = self.get_object()

        # relacionamentos
        ctx['allergies'] = patient.allergies.all()
        ctx['vaccines'] = patient.vaccines.all()
        ctx['medications'] = patient.medications.filter(is_active=True)
        return ctx


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


# ====== Novo: Perfil do paciente (edição das informações do usuário logado) ======
class PatientProfileView(LoginRequiredMixin, UpdateView):
    """
    Permite ao usuário paciente editar suas informações (User model).
    Rota esperada: patients/profile/
    """
    model = User
    template_name = 'patients/patient_profile.html'
    # campos que o paciente pode alterar (ajuste conforme necessidade)
    fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('patients:patient_profile')

    def get_object(self):
        # retorna o usuário logado
        return self.request.user
