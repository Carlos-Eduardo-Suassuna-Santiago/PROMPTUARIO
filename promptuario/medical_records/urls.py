from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    path('', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('create/<int:appointment_pk>/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('<int:pk>/edit/', views.MedicalRecordUpdateView.as_view(), name='medical_record_update'),
    path('<int:pk>/close/', views.MedicalRecordCloseView.as_view(), name='medical_record_close'),
]
