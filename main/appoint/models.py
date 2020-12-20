from django.db import models


class Doctor(models.Model):
    first_name = models.CharField('Doctor first name', max_length=50)
    last_name = models.CharField('Doctor last name', max_length=50)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Appointment(models.Model):
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    # pause_time

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    customer = models.CharField('Customer name', max_length=250, blank=True)
    status = models.BooleanField('Status')

    def __str__(self):
        return str(self.start_time)

    def get_absolute_url(self):
        pass    # TODO: make f url

    class Meta:
        ordering = ['start_time']
