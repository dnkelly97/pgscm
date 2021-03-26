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
from django.core.files.storage import FileSystemStorage


# Create your views here.
@login_required(login_url='login')
def createPage(response):
    students = Student.objects.all()
    if response.method == 'POST':
        form = CreateForm(response.POST, response.FILES)

        if form.is_valid():

            form.save()

            uploaded_image = response.FILES['profile_image'] if 'profile_image' in response.FILES else None
            uploaded_file = response.FILES['resume'] if 'resume' in response.FILES else None
            uploaded_file_1 = response.FILES['transcript'] if 'transcript' in response.FILES else None

            fs = FileSystemStorage()
            if uploaded_image:
                image = fs.save(uploaded_image.name, uploaded_image)
                fs.url(image)
            if uploaded_file:
                resume = fs.save(uploaded_file.name, uploaded_file)
                fs.url(resume)
            if uploaded_file_1:
                transcript = fs.save(uploaded_file_1.name, uploaded_file_1)
                fs.url(transcript)

            return redirect('student')

        context = {'form': form}
        return render(response, 'create_student.html', context)

    form = CreateForm
    context = {'form': form, 'students': students}
    return render(response, 'create_student.html', context)


@login_required(login_url='login')
def student(request):
    students = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=students)
    students = student_filter.qs
    context = {'students': students, 'student_filter': student_filter, 'save_query_form': SavedQueryForm()}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def run_saved_query(request, query_name):
    saved_query = SavedQuery.objects.get(query_name=query_name).query
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


def update_query(request, query_name):
    saved_query = SavedQuery.objects.get(query_name=query_name)
    students = Student.objects.all()
    student_filter = StudentFilter(saved_query.query, queryset=students)
    context = {'student_filter': student_filter, 'save_query_form': SavedQueryForm(instance=saved_query), "query_name": query_name}
    return render(request, 'update_query.html', context)


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
        form = CreateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()

            uploaded_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
            uploaded_file = request.FILES['resume'] if 'resume' in request.FILES else None
            uploaded_file_1 = request.FILES['transcript'] if 'transcript' in request.FILES else None

            fs = FileSystemStorage()
            if uploaded_image:
                image = fs.save(uploaded_image.name, uploaded_image)
                fs.url(image)
            if uploaded_file:
                resume = fs.save(uploaded_file.name, uploaded_file)
                fs.url(resume)
            if uploaded_file_1:
                transcript = fs.save(uploaded_file_1.name, uploaded_file_1)
                fs.url(transcript)

            return redirect('student')

    context = {'form': form, 'students': students, 'student': student}
    return render(request, 'update_student.html', context)


@login_required(login_url='login')
def studentProfile(request, key):
    students = Student.objects.all()
    student = Student.objects.get(id=key)

    context = {'students': students, 'student': student}
    return render(request, 'student_profile.html', context)
