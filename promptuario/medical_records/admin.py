from django.contrib import admin
from .models import MedicalRecord, MedicalRecordComment, Prescription, Exam, MedicalRecordHistory

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment', 'is_closed', 'created_at']
    list_filter = ['is_closed', 'created_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name']
    raw_id_fields = ['appointment', 'patient', 'doctor']

@admin.register(MedicalRecordComment)
class MedicalRecordCommentAdmin(admin.ModelAdmin):
    list_display = ['medical_record', 'author', 'created_at']
    raw_id_fields = ['medical_record', 'author']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'created_at', 'valid_until']
    list_filter = ['created_at']
    raw_id_fields = ['medical_record', 'patient', 'doctor']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['patient', 'exam_name', 'status', 'requested_date']
    list_filter = ['status', 'exam_type']
    raw_id_fields = ['medical_record', 'patient', 'doctor']

@admin.register(MedicalRecordHistory)
class MedicalRecordHistoryAdmin(admin.ModelAdmin):
    list_display = ['medical_record', 'user', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    raw_id_fields = ['medical_record', 'user']
