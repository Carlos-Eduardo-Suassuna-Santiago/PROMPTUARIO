from django import forms
from .models import MedicalRecord, Prescription, Exam

class MedicalRecordForm(forms.ModelForm):
    """
    Formulário para criação e edição de Prontuário Médico.
    """
    class Meta:
        model = MedicalRecord
        fields = [
            'appointment', 'patient', 'doctor', 
            'chief_complaint', 'symptoms', 'physical_examination', 
            'diagnosis', 'treatment_plan', 'observations'
        ]
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'physical_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos 'appointment', 'patient' e 'doctor' devem ser preenchidos automaticamente
        # ou restritos no contexto da view, mas mantidos no form para validação do modelo.
        # Por enquanto, vamos torná-los hidden.
        self.fields['appointment'].widget = forms.HiddenInput()
        self.fields['patient'].widget = forms.HiddenInput()
        self.fields['doctor'].widget = forms.HiddenInput()


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
