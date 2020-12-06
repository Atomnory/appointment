from django.db import models

class Appointment(models.Model):
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    # pause_time
    doctor = models.CharField('Doctor name', max_length=250)
    customer = models.CharField('Customer name', max_length=250)
    status = models.BooleanField('Status')
