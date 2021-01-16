from django.contrib import admin
from .models import Appointment
# from .models import User
from .models import Doctor
from .models import Customer
from .models import Moderator


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'date', 'doctor', 'has_not_customer', 'is_outdated',
                    'is_working_day_appointment')

    list_filter = ['start_time', 'date']

    search_fields = ['start_time', 'date']


admin.site.register(Moderator)
admin.site.register(Doctor)
admin.site.register(Appointment, AppointmentAdmin)
# admin.site.register(User)
admin.site.register(Customer)
