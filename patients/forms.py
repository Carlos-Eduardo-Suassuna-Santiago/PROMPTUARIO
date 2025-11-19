"""
Formulários para o app patients.
"""

from django import forms
from .models import Patient


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
