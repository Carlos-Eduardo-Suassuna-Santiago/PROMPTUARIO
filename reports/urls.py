from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('admin/', views.AdminReportView.as_view(), name='admin_report'),
    path('admin/pdf/', views.AdminReportPDFView.as_view(), name='admin_report_pdf'),
    path('doctor/', views.DoctorReportView.as_view(), name='doctor_report'),
    path('generate/', views.ReportGenerateView.as_view(), name='report_generate'),
    path('pdf/', views.ReportPDFView.as_view(), name='report_pdf'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
]