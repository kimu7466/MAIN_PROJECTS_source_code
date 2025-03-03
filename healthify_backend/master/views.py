from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .models import SignedUp, Role, Appointment
from .serializers import SignupSerializer, AppointmentSerializer, RoleSerializer

@api_view(['GET'])
def get_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup_view(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         user.set_password(request.data['password'])  # Hash password
#         user.save()
#         return Response({"message": "Signup successful"}, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     email = request.data.get("email")
#     password = request.data.get("password")
#     user = get_object_or_404(SignedUp, email=email)

#     if user.check_password(password):
#         return Response({"message": "Login successful", "role": user.role.name, "id": user.id}, status=200)
#     return Response({"error": "Invalid credentials"}, status=400)

# @api_view(['POST'])
# def book_appointment_view(request):
#     serializer = AppointmentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Appointment booked successfully"}, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['GET'])
# def all_doctors_view(request):
#     doctors = SignedUp.objects.filter(role__name="Doctor", is_activated=True)
#     serializer = SignupSerializer(doctors, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def my_appointments(request, user_id):
#     user = get_object_or_404(SignedUp, id=user_id)
#     if user.role.name == "Patient":
#         appointments = Appointment.objects.filter(patient=user)
#     else:
#         appointments = Appointment.objects.filter(doctor=user)

#     serializer = AppointmentSerializer(appointments, many=True)
#     return Response(serializer.data)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import json
from .models import SignedUp, Role, Appointment

# ✅ LOGIN VIEW
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = SignedUp.objects.get(email=email)
            if user.check_password(password):
                return JsonResponse({"message": "Login successful!", "user_id": user.id}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials!"}, status=400)
        except SignedUp.DoesNotExist:
            return JsonResponse({"error": "User not found!"}, status=400)

# ✅ SIGNUP VIEW
@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        role = get_object_or_404(Role, id=data.get("role"))
        
        user = SignedUp(
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            contact=data["contact"],
            role=role,
        )
        user.set_password(data["password"])
        user.save()

        return JsonResponse({"message": "Signup successful!"}, status=201)

# ✅ FORGOT PASSWORD
@csrf_exempt
def forget_password_view(request):
    return JsonResponse({"message": "Forgot Password logic here"})

# ✅ OTP VERIFICATION
@csrf_exempt
def otp_verification_view(request):
    return JsonResponse({"message": "OTP Verification logic here"})

# ✅ RESEND OTP
@csrf_exempt
def resend_otp(request):
    return JsonResponse({"message": "Resend OTP logic here"})

# ✅ LOGOUT
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)

# ✅ HOME VIEW (Dashboard)
@csrf_exempt
def home_view(request):
    return JsonResponse({"message": "Home Dashboard logic here"})

# ✅ GET ALL DOCTORS
@csrf_exempt
def all_doctors_view(request):
    doctors = SignedUp.objects.filter(role__name="Doctor")
    doctor_list = [{"id": doc.id, "firstname": doc.firstname, "lastname": doc.lastname, "email": doc.email} for doc in doctors]
    return JsonResponse(doctor_list, safe=False)

# ✅ GET DOCTOR DETAILS
@csrf_exempt
def doctor_detail_view(request, doctor_id):
    doctor = get_object_or_404(SignedUp, id=doctor_id, role__name="Doctor")
    data = {
        "id": doctor.id,
        "firstname": doctor.firstname,
        "lastname": doctor.lastname,
        "email": doctor.email,
        "contact": doctor.contact,
        "summary": doctor.summary,
    }
    return JsonResponse(data)

# ✅ BOOK APPOINTMENT
@csrf_exempt
def book_appointment_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        patient = get_object_or_404(SignedUp, id=data["patient"])
        doctor = get_object_or_404(SignedUp, id=data["doctor"], role__name="Doctor")

        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=data["date"],
            appointment_time=data["time"],
            status="Pending",
        )
        appointment.save()

        return JsonResponse({"message": "Appointment booked successfully!"}, status=201)

# ✅ MY APPOINTMENTS
@csrf_exempt
def my_appointments(request):
    user_id = request.GET.get("user_id")
    user = get_object_or_404(SignedUp, id=user_id)
    
    appointments = Appointment.objects.filter(patient=user)
    appointments_list = [
        {
            "id": a.id,
            "doctor": f"{a.doctor.firstname} {a.doctor.lastname}",
            "date": a.appointment_date,
            "time": a.appointment_time,
            "status": a.status,
        }
        for a in appointments
    ]
    return JsonResponse(appointments_list, safe=False)

# ✅ DELETE APPOINTMENT
@csrf_exempt
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return JsonResponse({"message": "Appointment deleted successfully!"}, status=200)

# ✅ UPDATE APPOINTMENT STATUS
@csrf_exempt
def update_appointment_status(request, appointment_id):
    if request.method == "POST":
        data = json.loads(request.body)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = data.get("status", appointment.status)
        appointment.save()
        return JsonResponse({"message": "Appointment status updated!"}, status=200)

# ✅ UPDATE PROFILE
@csrf_exempt
def update_profile_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = get_object_or_404(SignedUp, id=data["user_id"])
        
        user.firstname = data.get("firstname", user.firstname)
        user.lastname = data.get("lastname", user.lastname)
        user.contact = data.get("contact", user.contact)
        user.address = data.get("address", user.address)
        user.summary = data.get("summary", user.summary)

        user.save()
        return JsonResponse({"message": "Profile updated successfully!"}, status=200)
