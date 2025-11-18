from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Patient, Allergy, Vaccine, Medication

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'

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
