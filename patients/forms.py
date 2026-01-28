"""
Formulários para o app patients.
"""

from django import forms
from .models import Patient, Allergy, Vaccine, Medication


class PatientProfileUpdateForm(forms.ModelForm):
    """
    Formulário para atualização de informações médicas do paciente.
    """
    
    class Meta:
        model = Patient
        fields = [
            'blood_type', 'height', 'weight', 
            'emergency_contact_name', 'emergency_contact_phone', 
            'medical_notes'
        ]
        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kg'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AllergyForm(forms.ModelForm):
    """Formulário para adicionar/editar alergias."""
    
    class Meta:
        model = Allergy
        fields = ['allergen', 'severity', 'reaction', 'diagnosed_date', 'notes']
        widgets = {
            'allergen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Penicilina, Amendoim, Latex'
            }),
            'severity': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reaction': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva a reação alérgica',
                'rows': 3
            }),
            'diagnosed_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações adicionais',
                'rows': 2
            }),
        }


class VaccineForm(forms.ModelForm):
    """Formulário para adicionar/editar vacinas."""
    
    class Meta:
        model = Vaccine
        fields = ['name', 'dose', 'application_date', 'next_dose_date', 'batch_number', 'manufacturer', 'location', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: COVID-19, Gripe, Tétano'
            }),
            'dose': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1ª dose, 2ª dose, reforço'
            }),
            'application_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'next_dose_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'batch_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do lote'
            }),
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fabricante'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unidade de saúde'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações',
                'rows': 2
            }),
        }


class MedicationForm(forms.ModelForm):
    """Formulário para adicionar/editar medicamentos."""
    
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'frequency', 'start_date', 'end_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Dipirona, Amoxicilina'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 500mg, 10ml'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2x ao dia, de 8 em 8 horas'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações',
                'rows': 2
            }),
        }
