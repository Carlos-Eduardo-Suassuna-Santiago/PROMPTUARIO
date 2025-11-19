"""
Modelos para o app de pacientes.
"""

from django.db import models
from django.conf import settings


class Patient(models.Model):
    """
    Modelo de Paciente.
    """
    
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name='Usuário'
    )
    
    blood_type = models.CharField(
        'Tipo Sanguíneo',
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        blank=True
    )
    
    height = models.DecimalField(
        'Altura (cm)',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    weight = models.DecimalField(
        'Peso (kg)',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    emergency_contact_name = models.CharField(
        'Nome do Contato de Emergência',
        max_length=100,
        blank=True
    )
    
    emergency_contact_phone = models.CharField(
        'Telefone do Contato de Emergência',
        max_length=20,
        blank=True
    )
    
    medical_notes = models.TextField(
        'Observações Médicas',
        blank=True,
        help_text='Informações médicas gerais do paciente'
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
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - CPF: {self.user.cpf}"
    
    def get_age(self):
        """Calcula a idade do paciente."""
        from datetime import date
        if self.user.birth_date:
            today = date.today()
            return today.year - self.user.birth_date.year - (
                (today.month, today.day) < (self.user.birth_date.month, self.user.birth_date.day)
            )
        return None


class Allergy(models.Model):
    """
    Modelo de Alergia do Paciente.
    """
    
    SEVERITY_CHOICES = (
        ('mild', 'Leve'),
        ('moderate', 'Moderada'),
        ('severe', 'Grave'),
    )
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='allergies',
        verbose_name='Paciente'
    )
    
    allergen = models.CharField(
        'Alérgeno',
        max_length=200,
        help_text='Substância que causa alergia'
    )
    
    severity = models.CharField(
        'Gravidade',
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='mild'
    )
    
    reaction = models.TextField(
        'Reação',
        blank=True,
        help_text='Descrição da reação alérgica'
    )
    
    diagnosed_date = models.DateField(
        'Data do Diagnóstico',
        null=True,
        blank=True
    )
    
    notes = models.TextField(
        'Observações',
        blank=True
    )
    
    is_active = models.BooleanField(
        'Ativa',
        default=True
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Alergia'
        verbose_name_plural = 'Alergias'
        ordering = ['-severity', 'allergen']
    
    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.allergen}"


class Vaccine(models.Model):
    """
    Modelo de Vacina do Paciente.
    """
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='vaccines',
        verbose_name='Paciente'
    )
    
    name = models.CharField(
        'Nome da Vacina',
        max_length=200
    )
    
    dose = models.CharField(
        'Dose',
        max_length=50,
        help_text='Ex: 1ª dose, 2ª dose, dose única, reforço'
    )
    
    application_date = models.DateField(
        'Data de Aplicação'
    )
    
    next_dose_date = models.DateField(
        'Data da Próxima Dose',
        null=True,
        blank=True
    )
    
    batch_number = models.CharField(
        'Número do Lote',
        max_length=50,
        blank=True
    )
    
    manufacturer = models.CharField(
        'Fabricante',
        max_length=100,
        blank=True
    )
    
    location = models.CharField(
        'Local de Aplicação',
        max_length=200,
        blank=True,
        help_text='Unidade de saúde onde foi aplicada'
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
        verbose_name = 'Vacina'
        verbose_name_plural = 'Vacinas'
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.name} - {self.dose} ({self.application_date.strftime('%d/%m/%Y')})"


class Medication(models.Model):
    """
    Modelo de Medicamento em uso pelo Paciente.
    """
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medications',
        verbose_name='Paciente'
    )
    
    name = models.CharField(
        'Nome do Medicamento',
        max_length=200
    )
    
    dosage = models.CharField(
        'Dosagem',
        max_length=100,
        help_text='Ex: 500mg, 10ml'
    )
    
    frequency = models.CharField(
        'Frequência',
        max_length=100,
        help_text='Ex: 2x ao dia, de 8 em 8 horas'
    )
    
    start_date = models.DateField(
        'Data de Início'
    )
    
    end_date = models.DateField(
        'Data de Término',
        null=True,
        blank=True
    )
    
    prescribed_by = models.ForeignKey(
        'accounts.DoctorProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescribed_medications',
        verbose_name='Prescrito por'
    )
    
    notes = models.TextField(
        'Observações',
        blank=True
    )
    
    is_active = models.BooleanField(
        'Em Uso',
        default=True
    )
    
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['-is_active', '-start_date']
    
    def __str__(self):
        return f"{self.name} - {self.dosage} ({self.frequency})"
