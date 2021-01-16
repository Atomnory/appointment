from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RegisterUserForm
from .forms import RegisterDoctorUserForm
from django.http import Http404


# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = RegisterUserForm()
#
#     return render(request, 'userauth/register.html', {'form': form})
#
#
# def register_doctor(request):
#     if request.method == 'POST':
#         form = RegisterDoctorUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         else:
#             raise Http404('From is not valid')
#     else:
#         form = RegisterDoctorUserForm()
#
#     return render(request, 'userauth/register.html', {'form': form})
