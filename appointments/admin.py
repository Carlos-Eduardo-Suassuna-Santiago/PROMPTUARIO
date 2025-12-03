from django.contrib import admin
from .models import Appointment, AppointmentNotification, ReturnRequest

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'scheduled_date', 'scheduled_time', 'status']
    list_filter = ['status', 'appointment_type', 'scheduled_date']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name']
    raw_id_fields = ['patient', 'doctor', 'created_by']
    date_hierarchy = 'scheduled_date'

@admin.register(AppointmentNotification)
class AppointmentNotificationAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'notification_type', 'sent_at', 'is_read']
    list_filter = ['notification_type', 'is_read']
    raw_id_fields = ['appointment']

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'status', 'created_at']
    list_filter = ['status']
    raw_id_fields = ['original_appointment', 'patient', 'doctor', 'requested_by', 'new_appointment']
