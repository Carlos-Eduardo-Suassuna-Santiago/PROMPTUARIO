"""
Comando para criar usuários iniciais do sistema.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile, AttendantProfile
from patients.models import Patient

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria usuários iniciais para teste do sistema'

    def handle(self, *args, **kwargs):
        # Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@promptuario.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                user_type='admin',
                cpf='000.000.000-00'
            )
            self.stdout.write(self.style.SUCCESS('✓ Administrador criado'))
        else:
            self.stdout.write(self.style.WARNING('✗ Administrador já existe'))

        # Médico
        if not User.objects.filter(username='medico').exists():
            medico = User.objects.create_user(
                username='medico',
                email='medico@promptuario.com',
                password='medico123',
                first_name='João',
                last_name='Silva',
                user_type='doctor',
                cpf='111.111.111-11',
                phone='(11) 91111-1111'
            )
            DoctorProfile.objects.create(
                user=medico,
                crm='12345-SP',
                specialty='Clínico Geral',
                salary=15000.00
            )
            self.stdout.write(self.style.SUCCESS('✓ Médico criado'))
        else:
            self.stdout.write(self.style.WARNING('✗ Médico já existe'))

        # Atendente
        if not User.objects.filter(username='atendente').exists():
            atendente = User.objects.create_user(
                username='atendente',
                email='atendente@promptuario.com',
                password='atendente123',
                first_name='Maria',
                last_name='Santos',
                user_type='attendant',
                cpf='222.222.222-22',
                phone='(11) 92222-2222'
            )
            AttendantProfile.objects.create(
                user=atendente,
                department='Recepção',
                shift='morning'
            )
            self.stdout.write(self.style.SUCCESS('✓ Atendente criado'))
        else:
            self.stdout.write(self.style.WARNING('✗ Atendente já existe'))

        # Paciente
        if not User.objects.filter(username='paciente').exists():
            paciente = User.objects.create_user(
                username='paciente',
                email='paciente@promptuario.com',
                password='paciente123',
                first_name='Carlos',
                last_name='Oliveira',
                user_type='patient',
                cpf='333.333.333-33',
                phone='(11) 93333-3333',
                birth_date='1990-01-01'
            )
            Patient.objects.create(
                user=paciente,
                blood_type='O+',
                height=175.0,
                weight=75.0
            )
            self.stdout.write(self.style.SUCCESS('✓ Paciente criado'))
        else:
            self.stdout.write(self.style.WARNING('✗ Paciente já existe'))

        self.stdout.write(self.style.SUCCESS('\n=== Usuários de Teste ==='))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Médico: medico / medico123')
        self.stdout.write('Atendente: atendente / atendente123')
        self.stdout.write('Paciente: paciente / paciente123')
