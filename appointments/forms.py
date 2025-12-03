"""
Formulários para o app appointments.
"""

from django import forms
from .models import Appointment
from accounts.models import DoctorProfile
from patients.models import Patient
from django.utils import timezone
from datetime import timedelta


class PatientAppointmentForm(forms.ModelForm):
    """
    Formulário para agendamento de consulta por paciente.
    Permite escolher médico, data e hora.
    """
    
    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.all(),
        label='Médico',
        empty_label='Selecione um médico',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    scheduled_date = forms.DateField(
        label='Data da Consulta',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': (timezone.now().date() + timedelta(days=1)).isoformat() # Agendamento a partir do dia seguinte
        })
    )
    
    scheduled_time = forms.TimeField(
        label='Hora da Consulta',
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    
    reason = forms.CharField(
        label='Motivo da Consulta',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'scheduled_date', 'scheduled_time', 'reason']

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        scheduled_date = cleaned_data.get('scheduled_date')
        scheduled_time = cleaned_data.get('scheduled_time')

        if doctor and scheduled_date and scheduled_time:
            # 1. Verificar se o horário está dentro do horário de trabalho do médico (simplificado)
            # A lógica completa de horários e ausências seria implementada aqui.
            # Por enquanto, apenas uma verificação básica de horário comercial (8h às 18h)
            if scheduled_time.hour < 8 or scheduled_time.hour >= 18:
                raise forms.ValidationError("O horário selecionado está fora do horário comercial (8h às 18h).")

            # 2. Verificar se o médico já tem uma consulta agendada neste horário
            is_booked = Appointment.objects.filter(
                doctor=doctor,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status__in=['scheduled', 'confirmed']
            ).exists()

            if is_booked:
                raise forms.ValidationError("O médico já possui uma consulta agendada neste horário. Por favor, escolha outro horário.")

            # 3. Verificar se o agendamento é para o futuro (já feito no widget, mas bom ter no backend)
            scheduled_datetime = timezone.make_aware(timezone.datetime.combine(scheduled_date, scheduled_time))
            if scheduled_datetime <= timezone.now():
                raise forms.ValidationError("O agendamento deve ser para uma data e hora futura.")

        return cleaned_data

    def save(self, commit=True, patient=None):
        appointment = super().save(commit=False)
        if patient:
            appointment.patient = patient
        appointment.status = 'scheduled'
        
        if commit:
            appointment.save()
        return appointment


class AttendantAppointmentForm(PatientAppointmentForm):
    """
    Formulário para agendamento de consulta por atendente.
    Permite escolher o paciente, além de médico, data e hora.
    """
    
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label='Paciente',
        empty_label='Selecione um paciente',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'scheduled_date', 'scheduled_time', 'reason']
