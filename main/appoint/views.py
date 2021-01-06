from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse
from django.http import Http404

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


def get_today_or_next_week_monday_if_today_is_weekend():
    """
        Get today.
        If today is weekend get next week monday.

        :return: instance of datetime.date
    """
    today = date.today()
    # Next code change 'today' for displaying next week if 'today' is weekend
    if today.weekday() == 5:    # weekday == 5 is saturday
        today += timedelta(days=2)  # today is increasing that it will be monday in next week
    elif today.weekday() == 6:  # weekday == 6 is sunday
        today += timedelta(days=1)

    return today


def get_filtered_appoint_list(*, key_day, unfiltered_list):
    """
        Return list with appointments from unfiltered_list which have the same week as key_day.

        :param key_day: Instance of datetime.date
        :param unfiltered_list: Instance of List of Appointments
        :return: Instance of List with nested Lists of Appointments.
        Index of List = day of week (default = 0 ... 4)
    """
    appointment_list = []   # list to return
    number_of_working_days = 5  # number days of week and index of List
    appoint_week_display = key_day.isocalendar()[1]  # number week of 'today'

    # add list with appoints of each day to 'appointment_list' with index = number day of week
    for elem in range(number_of_working_days):
        temp_list = []  # temporary list of each day
        for appoint in unfiltered_list:
            if appoint.get_week_of_year() == appoint_week_display and appoint.get_day_of_week() == elem:
                # add appoint to 'temp_list' if 'appoint' week == 'today' week
                # and if 'appoint' day is working day(0-4(MON-FRI))
                temp_list.append(appoint)
        appointment_list.append(temp_list)

    return appointment_list


def doctor_appoints(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)    # 404 if doctor doesn't exist

    today = get_today_or_next_week_monday_if_today_is_weekend()     # get today from func
    unfiltered_list = doctor.appointment_set.order_by('start_time')  # sort appoints by 'start_time'

    # get filtered list from func
    appoint_list = get_filtered_appoint_list(key_day=today, unfiltered_list=unfiltered_list)

    next_week_day = today + timedelta(days=7)

    doctor_appoint_data = {
        'title': doctor.get_full_name(),
        'doctor_name': doctor.get_full_name(),
        'doctor_id': doctor_id,
        'today': today,
        'next_week': next_week_day,
        'appoints_list': appoint_list,
    }

    return render(request, 'appoint/appoint.html', doctor_appoint_data)


def doctor_appoints_with_day(request, doctor_id, new_day):
    doctor = get_object_or_404(Doctor, pk=doctor_id)  # 404 if doctor doesn't exist

    day = date.fromisoformat(new_day)
    today = get_today_or_next_week_monday_if_today_is_weekend()

    # isocalendar()[0] return ISO-year that may be different with calendar year.
    # When ISO-year is changed ISO-week will always change.
    today_week_iso = today.isocalendar()[1]
    today_year_iso = today.isocalendar()[0]
    day_week_iso = day.isocalendar()[1]
    day_year_iso = day.isocalendar()[0]

    if today_year_iso == day_year_iso:
        if today_week_iso == day_week_iso:
            return redirect('doctor_appoints', doctor_id=doctor_id)
        elif today_week_iso < day_week_iso:
            today = day
        elif today_week_iso > day_week_iso:
            return Http404('Appoints in the past does not exist')
    elif today_year_iso < day_year_iso:
        today = day
    elif today_year_iso > day_year_iso:
        return Http404('Appoints in the past does not exist')

    prev_week_day = today - timedelta(days=7)
    next_week_day = today + timedelta(days=7)

    unfiltered_list = doctor.appointment_set.order_by('start_time')  # sort appoints by 'start_time'

    # get filtered list from func
    appoint_list = get_filtered_appoint_list(key_day=today, unfiltered_list=unfiltered_list)

    doctor_appoint_with_day_data = {
        'title': doctor.get_full_name(),
        'doctor_name': doctor.get_full_name(),
        'doctor_id': doctor_id,
        'today': today,
        'prev_week': prev_week_day,
        'next_week': next_week_day,
        'appoints_list': appoint_list,
    }

    return render(request, 'appoint/appoint_with_day.html', doctor_appoint_with_day_data)


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

    if appoint.check_appointment_empty_customer() and not appoint.is_outdated():
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
        return redirect('doctor_appoints', doctor_id=doctor_id)

    make_appoint_data = {
        'title': appoint.start_time,
        'appoint': appoint,
        'error_text': make_appoint_error,
        'form': CustomerForm()
    }

    return render(request, 'appoint/make_appoint.html', make_appoint_data)
