from django.urls import path
from . import views
from .patient_booking_views import (
    PatientBookingDoctorListView,
    PatientBookingAvailabilityView,
    PatientBookingConfirmView
)

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('<int:pk>/cancel/', views.AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('<int:pk>/reschedule/', views.AppointmentRescheduleView.as_view(), name='appointment_reschedule'),
    path('<int:pk>/check-in/', views.AppointmentCheckInView.as_view(), name='appointment_check_in'),
    path('<int:pk>/check-out/', views.AppointmentCheckOutView.as_view(), name='appointment_check_out'),
    path('calendar/', views.AppointmentCalendarView.as_view(), name='appointment_calendar'),
    path('api/list/', views.AppointmentListJsonView.as_view(), name='appointment_list_json'),
    
    # Patient Booking
    path('book/', PatientBookingDoctorListView.as_view(), name='patient_booking_doctors'),
    path('book/doctor/<int:doctor_id>/', PatientBookingAvailabilityView.as_view(), name='patient_booking_availability'),
    path('book/doctor/<int:doctor_id>/confirm/', PatientBookingConfirmView.as_view(), name='patient_booking_confirm'),
]
