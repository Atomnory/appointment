from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from datetime import date
from datetime import timedelta

from .forms import AppointmentCreateFormDoctor
from .forms import AppointmentCreateFormModerator
from .models import Appointment
from .models import Moderator
from .models import Doctor
from .models import Customer


class IndexView(generic.ListView):
    model = Doctor
    template_name = 'appoint/index.html'
    context_object_name = 'doctors_list'

    def get_queryset(self):
        return Doctor.objects.all()


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = 'appoint/doctor_detail.html'
    context_object_name = 'doctor'


# def doctor_profile(request, doctor_id):
#     doctor = get_object_or_404(DoctorUser, user__pk=doctor_id)
#
#     doctor_profile_data = {
#         'doctor': doctor
#     }
#
#     return render(request, 'appoint/doctor_detail.html', doctor_profile_data)


@login_required(login_url='login')
def user_profile(request, user_pk):
    if request.user.pk == user_pk:
        customer = get_object_or_404(Customer, pk=user_pk)
        today = date.today()

        user_profile_data = {
            'title': customer.get_full_name(),
            'customer': customer,
            'appointment_list_past': customer.appointment_set.filter(date__lt=today).order_by('date'),
            'appointment_list_present': customer.appointment_set.filter(date__exact=today).order_by('start_time'),
            'appointment_list_future': customer.appointment_set.filter(date__gt=today).order_by('date')
        }

        return render(request, 'appoint/user_detail.html', user_profile_data)

    else:
        return redirect('index')


