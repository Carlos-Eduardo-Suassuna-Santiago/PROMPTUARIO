from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from appointments.models import Appointment
from medical_records.models import MedicalRecord
# from .models import Report # Assumindo que Report não é necessário para o relatório do médico


class DoctorRequiredMixin(UserPassesTestMixin):
    """Mixin que requer que o usuário seja um médico."""
    def test_func(self):
        return self.request.user.is_doctor()


class DoctorReportView(LoginRequiredMixin, DoctorRequiredMixin, TemplateView):
    """
    Relatório de atividades do médico.
    """
    template_name = 'reports/doctor_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_profile = self.request.user.doctor_profile
        
        # 1. Dados de Agendamentos
        appointments = Appointment.objects.filter(doctor=doctor_profile)
        
        context['total_appointments'] = appointments.count()
        context['completed_appointments'] = appointments.filter(status='completed').count()
        context['cancelled_appointments'] = appointments.filter(status='cancelled').count()
        
        # 2. Dados de Prontuários
        medical_records = MedicalRecord.objects.filter(doctor=doctor_profile)
        context['total_medical_records'] = medical_records.count()
        
        # 3. Pacientes Únicos Atendidos
        # Filtra os prontuários criados pelo médico e conta os pacientes únicos
        unique_patients = medical_records.values('patient').distinct().count()
        context['unique_patients_attended'] = unique_patients
        
        # 4. Atividade Recente (Últimos 30 dias)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_appointments = appointments.filter(scheduled_date__gte=thirty_days_ago)
        
        context['recent_appointments_count'] = recent_appointments.count()
        
        # 5. Top 5 Diagnósticos (simples)
        # Agrupa por diagnóstico e conta
        top_diagnoses = medical_records.values('diagnosis').annotate(count=Count('diagnosis')).order_by('-count')[:5]
        context['top_diagnoses'] = top_diagnoses
        
        return context


# Views placeholder existentes (mantidas para compatibilidade)
class ReportListView(LoginRequiredMixin, ListView):
    # model = Report # Descomentar se o modelo Report for implementado
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        # Retorna uma lista vazia ou implementa a lógica de listagem de relatórios
        return []

class ReportDetailView(LoginRequiredMixin, DetailView):
    # model = Report # Descomentar se o modelo Report for implementado
    template_name = 'reports/report_detail.html'
    
    def get_object(self, queryset=None):
        # Retorna um objeto placeholder ou implementa a lógica de detalhe de relatório
        raise Http404("Relatório não encontrado.")

class ReportGenerateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/report_generate.html'
