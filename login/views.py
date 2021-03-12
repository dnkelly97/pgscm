from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .decorators import unauthenticated_user, admin_func
from django.contrib.auth.models import Group
from student.models import Student
from student.filters import StudentFilter


# Create your views here.


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username/Password is incorrect')

    context = {}
    return render(request, 'login/login.html', context)


@admin_func
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get_or_create(name='administrator')
            group = Group.objects.get(name='administrator')
            group.user_set.add(user)

            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'login/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


