from django.contrib import admin
from .models import Doctor
from .models import Appointment
from .models import Customer

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Customer)
