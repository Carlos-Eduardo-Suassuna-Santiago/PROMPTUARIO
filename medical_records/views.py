from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from accounts.utils import log_access
from datetime import datetime
import os
from django.conf import settings
from django.http import Http404
from django.views import View

from .models import MedicalRecord, Prescription, Exam
from .forms import MedicalRecordForm, PrescriptionForm, ExamForm
from .utils import generate_prescription_pdf
from accounts.models import DoctorProfile
from patients.models import Patient
from appointments.models import Appointment


class DoctorRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja um médico."""
    def test_func(self):
        return self.request.user.is_doctor()


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    """Visualização detalhada de um prontuário médico."""
    model = MedicalRecord
    template_name = 'medical_records/medical_record_detail.html'
    context_object_name = 'record'

    def get_object(self, queryset=None):
        record = super().get_object(queryset)
        user = self.request.user
        
        # Registrar log de acesso
        log_access(self.request, 'view_record', f'Visualizou o prontuário do paciente {record.patient.user.get_full_name()} (ID: {record.pk})')
        
        # Paciente só pode ver seu próprio prontuário
        if user.is_patient() and record.patient.user != user:
            raise Http404("Acesso negado.")
        
        # Médico só pode ver prontuários de seus pacientes ou que ele criou
        if user.is_doctor() and record.doctor.user != user.doctor_profile:
            # Poderia ser mais complexo, mas por enquanto, apenas o médico criador
            # ou o médico do paciente (se for o caso)
            # Para simplificar, vamos permitir que o médico veja todos os prontuários
            # de seus pacientes. A lógica de "seus pacientes" deve ser implementada
            # em outro lugar (ex: PatientDetailView)
            pass
        
        return record

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prescriptions'] = context['record'].prescriptions.all()
        context['exams'] = context['record'].exams.all()
        context['comments'] = context['record'].comments.all()
        return context


class MedicalRecordCreateUpdateMixin(DoctorRequiredMixin, LoginRequiredMixin):
    """Mixin para criação e atualização de prontuários."""
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/medical_record_form.html'

    def get_success_url(self):
        return reverse_lazy('medical_records:record_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        with transaction.atomic():
            # 1. Preencher campos obrigatórios
            appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
            patient = appointment.patient
            doctor = self.request.user.doctor_profile
            
            form.instance.appointment = appointment
            form.instance.patient = patient
            form.instance.doctor = doctor
            
            # 2. Salvar o prontuário
            is_new = form.instance.pk is None
            response = super().form_valid(form)
            
            # 2.5. Registrar log de acesso
            action_log = 'create_record' if is_new else 'update_record'
            log_access(self.request, action_log, f'Prontuário do paciente {patient.user.get_full_name()} (ID: {self.object.pk}) {action_log}d.')
            
            # 3. Criar histórico (Audit Trail)
            action = 'created' if is_new else 'updated'
            self.object.history.create(
                medical_record=self.object,
                user=self.request.user,
                action=action,
                description=f"Prontuário {action} pelo Dr(a). {doctor.user.get_full_name()}"
            )
            
            # 4. Marcar a consulta como concluída (ou em andamento, dependendo da regra)
            if is_new:
                appointment.status = 'completed'
                appointment.save()
            
            messages.success(self.request, f'Prontuário {action} com sucesso!')
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se for uma atualização, o objeto já está no contexto
        if self.object:
            appointment = self.object.appointment
        else:
            # Se for uma criação, buscamos a consulta pelo PK
            appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
            
        context['appointment'] = appointment
        context['patient'] = appointment.patient
        return context


class MedicalRecordCreateView(MedicalRecordCreateUpdateMixin, CreateView):
    """Criação de prontuário a partir de uma consulta."""
    def get_initial(self):
        initial = super().get_initial()
        appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
        initial['appointment'] = appointment
        initial['patient'] = appointment.patient
        initial['doctor'] = self.request.user.doctor_profile
        return initial
    
class MedicalRecordQuickCreateView(LoginRequiredMixin, DoctorRequiredMixin, View):
    """Criação rápida de prontuário sem vínculo obrigatório com consulta."""
    def get(self, request, patient_pk):
        patient = get_object_or_404(Patient, pk=patient_pk)
        doctor = request.user.doctor_profile

        # Verifica se já existe um prontuário
        existing = MedicalRecord.objects.filter(patient=patient).first()
        if existing:
            messages.warning(request, "O prontuário deste paciente já existe.")
            return redirect('medical_records:record_detail', pk=existing.pk)

        # Cria prontuário simples
        record = MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor
        )

        # Log opcional
        log_access(request, 'create_record', f'Criou prontuário rápido para {patient.user.get_full_name()}.')

        messages.success(request, "Prontuário criado com sucesso!")
        return redirect('medical_records:record_detail', pk=record.pk)

class MedicalRecordUpdateView(MedicalRecordCreateUpdateMixin, UpdateView):
    """Atualização de prontuário existente."""
    def get_object(self, queryset=None):
        # Garante que o prontuário pertence à consulta
        appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
        try:
            return MedicalRecord.objects.get(appointment=appointment)
        except MedicalRecord.DoesNotExist:
            raise Http404("Prontuário não encontrado para esta consulta.")
        
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MedicalRecord

class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/medical_record_list.html'
    context_object_name = 'records'



class PrescriptionCreateView(DoctorRequiredMixin, LoginRequiredMixin, CreateView):
    """Criação de Receita Médica."""
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'medical_records/prescription_form.html'

    def get_success_url(self):
        return reverse_lazy('medical_records:record_detail', kwargs={'pk': self.kwargs['record_pk']})

    def form_valid(self, form):
        medical_record = get_object_or_404(MedicalRecord, pk=self.kwargs['record_pk'])
        
        form.instance.medical_record = medical_record
        form.instance.patient = medical_record.patient
        form.instance.doctor = self.request.user.doctor_profile
        
        response = super().form_valid(form)
        messages.success(self.request, 'Receita criada com sucesso!')
        
        # Geração do PDF da receita
        prescription = form.instance
        file_name = f"receita_{prescription.pk}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        
        # Registrar log de acesso
        log_access(self.request, 'generate_pdf', f'Gerou PDF de Receita para o paciente {medical_record.patient.user.get_full_name()} (ID: {medical_record.pk}).')
        file_path = os.path.join(settings.MEDIA_ROOT, 'prescriptions', file_name)
        
        # Garante que o diretório MEDIA_ROOT/prescriptions exista
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'prescriptions'), exist_ok=True)
        
        generate_prescription_pdf(prescription, file_path)
        
        # Salva o caminho do arquivo no modelo
        prescription.prescription_file.name = os.path.join('prescriptions', file_name)
        prescription.save()
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_record'] = get_object_or_404(MedicalRecord, pk=self.kwargs['record_pk'])
        return context


class ExamCreateView(DoctorRequiredMixin, LoginRequiredMixin, CreateView):
    """Solicitação de Exame."""
    model = Exam
    form_class = ExamForm
    template_name = 'medical_records/exam_form.html'

    def get_success_url(self):
        return reverse_lazy('medical_records:record_detail', kwargs={'pk': self.kwargs['record_pk']})



    def form_valid(self, form):
        medical_record = get_object_or_404(MedicalRecord, pk=self.kwargs['record_pk'])
        
        form.instance.medical_record = medical_record
        form.instance.patient = medical_record.patient
        form.instance.doctor = self.request.user.doctor_profile
        
        response = super().form_valid(form)
        messages.success(self.request, 'Exame solicitado com sucesso!')
        
        # Registrar log de acesso
        log_access(self.request, 'generate_pdf', f'Solicitou Exame para o paciente {medical_record.patient.user.get_full_name()} (ID: {medical_record.pk}).')
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_record'] = get_object_or_404(MedicalRecord, pk=self.kwargs['record_pk'])
        return context
