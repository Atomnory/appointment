from .models import Appointment
from django import forms


class AppointmentCreateFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time', 'end_time', 'date']


class AppointmentCreateFormModerator(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'start_time', 'end_time', 'date']

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['first_name', 'last_name']
#         widgets = {
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'First name'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Last name'
#             })
#         }
