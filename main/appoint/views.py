from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse

from datetime import date
from datetime import timedelta

from .models import Appointment
from .models import Doctor
from .models import Customer
from .forms import CustomerForm


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

    # Next code change 'today' for displaying next week on '/<pk>/appoint' if 'today' is weekend
    if today.weekday() == 5:
        today += timedelta(days=2)
    elif today.weekday() == 6:
        today += timedelta(days=1)

    appoint_week_display = today.isocalendar()[1]   # number week of 'today'

    unsorted_list = doctor.appointment_set.order_by('start_time')   # sort appoints by 'start_time'

    # add list with appoints of each day to 'appoint_list' with index = number day of week
    for elem in range(5):   # 5 because five working days and five columns in appoint.html
        temp_list = []  # temporary list of each day
        for appoint in unsorted_list:
            if appoint.get_week_of_year() == appoint_week_display and appoint.get_day_of_week() == elem:
                # add appoint to 'temp_list' if 'appoint' week == 'today' week
                # and if 'appoint' day is working day(0-4(MON-FRI))
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
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    appoint = get_object_or_404(Appointment, pk=appoint_id)

    appoint_detail_data = {
        'title': appoint.start_time,
        'appoint': appoint,
    }

    return render(request, 'appoint/appoint_detail.html', appoint_detail_data)


def make_appoint(request, doctor_id, appoint_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    appoint = get_object_or_404(Appointment, pk=appoint_id)

    make_appoint_error = ''

    if appoint.check_appointment_empty_customer():
        if request.method == 'POST':
            form_customer = CustomerForm(request.POST)
            if form_customer.is_valid():
                appoint.customer = form_customer.save(commit=False)
                form_customer.save()
                appoint.save()

                if not appoint.check_appointment_empty_customer():
                    return redirect(reverse('appoint_detail', args=(doctor_id, appoint_id)))
                else:
                    make_appoint_error = 'ERROR: appointment.customer still empty'
            else:
                make_appoint_error = 'ERROR: form_customer is not valid'
    else:
        return redirect('appoint_detail', doctor_id=doctor_id, appoint_id=appoint_id)

    make_appoint_data = {
        'title': appoint.start_time,
        'appoint': appoint,
        'error_text': make_appoint_error,
        'form': CustomerForm()
    }

    return render(request, 'appoint/make_appoint.html', make_appoint_data)
