from django.db import models
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
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def check_appointment_empty_customer(self):
        """:return: True if this appointment may be reserved. False if appointment is already reserved."""
        # if self.customer is None:
        #     return True
        # else:
        #     return False
        return self.customer is None

    def get_week_of_year(self):
        return self.date.isocalendar()[1]

    def get_day_of_week(self):
        return self.date.weekday()

    def is_outdated(self):
        """:return: True if this appointment is outdated. False if appointment is still fresh."""
        today = datetime.datetime.today()
        day = datetime.datetime.combine(self.date, self.start_time)
        return day <= today

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
