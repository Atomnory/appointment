from django.contrib import admin
from .models import Doctor
from .models import Appointment

admin.site.register(Doctor)
admin.site.register(Appointment)
