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
    # breakpoint()
    students = Student.objects.all()
    tmpd = {'name': ['mo'], 'school_year': [''], 'degree': [''], 'university': [''], 'gpa': [''], 'ethnicity': [''], 'gender': [''], 'country': [''], 'us_citizenship': ['unknown'], 'first_generation': ['unknown'], 'military': ['unknown']}
    student_filter = StudentFilter(request.GET, queryset=students)
    students = student_filter.qs
    # breakpoint()
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
        success = True
        message = "Query successfully saved!"
    else:
        success = False
        try:
            SavedQuery.objects.get(query_name=query_name)
            message = "Save Failed - A query with this name already exists."
        except SavedQuery.DoesNotExist:
            print('yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeet')
            if len(query_name) > 60:
                message = "Save Failed - Query names must be less than 60 characters in length."
            else:
                message = "Save Failed - Invalid query name."
    # breakpoint()
    response = {'success': success, 'message': message}
    return JsonResponse(response)
