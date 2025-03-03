from django.urls import path
from .views import *

urlpatterns = [
    # Authentication
    path("login/", login_view, name="login_view"),
    path('api/roles/', get_roles, name='get_roles'), 
    path("signup/", signup_view, name="signup_view"),
    path("forget-password/", forget_password_view, name="forget_password_view"),
    path("otp-verification/", otp_verification_view, name="otp_verification_view"),
    path("resend-otp/", resend_otp, name="resend_otp"),
    path("logout/", logout_view, name="logout"),

    # Dashboard & Profile
    path("home/", home_view, name="home_view"),
    path("update-profile/", update_profile_view, name="update_profile_view"),

    # Doctors
    path("doctors/", all_doctors_view, name="all_doctors_view"),
    path("doctor/<int:doctor_id>/", doctor_detail_view, name="doctor_detail_view"),

    # Appointments
    path("book-appointment/", book_appointment_view, name="book_appointment_view"),
    path("my-appointments/", my_appointments, name="my_appointments"),
    path("delete-appointment/<int:appointment_id>/", delete_appointment, name="delete_appointment"),
    path("update-appointment-status/<int:appointment_id>/", update_appointment_status, name="update_appointment_status"),
]
