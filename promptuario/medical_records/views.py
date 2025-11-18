from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import MedicalRecord

class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/medical_record_list.html'
    context_object_name = 'medical_records'
    paginate_by = 20

class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/medical_record_detail.html'

class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    template_name = 'medical_records/medical_record_form.html'
    fields = ['chief_complaint', 'symptoms', 'physical_examination', 'diagnosis', 'treatment_plan', 'observations']
    
    def form_valid(self, form):
        from appointments.models import Appointment
        appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
        form.instance.appointment = appointment
        form.instance.patient = appointment.patient
        form.instance.doctor = appointment.doctor
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('medical_records:medical_record_detail', kwargs={'pk': self.object.pk})

class MedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    template_name = 'medical_records/medical_record_form.html'
    fields = ['chief_complaint', 'symptoms', 'physical_examination', 'diagnosis', 'treatment_plan', 'observations']
    
    def get_success_url(self):
        return reverse_lazy('medical_records:medical_record_detail', kwargs={'pk': self.object.pk})

class MedicalRecordCloseView(LoginRequiredMixin, View):
    def post(self, request, pk):
        medical_record = get_object_or_404(MedicalRecord, pk=pk)
        medical_record.close_record()
        messages.success(request, 'Prontuário fechado com sucesso!')
        return redirect('medical_records:medical_record_detail', pk=pk)
