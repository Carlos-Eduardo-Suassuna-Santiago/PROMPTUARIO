"""
Testes para o app patients.
"""

import pytest
from django.contrib.auth import get_user_model
from patients.models import Patient, Allergy

User = get_user_model()


@pytest.mark.django_db
class TestPatientModel:
    """Testes para o modelo Patient."""
    
    def test_create_patient(self):
        """Testa criação de paciente."""
        user = User.objects.create_user(
            username='patient',
            email='patient@test.com',
            password='patient123',
            cpf='222.222.222-22',
            user_type='patient',
            birth_date='1990-01-01'
        )
        patient = Patient.objects.create(
            user=user,
            blood_type='O+',
            height=175.0,
            weight=75.0
        )
        assert patient.blood_type == 'O+'
        assert patient.get_age() is not None


@pytest.mark.django_db
class TestAllergyModel:
    """Testes para o modelo Allergy."""
    
    def test_create_allergy(self):
        """Testa criação de alergia."""
        user = User.objects.create_user(
            username='patient2',
            email='patient2@test.com',
            password='patient123',
            cpf='333.333.333-33',
            user_type='patient'
        )
        patient = Patient.objects.create(user=user)
        allergy = Allergy.objects.create(
            patient=patient,
            allergen='Penicilina',
            severity='severe'
        )
        assert allergy.allergen == 'Penicilina'
        assert allergy.severity == 'severe'
