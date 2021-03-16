from django.shortcuts import render, redirect
from student.forms import CreateForm
from .models import *
from login.decorators import unauthenticated_user, admin_func
from django.contrib.auth.decorators import login_required
from .filters import StudentFilter


# Create your views here.
@login_required(login_url='login')
def createPage(response):
    students = Student.objects.all()
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
    context = {'form': form, 'students':students}
    return render(response, 'create_student.html', context)


@login_required(login_url='login')
def student(request):
    students = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=students)
    students = student_filter.qs

    context = {'students': students, 'student_filter': student_filter}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def deleteStudent(request, key):
    student = Student.objects.get(id=key)
    if request.method == "POST":
        student.delete()
        return redirect('student')

    context = {'student': student}
    return render(request, 'delete.html', context)

