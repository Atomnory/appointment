from django.db import models
from django.contrib.auth.models import User
import datetime


class Doctor(models.Model):
    first_name = models.CharField('Doctor first name', max_length=50)
    last_name = models.CharField('Doctor last name', max_length=50)
    specialization = models.CharField('Specialization', max_length=50)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        # return f'/{self.id}'
        return "/%i" % self.id

    class Meta:
        ordering = ['last_name']


class Customer(models.Model):
    first_name = models.CharField('Customer first name', max_length=50)
    last_name = models.CharField('Customer last name', max_length=50)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return f'/profile/{self.id}'
        # return "/profile/%i" % self.id


class Appointment(models.Model):
    start_time = models.TimeField('Start time')
    end_time = models.TimeField('End time')
    date = models.DateField('Date')
    # pause_time

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def check_appointment_empty_customer(self):
        """
            True if this appointment has not customer.
            False if appointment already has customer.

            :return: Boolean
        """
        return self.user is None

    def is_outdated(self):
        """
            True if this appointment is outdated.
            False if appointment is still fresh.

            :return: Boolean
        """
        today = datetime.datetime.today()
        day = datetime.datetime.combine(self.date, self.start_time)
        return day <= today

    def is_working_day_appointment(self):
        """
            True if this appointment is in working day.
            False if appointment is in weekend.

            :return: Boolean
        """
        # function helps hide appointments on weekend
        return 0 <= self.date.weekday() <= 4

    def __str__(self):
        return str(self.start_time)

    def get_absolute_url(self):
        return f'/{self.doctor.id}/appoint/{self.id}'

    class Meta:
        ordering = ['start_time']

    check_appointment_empty_customer.boolean = True
    check_appointment_empty_customer.short_description = 'Have not customer?'

    is_outdated.boolean = True
    is_outdated.short_description = 'Is Outdated?'

    is_working_day_appointment.boolean = True
    is_working_day_appointment.short_description = 'Is in working day?'
