from django.db import models


class Doctor(models.Model):
    first_name = models.CharField('Doctor first name', max_length=50)
    last_name = models.CharField('Doctor last name', max_length=50)
    specialization = models.CharField('Specialization', max_length=50)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        # return f'/{self.id}'
        return "/%i" % self.id


class Customer(models.Model):
    first_name = models.CharField('Customer first name', max_length=50)
    last_name = models.CharField('Customer last name', max_length=50)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return f'/profile/{self.id}'
        # return "/profile/%i" % self.id


class Appointment(models.Model):
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    # pause_time

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def check_appointment_status(self):
        """:return: True if this appointment may be reserved. False if appointment is already reserved."""
        if self.customer is None:
            return True
        else:
            return False

    def __str__(self):
        return str(self.start_time)

    def get_absolute_url(self):
        return f'/{self.doctor.id}/appoints/{self.id}'

    class Meta:
        ordering = ['start_time']
