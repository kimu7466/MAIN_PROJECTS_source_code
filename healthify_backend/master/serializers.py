from rest_framework import serializers
from .models import SignedUp, Appointment, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignedUp
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
