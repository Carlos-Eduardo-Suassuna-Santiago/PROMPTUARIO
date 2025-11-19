from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('<int:pk>/cancel/', views.AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('<int:pk>/check-in/', views.AppointmentCheckInView.as_view(), name='appointment_check_in'),
    path('<int:pk>/check-out/', views.AppointmentCheckOutView.as_view(), name='appointment_check_out'),
    path('calendar/', views.AppointmentCalendarView.as_view(), name='appointment_calendar'),
]
