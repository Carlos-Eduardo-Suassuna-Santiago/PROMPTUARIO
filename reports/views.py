from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import tempfile
from django.views import View

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

    def post(self, request, *args, **kwargs):
        """
        Gera os dados completos do relatório e os envia para o template.
        """
        user = request.user
        
        # Verifica se é médico (se quiser permitir só médicos)
        if not user.is_doctor():
            return self.render_to_response({
                "error": "Apenas médicos podem gerar este relatório."
            })

        doctor_profile = user.doctor_profile
        
        # ---------------------------
        # 1. Agendamentos do médico
        # ---------------------------
        appointments = Appointment.objects.filter(doctor=doctor_profile)

        total_appointments = appointments.count()
        completed_appointments = appointments.filter(status='completed').count()
        cancelled_appointments = appointments.filter(status='cancelled').count()

        # ---------------------------
        # 2. Prontuários
        # ---------------------------
        medical_records = MedicalRecord.objects.filter(doctor=doctor_profile)
        total_medical_records = medical_records.count()

        # ---------------------------
        # 3. Pacientes únicos
        # ---------------------------
        unique_patients_attended = (
            medical_records.values('patient').distinct().count()
        )

        # ---------------------------
        # 4. Atividade nos últimos 30 dias
        # ---------------------------
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_appointments = appointments.filter(
            scheduled_date__gte=thirty_days_ago
        )
        recent_appointments_count = recent_appointments.count()

        # ---------------------------
        # 5. Top diagnósticos
        # ---------------------------
        top_diagnoses = (
            medical_records.values('diagnosis')
            .annotate(count=Count('diagnosis'))
            .order_by('-count')[:5]
        )

        # ---------------------------
        # Enviar tudo para o template
        # ---------------------------
        context = {
            "doctor": doctor_profile,
            "generated_at": timezone.now(),

            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "cancelled_appointments": cancelled_appointments,

            "total_medical_records": total_medical_records,
            "unique_patients_attended": unique_patients_attended,

            "recent_appointments_count": recent_appointments_count,

            "top_diagnoses": top_diagnoses,
        }

        return self.render_to_response(context)
    
class ReportPDFView(View):
    def get(self, request, *args, **kwargs):
        # Nome do arquivo
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

        # Criador do PDF
        pdf = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Cabeçalho
        story.append(Paragraph("<b>Relatório Médico</b>", styles['Title']))
        story.append(Spacer(1, 20))

        # Informações do médico
        doctor_name = request.user.get_full_name() or request.user.username
        story.append(Paragraph(f"Médico responsável: <b>{doctor_name}</b>", styles['Normal']))
        story.append(Paragraph(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))

        # Conteúdo principal
        story.append(Paragraph("<b>Resumo Geral</b>", styles['Heading2']))
        story.append(Paragraph(
            "Este relatório contém informações compiladas do sistema, incluindo dados do paciente, "
            "consultas, diagnósticos recentes e outras informações relevantes.",
            styles['Normal']
        ))
        story.append(Spacer(1, 15))

        # Exemplo de tabela
        data = [
            ["Campo", "Valor"],
            ["Total de Pacientes", "54"],
            ["Consultas no mês", "128"],
            ["Diagnósticos recentes", "32"],
        ]

        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
        ]))

        story.append(table)
        story.append(Spacer(1, 20))

        # Assinatura
        story.append(Paragraph("<br/><br/>__________________________________", styles['Normal']))
        story.append(Paragraph("Assinatura do Médico", styles['Normal']))

        # Gerar PDF
        pdf.build(story)

        return response