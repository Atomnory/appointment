from django.shortcuts import render
from django.views import generic
from .models import Appointment


class IndexView(generic.ListView):
    template_name = 'appoint/index.html'
    context_object_name = 'appoints_list'

    def get_queryset(self):
        return Appointment.objects.order_by('start_time')
