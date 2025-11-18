"""
Modelos para o app de prontuários médicos.
"""

from django.db import models
from django.conf import settings


class MedicalRecord(models.Model):
    """
    Modelo de Prontuário Médico (Registro de Consulta).
    """
    
    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name='medical_record',
        verbose_name='Consulta'
    )
    
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name='Paciente'
    )
    
    doctor = models.ForeignKey(
        'accounts.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name='Médico'
    )
    
    chief_complaint = models.TextField(
        'Queixa Principal',
        help_text='Motivo da consulta relatado pelo paciente'
    )
    
    symptoms = models.TextField(
        'Sintomas',
        blank=True
    )
    
    physical_examination = models.TextField(
        'Exame Físico',
        blank=True
    )
    
    diagnosis = models.TextField(
        'Diagnóstico'
    )
    
    treatment_plan = models.TextField(
        'Plano de Tratamento',
        blank=True
    )
    
    observations = models.TextField(
        'Observações',
        blank=True
    )
    
    is_closed = models.BooleanField(
        'Fechado',
        default=False,
        help_text='Indica se o prontuário foi fechado (não pode mais ser editado)'
    )
    
    closed_at = models.DateTimeField(
        'Fechado em',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Prontuário Médico'
        verbose_name_plural = 'Prontuários Médicos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prontuário - {self.patient.user.get_full_name()} ({self.appointment.scheduled_date.strftime('%d/%m/%Y')})"
    
    def close_record(self):
        """Fecha o prontuário, impedindo edições futuras."""
        from django.utils import timezone
        if not self.is_closed:
            self.is_closed = True
            self.closed_at = timezone.now()
            self.save()


class MedicalRecordComment(models.Model):
    """
    Modelo de Comentário em Prontuário Médico.
    Permite adicionar comentários mesmo após o fechamento do prontuário.
    """
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Prontuário'
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_record_comments',
        verbose_name='Autor'
    )
    
    comment = models.TextField(
        'Comentário'
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Comentário de Prontuário'
        verbose_name_plural = 'Comentários de Prontuários'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentário por {self.author.get_full_name()} em {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class Prescription(models.Model):
    """
    Modelo de Receita Médica.
    """
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Prontuário'
    )
    
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Paciente'
    )
    
    doctor = models.ForeignKey(
        'accounts.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name='Médico'
    )
    
    medications = models.TextField(
        'Medicamentos',
        help_text='Lista de medicamentos prescritos'
    )
    
    instructions = models.TextField(
        'Instruções',
        blank=True
    )
    
    valid_until = models.DateField(
        'Válida até',
        null=True,
        blank=True
    )
    
    prescription_file = models.FileField(
        'Arquivo da Receita',
        upload_to='prescriptions/%Y/%m/',
        blank=True,
        help_text='Receita em formato PDF'
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Receita Médica'
        verbose_name_plural = 'Receitas Médicas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Receita - {self.patient.user.get_full_name()} ({self.created_at.strftime('%d/%m/%Y')})"


class Exam(models.Model):
    """
    Modelo de Exame Médico.
    """
    
    EXAM_TYPE_CHOICES = (
        ('blood', 'Exame de Sangue'),
        ('urine', 'Exame de Urina'),
        ('imaging', 'Exame de Imagem'),
        ('biopsy', 'Biópsia'),
        ('other', 'Outro'),
    )
    
    STATUS_CHOICES = (
        ('requested', 'Solicitado'),
        ('scheduled', 'Agendado'),
        ('completed', 'Realizado'),
        ('cancelled', 'Cancelado'),
    )
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='exams',
        verbose_name='Prontuário',
        null=True,
        blank=True
    )
    
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='exams',
        verbose_name='Paciente'
    )
    
    doctor = models.ForeignKey(
        'accounts.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='requested_exams',
        verbose_name='Médico Solicitante'
    )
    
    exam_type = models.CharField(
        'Tipo de Exame',
        max_length=20,
        choices=EXAM_TYPE_CHOICES
    )
    
    exam_name = models.CharField(
        'Nome do Exame',
        max_length=200
    )
    
    description = models.TextField(
        'Descrição',
        blank=True
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested'
    )
    
    requested_date = models.DateField(
        'Data da Solicitação',
        auto_now_add=True
    )
    
    scheduled_date = models.DateField(
        'Data Agendada',
        null=True,
        blank=True
    )
    
    completed_date = models.DateField(
        'Data de Realização',
        null=True,
        blank=True
    )
    
    result = models.TextField(
        'Resultado',
        blank=True
    )
    
    result_file = models.FileField(
        'Arquivo do Resultado',
        upload_to='exams/%Y/%m/',
        blank=True
    )
    
    notes = models.TextField(
        'Observações',
        blank=True
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'
        ordering = ['-requested_date']
    
    def __str__(self):
        return f"{self.exam_name} - {self.patient.user.get_full_name()} ({self.get_status_display()})"


class MedicalRecordHistory(models.Model):
    """
    Modelo de Histórico de Alterações em Prontuário.
    Registra todas as modificações realizadas no prontuário.
    """
    
    ACTION_CHOICES = (
        ('created', 'Criado'),
        ('updated', 'Atualizado'),
        ('closed', 'Fechado'),
        ('comment_added', 'Comentário Adicionado'),
    )
    
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Prontuário'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_record_actions',
        verbose_name='Usuário'
    )
    
    action = models.CharField(
        'Ação',
        max_length=20,
        choices=ACTION_CHOICES
    )
    
    description = models.TextField(
        'Descrição',
        blank=True
    )
    
    timestamp = models.DateTimeField(
        'Data/Hora',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Histórico de Prontuário'
        verbose_name_plural = 'Históricos de Prontuários'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_action_display()} por {self.user.get_full_name()} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
