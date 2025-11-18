"""
Configuração do Django Admin para o app accounts.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DoctorProfile, AttendantProfile, DoctorSchedule, DoctorAbsence


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin para o modelo User."""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'cpf', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'cpf']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'cpf', 'phone', 'birth_date', 'address', 'city', 'state', 'zip_code', 'is_active_user')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'cpf', 'phone', 'birth_date', 'email')
        }),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """Admin para o modelo DoctorProfile."""
    
    list_display = ['user', 'crm', 'specialty', 'is_available']
    list_filter = ['specialty', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'crm', 'specialty']
    raw_id_fields = ['user']


@admin.register(AttendantProfile)
class AttendantProfileAdmin(admin.ModelAdmin):
    """Admin para o modelo AttendantProfile."""
    
    list_display = ['user', 'department', 'shift']
    list_filter = ['shift', 'department']
    search_fields = ['user__first_name', 'user__last_name', 'department']
    raw_id_fields = ['user']


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    """Admin para o modelo DoctorSchedule."""
    
    list_display = ['doctor', 'weekday', 'start_time', 'end_time', 'is_on_call', 'is_active']
    list_filter = ['weekday', 'is_on_call', 'is_active']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']
    raw_id_fields = ['doctor']


@admin.register(DoctorAbsence)
class DoctorAbsenceAdmin(admin.ModelAdmin):
    """Admin para o modelo DoctorAbsence."""
    
    list_display = ['doctor', 'start_datetime', 'end_datetime', 'is_full_day']
    list_filter = ['is_full_day', 'start_datetime']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name', 'reason']
    raw_id_fields = ['doctor']
    date_hierarchy = 'start_datetime'
