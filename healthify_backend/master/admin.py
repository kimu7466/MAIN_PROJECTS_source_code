from django.contrib import admin
from .models import SignedUp, Appointment, Role

# Register your models here.
admin.site.register(SignedUp)
admin.site.register(Appointment)
admin.site.register(Role)