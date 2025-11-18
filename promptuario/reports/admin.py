from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_by', 'created_at']
    list_filter = ['report_type', 'format', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['generated_by']
    date_hierarchy = 'created_at'
