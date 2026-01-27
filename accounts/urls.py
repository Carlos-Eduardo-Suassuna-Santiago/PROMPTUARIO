"""
URLs para o app accounts.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # User Management (Admin only)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('logs/', views.AccessLogListView.as_view(), name='access_log_list'),
    
    # Doctor Management
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/schedule/', views.DoctorScheduleView.as_view(), name='doctor_schedule'),
    path('doctors/<int:pk>/absence/', views.DoctorAbsenceCreateView.as_view(), name='doctor_absence_create'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),
    # Registration
    path('register/', views.PatientRegistrationView.as_view(), name='register'),
    path('register/patient/', views.PatientRegistrationAttendantView.as_view(), name='register_patient'),
    path('register/doctor/', views.DoctorRegistrationView.as_view(), name='register_doctor'),
    path('register/attendant/', views.AttendantRegistrationView.as_view(), name='register_attendant'),
    path('register/choice/', views.RegistrationChoiceView.as_view(), name='register_choice'),
]
