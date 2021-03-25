from django.shortcuts import render, redirect
from django.http import QueryDict
from django.contrib import messages
from student.forms import CreateForm
from .models import *
from login.decorators import unauthenticated_user, admin_func
from django.contrib.auth.decorators import login_required
from .filters import StudentFilter
from django.http import JsonResponse
from django.template.loader import render_to_string
from pipeline.models import SavedQueryForm, SavedQuery
import pdb


# Create your views here.
@login_required(login_url='login')
def createPage(response):
    students = Student.objects.all()
    if response.method == 'POST':
        form = CreateForm(response.POST)

        if form.is_valid():
            form.save()
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
    context = {'students': students, 'student_filter': student_filter, 'save_query_form': SavedQueryForm()}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def run_saved_query(request):
    # get saved_query form db
    students = Student.objects.all()
    student_filter = StudentFilter(saved_query, queryset=students)
    students = student_filter.qs
    context = {'students': students, 'student_filter': student_filter, 'save_query_form': SavedQueryForm()}
    return render(request, 'home.html', context)



@login_required(login_url='login')
def ajax_save_query(request):
    query_fields = request.POST.copy()
    query_name = query_fields.pop('query_name')[0]
    description = query_fields.pop('description')[0]
    query_fields.pop('csrfmiddlewaretoken')
    saved_query_dict = {'query_name': query_name, 'description': description, 'query': query_fields}
    saved_query_form = SavedQueryForm(saved_query_dict)
    # breakpoint()
    if saved_query_form.is_valid():
        saved_query_form.save()
        success = True
        message = "Query successfully saved!"
    else:
        success = False
        try:
            SavedQuery.objects.get(query_name=query_name)
            message = "Save Failed - A query with this name already exists."
        except SavedQuery.DoesNotExist:
            if len(query_name) > 60:
                message = "Save Failed - Query names must be less than 60 characters in length."
            else:
                message = "Save Failed - Invalid query name."
    # breakpoint()
    response = {'success': success, 'message': message}
    return JsonResponse(response)


@login_required(login_url='login')
def deleteStudent(request, key):
    student = Student.objects.get(id=key)
    if request.method == "POST":
        student.delete()
        return redirect('student')

    context = {'student': student}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def updateStudent(request, key):
    students = Student.objects.all()
    student = Student.objects.get(id=key)
    form = CreateForm(instance=student)

    if request.method == 'POST':
        form = CreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student')

    context = {'form': form, 'students': students, 'student': student}
    return render(request, 'update_student.html', context)

