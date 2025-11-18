"""
Modelos para o app de relatórios.
"""

from django.db import models
from django.conf import settings


class Report(models.Model):
    """
    Modelo de Relatório.
    """
    
    REPORT_TYPE_CHOICES = (
        ('appointments', 'Relatório de Consultas'),
        ('patients', 'Relatório de Pacientes'),
        ('doctors', 'Relatório de Médicos'),
        ('prescriptions', 'Relatório de Prescrições'),
        ('exams', 'Relatório de Exames'),
        ('vaccines', 'Relatório de Vacinas'),
        ('custom', 'Relatório Personalizado'),
    )
    
    FORMAT_CHOICES = (
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    )
    
    title = models.CharField(
        'Título',
        max_length=200
    )
    
    report_type = models.CharField(
        'Tipo de Relatório',
        max_length=20,
        choices=REPORT_TYPE_CHOICES
    )
    
    description = models.TextField(
        'Descrição',
        blank=True
    )
    
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='generated_reports',
        verbose_name='Gerado por'
    )
    
    start_date = models.DateField(
        'Data Inicial',
        null=True,
        blank=True
    )
    
    end_date = models.DateField(
        'Data Final',
        null=True,
        blank=True
    )
    
    filters = models.JSONField(
        'Filtros',
        default=dict,
        blank=True,
        help_text='Filtros aplicados ao relatório em formato JSON'
    )
    
    format = models.CharField(
        'Formato',
        max_length=10,
        choices=FORMAT_CHOICES,
        default='pdf'
    )
    
    file = models.FileField(
        'Arquivo',
        upload_to='reports/%Y/%m/',
        blank=True
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%d/%m/%Y')})"
