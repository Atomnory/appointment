from django.contrib import admin
from .models import Doctor
from .models import Appointment
from .models import Customer


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'date')


admin.site.register(Doctor)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Customer)