def get_today_or_next_week_monday_if_today_is_weekend():
    """
        Get today.
        If today is weekend get next week monday.

        :return: Instance of datetime.date
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
    # TODO: test if unfiltered_list is empty

    appointment_list = []   # list to return
    number_of_working_days = 5  # number days of week and index of List
    key_day_week_iso = key_day.isocalendar()[1]     # 'key_day' week of year number
    key_day_year_iso = key_day.isocalendar()[0]     # 'key_day' year number

    # add list with appoints of each day to 'appointment_list' with index = number day of week
    for elem in range(number_of_working_days):
        temp_list = []  # temporary list of each day

        for appoint in unfiltered_list:
            if appoint.date.isocalendar()[0] == key_day_year_iso and \
                    appoint.date.isocalendar()[1] == key_day_week_iso and \
                    appoint.date.weekday() == elem:
                # add appoint to 'temp_list' if 'appoint' year == 'key_day' year
                # and if 'appoint' week == 'key_day' week
                # and if 'appoint' day is working day(0-4(MON-FRI))
                temp_list.append(appoint)

        # add temp_list to appointment_list with index = number day of week
        appointment_list.append(temp_list)

    return appointment_list


def does_doctor_have_any_appoint_on_week(*, key_day, doctor_pk):
    """
        Return True if doctor have although one appointment on 'key_day' week.
            False if doctor have not any.
            None if doctor with 'doctor_id' does not exist.

        :param key_day: Instance of datetime.date
        :param doctor_pk: id of Instance of Doctor
        :return: Boolean or None
    """
    key_day_week_iso = key_day.isocalendar()[1]  # 'key_day' week of year number
    key_day_year_iso = key_day.isocalendar()[0]  # 'key_day' year number

    try:
        doctor = Doctor.objects.get(pk=doctor_pk)
    except Doctor.DoesNotExist:
        return None

    prev_week_key_day = key_day - timedelta(days=7)
    appoints = doctor.appointment_set.filter(date__gte=prev_week_key_day)

    if appoints:
        for appoint in appoints:
            if appoint.date.isocalendar()[0] == key_day_year_iso and \
                    appoint.date.isocalendar()[1] == key_day_week_iso and \
                    appoint.is_working_day_appointment():
                return True

    return False


def doctor_appoints(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)    # 404 if doctor doesn't exist

    today = get_today_or_next_week_monday_if_today_is_weekend()     # get today from func
    unfiltered_list = doctor.appointment_set.order_by('start_time')  # sort appoints by 'start_time'
    # get filtered list from func
    appoint_list = get_filtered_appoint_list(key_day=today, unfiltered_list=unfiltered_list)

    # get info about 'Next week' button for 'appoint.html'
    next_week_day = today + timedelta(days=7)
    is_next_week_appoint_exists = does_doctor_have_any_appoint_on_week(key_day=next_week_day, doctor_pk=doctor_pk)
    if is_next_week_appoint_exists is None:
        raise Http404('Doctor suddenly does not exist.')

    doctor_appoint_data = {
        'title': doctor.get_full_name(),
        'doctor_name': doctor.get_full_name(),
        'doctor_pk': doctor_pk,
        'today': today,
        'next_week': next_week_day,
        'is_nw_app_exists': is_next_week_appoint_exists,
        'appoints_list': appoint_list,
    }

    return render(request, 'appoint/appoint.html', doctor_appoint_data)


def doctor_appoints_with_day(request, doctor_pk, new_day):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)  # 404 if doctor doesn't exist

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
            return redirect('doctor_appoints', doctor_pk=doctor_pk)
        elif today_week_iso < day_week_iso:
            today = day
        elif today_week_iso > day_week_iso:
            raise Http404('Appoints in the past does not exist')
    elif today_year_iso < day_year_iso:
        today = day
    elif today_year_iso > day_year_iso:
        raise Http404('Appoints in the past does not exist')

    # sort appoints by 'start_time'
    unfiltered_list = doctor.appointment_set.order_by('start_time')
    # get filtered list from func
    appoint_list = get_filtered_appoint_list(key_day=today, unfiltered_list=unfiltered_list)

    # get info about 'Prev week' button and 'Next week' button for 'appoint_with_day.html'
    prev_week_day = today - timedelta(days=7)
    next_week_day = today + timedelta(days=7)
    is_prev_week_appoint_exists = does_doctor_have_any_appoint_on_week(key_day=prev_week_day, doctor_pk=doctor_pk)
    is_next_week_appoint_exists = does_doctor_have_any_appoint_on_week(key_day=next_week_day, doctor_pk=doctor_pk)
    if is_prev_week_appoint_exists is None or is_next_week_appoint_exists is None:
        raise Http404("Doctor suddenly does not exist.")

    doctor_appoint_with_day_data = {
        'title': doctor.get_full_name(),
        'doctor_name': doctor.get_full_name(),
        'doctor_pk': doctor_pk,
        'today': today,
        'prev_week': prev_week_day,
        'next_week': next_week_day,
        'is_pw_app_exists': is_prev_week_appoint_exists,
        'is_nw_app_exists': is_next_week_appoint_exists,
        'appoints_list': appoint_list,
    }

    return render(request, 'appoint/appoint_with_day.html', doctor_appoint_with_day_data)


def appoint_detail(request, doctor_pk, appoint_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)
    appoint = get_object_or_404(Appointment, pk=appoint_pk)

    appoint_detail_data = {
        'title': appoint.start_time,
        'appoint': appoint,
    }

    return render(request, 'appoint/appoint_detail.html', appoint_detail_data)


@login_required(login_url='login')
def make_appoint(request, doctor_pk, appoint_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)
    appoint = get_object_or_404(Appointment, pk=appoint_pk)

    make_appoint_error = ''

    if appoint.has_not_customer() and not appoint.is_outdated():
        if request.method == 'POST':
            if request.user.is_authenticated and request.user.is_customer():
                customer = get_object_or_404(Customer, pk=request.user.pk)
                appoint.customer = customer
                appoint.save()

                if not appoint.has_not_customer():
                    return redirect(reverse('appoint_detail', args=(doctor_pk, appoint_pk)))
                else:
                    make_appoint_error = 'ERROR: appointment.customer still empty'
            else:
                make_appoint_error = 'ERROR: user is not authenticated or is not Customer'
    else:
        return redirect('doctor_appoints', doctor_pk=doctor_pk)

    make_appoint_data = {
        'title': appoint.start_time,
        'appoint': appoint,
        'error_text': make_appoint_error,
        'customer': request.user
    }

    return render(request, 'appoint/make_appoint.html', make_appoint_data)


@login_required(login_url='login')
def moderator_dashboard(request):

    moderator_dashboard_data = {
        'user': request.user
    }

    if request.user.is_authenticated and request.user.is_moderator():
        return render(request, 'appoint/moderator_dashboard.html', moderator_dashboard_data)
    else:
        raise Http404("ERROR: user is not authenticated.")


@login_required(login_url='login')
def doctor_dashboard(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    doctor_dashboard_data = {
        'user': request.user
    }

    if request.user.is_authenticated and request.user.pk == doctor_pk and request.user.is_doctor():
        return render(request, 'appoint/doctor_dashboard.html', doctor_dashboard_data)
    else:
        raise Http404("ERROR: user is not authenticated.")


@login_required(login_url='login')
@permission_required('appoint.add_appointment', raise_exception=True)
def create_appoint_doctor(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)

    if request.method == 'POST' and request.user.is_doctor():
        form = AppointmentCreateFormDoctor(request.POST)
        if form.is_valid():
            appoint = form.save(commit=False)
            appoint.doctor = doctor
            appoint.save()

            return redirect('doctor_appoints', doctor_pk=doctor_pk)

        else:
            raise Http404('Form is not valid')
    else:
        form = AppointmentCreateFormDoctor()

    return render(request, 'appoint/create_appoint.html', {'form': form})


@login_required(login_url='login')
@permission_required('appoint.add_appointment', raise_exception=True)
def create_appoint_moderator(request):

    if request.method == 'POST' and request.user.is_moderator():
        form = AppointmentCreateFormModerator(request.POST)
        if form.is_valid():
            appoint = form.save()

            return redirect('doctor_appoints', doctor_pk=appoint.doctor.pk)

        else:
            raise Http404('Form is not valid')
    else:
        form = AppointmentCreateFormModerator()

    return render(request, 'appoint/create_appoint.html', {'form': form})


# TODO: combine create_appoint_doctor and create_appoint_moderator
