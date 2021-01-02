from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from datetime import date
from datetime import timedelta
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
    doctor = get_object_or_404(Doctor, pk=doctor_id)    # 404 if doctor doesn't exist

    appoint_list = []
    today = date.today()

    # Next code change today for displaying next week on '/<pk>/appoint' if today weekend
    if today.weekday() == 5:
        today += timedelta(days=2)
    elif today.weekday() == 6:
        today += timedelta(days=1)

    appoint_week_display = today.isocalendar()[1]

    unsorted_list = doctor.appointment_set.order_by('start_time')
    for elem in range(5):
        temp_list = []
        for appoint in unsorted_list:
            if appoint.get_week_of_year() == appoint_week_display and appoint.get_day_of_week() == elem:
                temp_list.append(appoint)

        appoint_list.append(temp_list)

    doctor_appoint_data = {
        'title': doctor.get_full_name(),
        'doctor_name': doctor.get_full_name(),
        'doctor_id': doctor_id,
        'today': today,
        'appoint_week_display': appoint_week_display,
        'appoints_list': appoint_list,
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
