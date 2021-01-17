from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .forms import RegisterUserForm
from .forms import RegisterDoctorUserForm
from .forms import RegisterModeratorUserForm
from django.http import Http404
from django.contrib.auth.models import Group


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegisterUserForm()

    return render(request, 'userauth/register.html', {'form': form})


@login_required(login_url='login')
@permission_required('appoint.add_doctor', raise_exception=True)
def register_doctor(request):
    if request.method == 'POST':
        form = RegisterDoctorUserForm(request.POST)
        if form.is_valid():
            new_doctor = form.save()
            group_doctor = Group.objects.get(name='DoctorGroup')
            new_doctor.groups.add(group_doctor)
            return redirect('index')
        else:
            raise Http404('Form is not valid')
    else:
        form = RegisterDoctorUserForm()

    return render(request, 'userauth/register.html', {'form': form})


@login_required(login_url='login')
@permission_required('appoint.add_moderator', raise_exception=True)
def register_moderator(request):
    if request.method == 'POST':
        form = RegisterModeratorUserForm(request.POST)
        if form.is_valid():
            new_moderator = form.save()
            group_doctor = Group.objects.get(name='DoctorGroup')
            group_moderator = Group.objects.get(name='ModeratorGroup')
            new_moderator.groups.add(group_doctor)
            new_moderator.groups.add(group_moderator)
            return redirect('index')
        else:
            raise Http404('Form is not valid')
    else:
        form = RegisterModeratorUserForm()

    return render(request, 'userauth/register.html', {'form': form})
