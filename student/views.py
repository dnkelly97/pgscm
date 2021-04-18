from django.shortcuts import render, redirect
from django.http import QueryDict
from django.contrib import messages
from student.forms import CreateForm, ResearchForm, EmailForm
from .models import *
from login.decorators import unauthenticated_user, admin_func
from django.contrib.auth.decorators import login_required
from .filters import StudentFilter
from django.http import JsonResponse
from django.template.loader import render_to_string
from pipeline.models import SavedQueryForm, SavedQuery
import pdb
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


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
    saved_query_dict = parse_save_query_request(request.POST)
    saved_query_form = SavedQueryForm(saved_query_dict)
    query_name = saved_query_dict['query_name']
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


def parse_save_query_request(post):
    query_fields = post.copy()
    query_name = query_fields.pop('query_name')[0]
    description = query_fields.pop('description')[0]
    query_fields.pop('csrfmiddlewaretoken')
    return {'query_name': query_name, 'description': description, 'query': query_fields}


def update_query(request, query_name):
    saved_query = SavedQuery.objects.get(query_name=query_name)
    students = Student.objects.all()
    student_filter = StudentFilter(saved_query.query, queryset=students)
    if request.method == 'POST':
        update_dict = parse_save_query_request(request.POST)
        update_form = SavedQueryForm(update_dict, instance=saved_query)
        if update_form.is_valid():
            update_form.save()
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, 'Query could not be saved because one or more fields were invalid.')
    context = {'student_filter': student_filter, 'save_query_form': SavedQueryForm(instance=saved_query),
               "query_name": query_name}
    return render(request, 'update_query.html', context)


@login_required(login_url='login')
def deleteStudent(request):
    try:
        student = Student.objects.get(id=request.POST['id'])
        student.delete()
        success = True
        url = '/student/'
    except Student.DoesNotExist:
        url = None
        success = False
    return JsonResponse({'success': success, 'url': url})

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

            context = {'students': students, 'student': student}
            return render(request, 'student_profile.html', context)

    context = {'form': form, 'students': students, 'student': student}
    return render(request, 'update_student.html', context)


@login_required(login_url='login')
def studentProfile(request, key):
    students = Student.objects.all()
    student = Student.objects.get(id=key)
    name = student.first_name
    email = student.email
    scheme = request.scheme
    host = request.get_host()

    if request.method == 'POST':
        print(student.submitted)
        student.submitted = False
        student.save()
        print(student.submitted)
        send_mail(subject='Update Request',
                  message="This is important, please update...",
                  html_message="<p> Hello " + name + ", <br><br> Please update your information within the "
                               "UIOWA database by following this link <br><br> <a href='" + scheme + "://" + host +
                               "/student/research_interests/" + email + "'> " + scheme + "://" + host +
                               "/student/research_interests/" + email + "</a></p>",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[student.email],
                  fail_silently=False)
        messages.success(request, 'Email sent...')

    context = {'students': students, 'student': student}
    return render(request, 'student_profile.html', context)


@login_required(login_url='login')
def sendEmail(request):
    students = Student.objects.all()
    scheme = request.scheme
    host = request.get_host()

    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            send_mail(subject='Submit Information',
                      message="This is important, please update...",
                      html_message="<p> Hello student, <br><br> Please submit your information within the "
                                   "UIOWA database by following this link <br><br> <a href='" + scheme + "://" + host +
                                   "/student/self_create'> " + scheme + "://" + host + "/student/self_create" + "</a></p>",
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[form.cleaned_data['from_email']],
                      fail_silently=False)
            messages.success(request, 'Email sent...')

    context = {'students': students, 'form': form}
    return render(request, 'send_email.html', context)


def form_email(response):
    if response.method == 'POST':
        form = CreateForm(response.POST)

        if form.is_valid():
            form.save()
            messages.success(response, 'Creation successful...')

            context = {'form': form}
            return render(response, 'success.html', context)

        else:
            messages.error(response, 'Email already exists...')

            context = {'form': form}
            return render(response, 'self_create_form.html', context)

    form = CreateForm
    context = {'form': form}
    return render(response, 'self_create_form.html', context)


def research_interests_form(request, key):
    student = Student.objects.get(email=key)
    form = ResearchForm(instance=student)

    if student.submitted is False:
        if request.method == 'POST':
            form = ResearchForm(request.POST, instance=student)

            if form.is_valid():
                form.save()
                student.submitted = True
                student.save()
                messages.success(request, 'Thank you for updating this...')

            context = {'form': form, 'student': student}
            return render(request, 'research_interests.html', context)

        context = {'form': form, 'student': student}
        return render(request, 'research_interests.html', context)

    else:
        return render(request, 'error.html')


