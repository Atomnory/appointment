from django.shortcuts import render
from django.views import generic
from .models import Appointment
from .models import Doctor


class IndexView(generic.ListView):
    template_name = 'appoint/index.html'
    context_object_name = 'doctors_list'

    def get_queryset(self):
        return Doctor.objects.order_by('last_name')


class AppointView(generic.ListView):
    template_name = 'appoint/appoint.html'
    context_object_name = 'appoints_list'

    def get_queryset(self):
        return Appointment.objects.order_by('start_time')
