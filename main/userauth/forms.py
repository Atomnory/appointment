from django import forms
from django.contrib.auth import login
from django.contrib.auth import authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from appoint.models import DoctorUser
from django.db import transaction


# class RegisterUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

#
# class RegisterDoctorUserForm(UserCreationForm):
#     class Meta:
#         # model = DoctorUser
#         fields = ['specialization']

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_doctor = True
    #     user.save()
    #     doctor = DoctorUser.objects.create(user=user)
    #     return user
