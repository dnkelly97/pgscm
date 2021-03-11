from django.shortcuts import render, redirect
from student.forms import CreateForm
from .models import *
from login.decorators import unauthenticated_user, admin_func
from django.contrib.auth.decorators import login_required
from .filters import StudentFilter


# Create your views here.
@login_required(login_url='login')
def createPage(response):
    if response.method == 'POST':
        form = CreateForm(response.POST)

        if form.is_valid():
            # Create the user
            student = form.save()

            response = redirect('student')
            return response
        context = {'form': form}
        return render(response, 'create_student.html', context)

    form = CreateForm
    context = {'form': form}
    return render(response, 'create_student.html', context)


@login_required(login_url='login')
def student(response):
    return render(response, 'home.html')


@login_required(login_url='login')
def studentList(request):
    students = Student.objects.all()

    context = {'students': students}

    return render(request, 'student_list.html', context)
