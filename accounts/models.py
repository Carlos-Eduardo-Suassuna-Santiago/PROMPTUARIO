"""
Modelos para o app de contas e autenticação.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Modelo de usuário customizado que estende AbstractUser.
    Suporta diferentes tipos de usuários: Admin, Médico, Atendente, Paciente.
    """
    
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('doctor', 'Médico'),
        ('attendant', 'Atendente'),
        ('patient', 'Paciente'),
    )
    
    user_type = models.CharField(
        'Tipo de Usuário',
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='patient'
    )
    
    cpf = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        help_text='Formato: 000.000.000-00'
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        help_text='Formato: (00) 00000-0000'
    )
    
    birth_date = models.DateField(
        'Data de Nascimento',
        null=True,
        blank=True
    )
    
    address = models.CharField(
        'Endereço',
        max_length=255,
        blank=True
    )
    
    city = models.CharField(
        'Cidade',
        max_length=100,
        blank=True
    )
    
    state = models.CharField(
        'Estado',
        max_length=2,
        blank=True
    )
    
    zip_code = models.CharField(
        'CEP',
        max_length=10,
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
    
    is_active_user = models.BooleanField(
        'Usuário Ativo',
        default=True,
        help_text='Indica se o usuário está ativo no sistema'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
    
    def is_admin(self):
        """Verifica se o usuário é administrador."""
        return self.user_type == 'admin'
    
    def is_doctor(self):
        """Verifica se o usuário é médico."""
        return self.user_type == 'doctor'
    
    def is_attendant(self):
        """Verifica se o usuário é atendente."""
        return self.user_type == 'attendant'
    
    def is_patient(self):
        """Verifica se o usuário é paciente."""
        return self.user_type == 'patient'


class DoctorProfile(models.Model):
    """
    Perfil estendido para médicos.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='Usuário'
    )
    
    crm = models.CharField(
        'CRM',
        max_length=20,
        unique=True,
        help_text='Registro no Conselho Regional de Medicina'
    )
    
    specialty = models.CharField(
        'Especialidade',
        max_length=100
    )
    
    salary = models.DecimalField(
        'Salário',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    is_available = models.BooleanField(
        'Disponível',
        default=True,
        help_text='Indica se o médico está disponível para consultas'
    )
    
    class Meta:
        verbose_name = 'Perfil de Médico'
        verbose_name_plural = 'Perfis de Médicos'
    
    def __str__(self):
        return f"Dr(a). {self.user.get_full_name()} - CRM: {self.crm}"


class AttendantProfile(models.Model):
    """
    Perfil estendido para atendentes.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='attendant_profile',
        verbose_name='Usuário'
    )
    
    department = models.CharField(
        'Departamento',
        max_length=100,
        blank=True
    )
    
    shift = models.CharField(
        'Turno',
        max_length=20,
        choices=(
            ('morning', 'Manhã'),
            ('afternoon', 'Tarde'),
            ('night', 'Noite'),
            ('full', 'Integral'),
        ),
        default='full'
    )
    
    class Meta:
        verbose_name = 'Perfil de Atendente'
        verbose_name_plural = 'Perfis de Atendentes'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_shift_display()}"


class DoctorSchedule(models.Model):
    """
    Quadro de horários dos médicos.
    """
    
    WEEKDAY_CHOICES = (
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )
    
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Médico'
    )
    
    weekday = models.IntegerField(
        'Dia da Semana',
        choices=WEEKDAY_CHOICES
    )
    
    start_time = models.TimeField(
        'Horário de Início'
    )
    
    end_time = models.TimeField(
        'Horário de Término'
    )
    
    is_on_call = models.BooleanField(
        'Plantão',
        default=False,
        help_text='Indica se é um plantão'
    )
    
    is_active = models.BooleanField(
        'Ativo',
        default=True
    )
    
    class Meta:
        verbose_name = 'Horário de Médico'
        verbose_name_plural = 'Horários de Médicos'
        ordering = ['weekday', 'start_time']
        unique_together = ['doctor', 'weekday', 'start_time']
    
    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.get_weekday_display()} ({self.start_time} - {self.end_time})"


class DoctorAbsence(models.Model):
    """
    Registro de ausências dos médicos.
    """
    
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='absences',
        verbose_name='Médico'
    )
    
    start_datetime = models.DateTimeField(
        'Início da Ausência'
    )
    
    end_datetime = models.DateTimeField(
        'Fim da Ausência'
    )
    
    reason = models.TextField(
        'Motivo',
        blank=True
    )
    
    is_full_day = models.BooleanField(
        'Dia Inteiro',
        default=False
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Ausência de Médico'
        verbose_name_plural = 'Ausências de Médicos'
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.start_datetime.strftime('%d/%m/%Y')}"
