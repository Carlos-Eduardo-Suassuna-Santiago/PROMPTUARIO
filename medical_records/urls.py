from django.urls import path
from . import views
from .views import MedicalRecordQuickCreateView

app_name = 'medical_records'

urlpatterns = [
    path('record/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='record_detail'),
    path('appointment/<int:appointment_pk>/record/create/', views.MedicalRecordCreateView.as_view(), name='record_create'),
    path('appointment/<int:appointment_pk>/record/update/', views.MedicalRecordUpdateView.as_view(), name='record_update'),

    path('record/<int:record_pk>/prescription/create/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    path('record/<int:record_pk>/exam/create/', views.ExamCreateView.as_view(), name='exam_create'),

    path('', views.MedicalRecordListView.as_view(), name='medical_record_list'),

    # AQUI ESTÁ O PROBLEMA — FALTAVA O IMPORT
    path('quick-create/<int:patient_pk>/', MedicalRecordQuickCreateView.as_view(), name='medical_record_quick_create'),
]
