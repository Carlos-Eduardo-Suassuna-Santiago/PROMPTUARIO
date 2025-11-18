"""
Testes para a funcionalidade de registro de usuários.
"""

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile, AttendantProfile
from patients.models import Patient

User = get_user_model()


@pytest.mark.django_db
class TestPatientRegistration:
    """Testes para registro de pacientes."""
    
    def test_patient_registration_view_get(self, client):
        """Testa acesso à página de registro de paciente."""
        url = reverse('accounts:register_patient')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Cadastro de Paciente' in response.content.decode()
    
    def test_patient_registration_success(self, client):
        """Testa registro bem-sucedido de paciente."""
        url = reverse('accounts:register_patient')
        data = {
            'username': 'novopaciente',
            'email': 'novopaciente@test.com',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123',
            'first_name': 'João',
            'last_name': 'Silva',
            'cpf': '123.456.789-00',
            'phone': '(11) 91234-5678',
            'birth_date': '1990-01-01',
            'blood_type': 'O+',
            'height': '175.00',
            'weight': '75.00'
        }
        response = client.post(url, data)
        
        # Verifica redirecionamento
        assert response.status_code == 302
        
        # Verifica criação do usuário
        user = User.objects.get(username='novopaciente')
        assert user.email == 'novopaciente@test.com'
        assert user.user_type == 'patient'
        
        # Verifica criação do perfil de paciente
        patient = Patient.objects.get(user=user)
        assert patient.blood_type == 'O+'
        assert float(patient.height) == 175.00
    
    def test_patient_registration_duplicate_cpf(self, client):
        """Testa registro com CPF duplicado."""
        # Cria primeiro usuário
        User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='pass123',
            cpf='123.456.789-00',
            user_type='patient'
        )
        
        # Tenta criar segundo usuário com mesmo CPF
        url = reverse('accounts:register_patient')
        data = {
            'username': 'user2',
            'email': 'user2@test.com',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'cpf': '123.456.789-00',  # CPF duplicado
        }
        response = client.post(url, data)
        
        # Verifica que não foi criado
        assert response.status_code == 200
        assert 'Este CPF já está cadastrado' in response.content.decode()
        assert not User.objects.filter(username='user2').exists()
    
    def test_patient_registration_password_mismatch(self, client):
        """Testa registro com senhas diferentes."""
        url = reverse('accounts:register_patient')
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'senhaforte123',
            'password2': 'senhadiferente123',  # Senha diferente
            'first_name': 'João',
            'last_name': 'Silva',
            'cpf': '123.456.789-00',
        }
        response = client.post(url, data)
        
        # Verifica que não foi criado
        assert response.status_code == 200
        assert not User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
class TestDoctorRegistration:
    """Testes para registro de médicos."""
    
    def test_doctor_registration_requires_admin(self, client):
        """Testa que registro de médico requer admin."""
        url = reverse('accounts:register_doctor')
        response = client.get(url)
        
        # Deve redirecionar para login
        assert response.status_code == 302
    
    def test_doctor_registration_success(self, client, admin_user):
        """Testa registro bem-sucedido de médico por admin."""
        client.force_login(admin_user)
        
        url = reverse('accounts:register_doctor')
        data = {
            'username': 'novomedico',
            'email': 'medico@test.com',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123',
            'first_name': 'Dr. Carlos',
            'last_name': 'Oliveira',
            'cpf': '987.654.321-00',
            'phone': '(11) 98765-4321',
            'crm': '54321-SP',
            'specialty': 'Cardiologia',
            'consultation_price': '250.00'
        }
        response = client.post(url, data)
        
        # Verifica redirecionamento
        assert response.status_code == 302
        
        # Verifica criação do usuário
        user = User.objects.get(username='novomedico')
        assert user.user_type == 'doctor'
        
        # Verifica criação do perfil de médico
        doctor = DoctorProfile.objects.get(user=user)
        assert doctor.crm == '54321-SP'
        assert doctor.specialty == 'Cardiologia'
    
    def test_doctor_registration_duplicate_crm(self, client, admin_user):
        """Testa registro com CRM duplicado."""
        client.force_login(admin_user)
        
        # Cria primeiro médico
        user1 = User.objects.create_user(
            username='doctor1',
            email='doctor1@test.com',
            password='pass123',
            cpf='111.111.111-11',
            user_type='doctor'
        )
        DoctorProfile.objects.create(
            user=user1,
            crm='12345-SP',
            specialty='Clínico Geral'
        )
        
        # Tenta criar segundo médico com mesmo CRM
        url = reverse('accounts:register_doctor')
        data = {
            'username': 'doctor2',
            'email': 'doctor2@test.com',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123',
            'first_name': 'Dr. José',
            'last_name': 'Silva',
            'cpf': '222.222.222-22',
            'crm': '12345-SP',  # CRM duplicado
            'specialty': 'Pediatria'
        }
        response = client.post(url, data)
        
        # Verifica que não foi criado
        assert response.status_code == 200
        assert 'Este CRM já está cadastrado' in response.content.decode()


@pytest.mark.django_db
class TestAttendantRegistration:
    """Testes para registro de atendentes."""
    
    def test_attendant_registration_requires_admin(self, client):
        """Testa que registro de atendente requer admin."""
        url = reverse('accounts:register_attendant')
        response = client.get(url)
        
        # Deve redirecionar para login
        assert response.status_code == 302
    
    def test_attendant_registration_success(self, client, admin_user):
        """Testa registro bem-sucedido de atendente por admin."""
        client.force_login(admin_user)
        
        url = reverse('accounts:register_attendant')
        data = {
            'username': 'novoatendente',
            'email': 'atendente@test.com',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123',
            'first_name': 'Ana',
            'last_name': 'Costa',
            'cpf': '555.555.555-55',
            'phone': '(11) 95555-5555',
            'department': 'Recepção',
            'shift': 'morning'
        }
        response = client.post(url, data)
        
        # Verifica redirecionamento
        assert response.status_code == 302
        
        # Verifica criação do usuário
        user = User.objects.get(username='novoatendente')
        assert user.user_type == 'attendant'
        
        # Verifica criação do perfil de atendente
        attendant = AttendantProfile.objects.get(user=user)
        assert attendant.department == 'Recepção'
        assert attendant.shift == 'morning'


# Fixtures
@pytest.fixture
def admin_user(db):
    """Cria um usuário admin para testes."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123',
        cpf='000.000.000-00'
    )
