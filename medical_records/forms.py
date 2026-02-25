from django import forms
from .models import MedicalRecord, Prescription, Exam

class MedicalRecordForm(forms.ModelForm):
    """
    Formulário para criação e edição de Prontuário Médico.
    """
    class Meta:
        model = MedicalRecord
        fields = [
            'chief_complaint', 'symptoms', 'physical_examination', 
            'diagnosis', 'treatment_plan', 'observations'
        ]
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'physical_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PrescriptionForm(forms.ModelForm):
    """
    Formulário para criação de Receita Médica.
    """
    class Meta:
        model = Prescription
        fields = ['medications', 'instructions', 'valid_until']
        widgets = {
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ExamForm(forms.ModelForm):
    """
    Formulário para solicitação de Exame.
    """
    class Meta:
        model = Exam
        fields = ['exam_type', 'exam_name', 'description', 'scheduled_date']
        widgets = {
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
