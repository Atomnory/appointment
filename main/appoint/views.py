from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.urls import reverse
from django.views import generic
from .models import Appointment
from .models import Doctor


class IndexView(generic.ListView):
    model = Doctor
    template_name = 'appoint/index.html'
    context_object_name = 'doctors_list'

    def get_queryset(self):
        return Doctor.objects.order_by('last_name')


def doctor_appoints(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    doctor_appoint_data = {
        'title': doctor.get_full_name(),
        'doctor_name': doctor.get_full_name(),
        'doctor_id': doctor_id,
        'appoints_list': doctor.appointment_set.all().order_by('start_time')
    }

    return render(request, 'appoint/appoint.html', doctor_appoint_data)


def appoint_detail(request, doctor_id, appoint_id):
    appoint = get_object_or_404(Appointment, pk=appoint_id)

    appoint_detail_data = {
        'title': appoint.start_time,
        'appoint_obj': appoint,
    }

    return render(request, 'appoint/appoint_detail.html', appoint_detail_data)


    # TODO: add a lot Appointment objects
    # TODO: display appoints in column of one day
    # TODO: display 5 column of days
