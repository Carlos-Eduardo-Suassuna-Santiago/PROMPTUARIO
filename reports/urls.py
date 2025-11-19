from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('doctor/', views.DoctorReportView.as_view(), name='doctor_report'),
    path('generate/', views.ReportGenerateView.as_view(), name='report_generate'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
]
