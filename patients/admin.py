"""
Configuração do Django Admin para o app patients.
"""

from django.contrib import admin
from .models import Patient, Allergy, Vaccine, Medication


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_type', 'created_at']
    list_filter = ['blood_type']
    search_fields = ['user__first_name', 'user__last_name', 'user__cpf']
    raw_id_fields = ['user']


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ['patient', 'allergen', 'severity', 'is_active']
    list_filter = ['severity', 'is_active']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'allergen']
    raw_id_fields = ['patient']


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['patient', 'name', 'dose', 'application_date']
    list_filter = ['application_date']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'name']
    raw_id_fields = ['patient']
    date_hierarchy = 'application_date'


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'name', 'dosage', 'frequency', 'is_active']
    list_filter = ['is_active', 'start_date']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'name']
    raw_id_fields = ['patient', 'prescribed_by']
    date_hierarchy = 'start_date'
