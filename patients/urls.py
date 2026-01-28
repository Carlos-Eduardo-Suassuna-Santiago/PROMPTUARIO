from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='patient_list'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('allergies/', views.AllergyListView.as_view(), name='allergy_list'),
    path('vaccines/', views.VaccineListView.as_view(), name='vaccine_list'),
    path('medications/', views.MedicationListView.as_view(), name='medication_list'),
    path("my-record/", views.PatientDetailView.as_view(), name="my_medical_record"),
    path('api/search/', views.PatientSearchJsonView.as_view(), name='patient_search_json'),
    # Alergias
    path('<int:patient_pk>/allergy/add/', views.AllergyCreateView.as_view(), name='allergy_add'),
    # Vacinas
    path('<int:patient_pk>/vaccine/add/', views.VaccineCreateView.as_view(), name='vaccine_add'),
    # Medicamentos
    path('<int:patient_pk>/medication/add/', views.MedicationCreateView.as_view(), name='medication_add'),
]
