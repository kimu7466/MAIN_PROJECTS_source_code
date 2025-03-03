from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(models.Model):
    DOCTOR = 'Doctor'
    PATIENT = 'Patient'

    CHOICES = [
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ]

    name = models.CharField(max_length=255, choices=CHOICES, unique=True)

    def __str__(self):
        return self.name

class SignedUp(BaseClass):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    password = models.CharField(max_length=255)  # Hashed password storage
    is_activated = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.role.name})"

class Appointment(BaseClass):
    patient = models.ForeignKey(SignedUp, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(SignedUp, on_delete=models.CASCADE, related_name="doctor_appointments")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    additional_info = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved")], default="Pending")

    def __str__(self):
        return f"Appointment with {self.doctor.firstname} on {self.appointment_date}"
