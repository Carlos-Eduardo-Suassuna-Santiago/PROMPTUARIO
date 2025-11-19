"""
Testes para o app accounts.
"""

import pytest
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile, AttendantProfile

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Testes para o modelo User."""
    
    def test_create_user(self):
        """Testa criação de usuário."""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            cpf='123.456.789-00',
            user_type='patient'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@test.com'
        assert user.is_patient()
        assert not user.is_doctor()
    
    def test_create_superuser(self):
        """Testa criação de superusuário."""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            cpf='000.000.000-00'
        )
        assert user.is_staff
        assert user.is_superuser


@pytest.mark.django_db
class TestDoctorProfile:
    """Testes para o modelo DoctorProfile."""
    
    def test_create_doctor_profile(self):
        """Testa criação de perfil de médico."""
        user = User.objects.create_user(
            username='doctor',
            email='doctor@test.com',
            password='doctor123',
            cpf='111.111.111-11',
            user_type='doctor'
        )
        profile = DoctorProfile.objects.create(
            user=user,
            crm='12345-SP',
            specialty='Cardiologia'
        )
        assert profile.crm == '12345-SP'
        assert profile.specialty == 'Cardiologia'
        assert str(profile).startswith('Dr(a).')
