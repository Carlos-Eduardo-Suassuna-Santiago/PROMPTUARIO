"""
Modelos para o app de agendamentos.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Appointment(models.Model):
    """
    Modelo de Agendamento de Consulta.
    """
    
    STATUS_CHOICES = (
        ('scheduled', 'Agendada'),
        ('confirmed', 'Confirmada'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada'),
        ('no_show', 'Não Compareceu'),
    )
    
    APPOINTMENT_TYPE_CHOICES = (
        ('first_visit', 'Primeira Consulta'),
        ('return', 'Retorno'),
        ('emergency', 'Emergência'),
        ('routine', 'Rotina'),
    )
    
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Paciente'
    )
    
    doctor = models.ForeignKey(
        'accounts.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Médico'
    )
    
    scheduled_date = models.DateField(
        'Data da Consulta'
    )
    
    scheduled_time = models.TimeField(
        'Horário da Consulta'
    )
    
    duration_minutes = models.IntegerField(
        'Duração (minutos)',
        default=30
    )
    
    appointment_type = models.CharField(
        'Tipo de Consulta',
        max_length=20,
        choices=APPOINTMENT_TYPE_CHOICES,
        default='first_visit'
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    reason = models.TextField(
        'Motivo da Consulta',
        blank=True
    )
    
    notes = models.TextField(
        'Observações',
        blank=True
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_appointments',
        verbose_name='Criado por'
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )
    
    cancelled_at = models.DateTimeField(
        'Cancelado em',
        null=True,
        blank=True
    )
    
    cancellation_reason = models.TextField(
        'Motivo do Cancelamento',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-scheduled_date', '-scheduled_time']
        unique_together = ['doctor', 'scheduled_date', 'scheduled_time']
    
    def __str__(self):
        return f"{self.patient.user.get_full_name()} - Dr(a). {self.doctor.user.get_full_name()} ({self.scheduled_date.strftime('%d/%m/%Y')} {self.scheduled_time.strftime('%H:%M')})"
    
    def can_be_cancelled(self):
        """
        Verifica se a consulta pode ser cancelada.
        Regra: mínimo de 24 horas antes da consulta.
        """
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        if self.status in ['cancelled', 'completed']:
            return False
        
        appointment_datetime = timezone.make_aware(
            datetime.combine(self.scheduled_date, self.scheduled_time)
        )
        
        hours_until_appointment = (appointment_datetime - timezone.now()).total_seconds() / 3600
        
        return hours_until_appointment >= settings.APPOINTMENT_CANCELLATION_HOURS
    
    def cancel(self, reason='', user=None):
        """Cancela a consulta."""
        if self.can_be_cancelled():
            self.status = 'cancelled'
            self.cancelled_at = timezone.now()
            self.cancellation_reason = reason
            self.save()
            return True
        return False


class AppointmentNotification(models.Model):
    """
    Modelo de Notificação de Agendamento.
    """
    
    NOTIFICATION_TYPE_CHOICES = (
        ('reminder', 'Lembrete'),
        ('cancellation', 'Cancelamento'),
        ('rescheduling', 'Remarcação'),
        ('doctor_absence', 'Ausência do Médico'),
    )
    
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Agendamento'
    )
    
    notification_type = models.CharField(
        'Tipo de Notificação',
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES
    )
    
    message = models.TextField(
        'Mensagem'
    )
    
    sent_at = models.DateTimeField(
        'Enviado em',
        auto_now_add=True
    )
    
    is_read = models.BooleanField(
        'Lida',
        default=False
    )
    
    class Meta:
        verbose_name = 'Notificação de Agendamento'
        verbose_name_plural = 'Notificações de Agendamentos'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.appointment.patient.user.get_full_name()}"


class ReturnRequest(models.Model):
    """
    Modelo de Solicitação de Retorno.
    """
    
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('scheduled', 'Agendado'),
        ('cancelled', 'Cancelado'),
    )
    
    original_appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='return_requests',
        verbose_name='Consulta Original'
    )
    
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='return_requests',
        verbose_name='Paciente'
    )
    
    doctor = models.ForeignKey(
        'accounts.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='return_requests',
        verbose_name='Médico'
    )
    
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requested_returns',
        verbose_name='Solicitado por'
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    notes = models.TextField(
        'Observações',
        blank=True
    )
    
    new_appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='return_request',
        verbose_name='Novo Agendamento'
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Solicitação de Retorno'
        verbose_name_plural = 'Solicitações de Retorno'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Retorno - {self.patient.user.get_full_name()} ({self.get_status_display()})"
