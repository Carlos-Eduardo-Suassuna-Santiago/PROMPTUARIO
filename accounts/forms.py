"""
Formulários para o app accounts.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, DoctorProfile, AttendantProfile
from patients.models import Patient


class UserRegistrationForm(UserCreationForm):
    """Formulário base para registro de usuários."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'})
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'João'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Silva'})
    )
    cpf = forms.CharField(
        max_length=14,
        required=True,
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'onkeyup': 'formatCPF(this)'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000',
            'onkeyup': 'formatPhone(this)'
        })
    )
    birth_date = forms.DateField(
        required=False,
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        label='Endereço',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, número'})
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        label='Cidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'São Paulo'})
    )
    state = forms.CharField(
        max_length=2,
        required=False,
        label='Estado',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SP', 'maxlength': '2'})
    )
    zip_code = forms.CharField(
        max_length=9,
        required=False,
        label='CEP',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000',
            'onkeyup': 'formatCEP(this)'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'cpf', 'phone', 
                  'birth_date', 'address', 'city', 'state', 'zip_code', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario123'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirme a Senha'

    def clean_cpf(self):
        """Valida se o CPF já não está cadastrado."""
        cpf = self.cleaned_data.get('cpf')
        if User.objects.filter(cpf=cpf).exists():
            raise ValidationError('Este CPF já está cadastrado no sistema.')
        return cpf

    def clean_email(self):
        """Valida se o email já não está cadastrado."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado no sistema.')
        return email


class PatientRegistrationForm(UserRegistrationForm):
    """Formulário de registro para pacientes."""
    
    blood_type = forms.ChoiceField(
        choices=[('', 'Selecione')] + list(Patient.BLOOD_TYPE_CHOICES),
        required=False,
        label='Tipo Sanguíneo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    height = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label='Altura (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '175.00'})
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label='Peso (kg)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '75.00'})
    )
    emergency_contact_name = forms.CharField(
        max_length=200,
        required=False,
        label='Nome do Contato de Emergência',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maria Silva'})
    )
    emergency_contact_phone = forms.CharField(
        max_length=20,
        required=False,
        label='Telefone do Contato de Emergência',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000',
            'onkeyup': 'formatPhone(this)'
        })
    )
    medical_notes = forms.CharField(
        required=False,
        label='Observações Médicas',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Informações adicionais relevantes...'
        })
    )

    def save(self, commit=True):
        """Salva o usuário e cria o perfil de paciente."""
        user = super().save(commit=False)
        user.user_type = 'patient'
        
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                blood_type=self.cleaned_data.get('blood_type'),
                height=self.cleaned_data.get('height'),
                weight=self.cleaned_data.get('weight'),
                emergency_contact_name=self.cleaned_data.get('emergency_contact_name'),
                emergency_contact_phone=self.cleaned_data.get('emergency_contact_phone'),
                medical_notes=self.cleaned_data.get('medical_notes')
            )
        
        return user


class DoctorRegistrationForm(UserRegistrationForm):
    """Formulário de registro para médicos (apenas admin)."""
    
    crm = forms.CharField(
        max_length=20,
        required=True,
        label='CRM',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345-SP'})
    )
    specialty = forms.CharField(
        max_length=100,
        required=True,
        label='Especialidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cardiologia'})
    )
    salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Salário (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '3000.00'})
    )
    is_available = forms.BooleanField(
        required=False,
        label='Disponível para Consultas',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_crm(self):
        """Valida se o CRM já não está cadastrado."""
        crm = self.cleaned_data.get('crm')
        if DoctorProfile.objects.filter(crm=crm).exists():
            raise ValidationError('Este CRM já está cadastrado no sistema.')
        return crm

    def save(self, commit=True):
        """Salva o usuário e cria o perfil de médico."""
        user = super().save(commit=False)
        user.user_type = 'doctor'
        
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                crm=self.cleaned_data.get('crm'),
                specialty=self.cleaned_data.get('specialty'),
                salary=self.cleaned_data.get('salary'),
                is_available=self.cleaned_data.get('is_available')
            )
        
        return user


class AttendantRegistrationForm(UserRegistrationForm):
    """Formulário de registro para atendentes (apenas admin)."""
    
    department = forms.CharField(
        max_length=100,
        required=False,
        label='Departamento',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recepção'})
    )
    shift = forms.ChoiceField(
        choices=[('', 'Selecione'), ('morning', 'Manhã'), ('afternoon', 'Tarde'), ('night', 'Noite'), ('full', 'Integral')],
        required=False,
        label='Turno',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def save(self, commit=True):
        """Salva o usuário e cria o perfil de atendente."""
        user = super().save(commit=False)
        user.user_type = 'attendant'
        
        if commit:
            user.save()
            AttendantProfile.objects.create(
                user=user,
                department=self.cleaned_data.get('department'),
                shift=self.cleaned_data.get('shift')
            )
        
        return user


# ==============================================================================
# Formulários de Atualização de Perfil
# ==============================================================================

class DoctorProfileUpdateForm(forms.ModelForm):
    """Formulário para atualização de perfil de Médico."""
    
    class Meta:
        model = DoctorProfile
        fields = ['crm', 'specialty', 'salary', 'is_available']
        widgets = {
            'crm': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AttendantProfileUpdateForm(forms.ModelForm):
    """Formulário para atualização de perfil de Atendente."""
    
    class Meta:
        model = AttendantProfile
        fields = ['department', 'shift']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-control'}),
        }
