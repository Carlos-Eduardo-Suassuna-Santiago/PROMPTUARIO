from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    # Rotas para Prontuário
    path('record/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='record_detail'),
    path('appointment/<int:appointment_pk>/record/create/', views.MedicalRecordCreateView.as_view(), name='record_create'),
    path('appointment/<int:appointment_pk>/record/update/', views.MedicalRecordUpdateView.as_view(), name='record_update'),
    
    # Rotas para Receita
    path('record/<int:record_pk>/prescription/create/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    
    # Rotas para Exame
    path('record/<int:record_pk>/exam/create/', views.ExamCreateView.as_view(), name='exam_create'),
]
