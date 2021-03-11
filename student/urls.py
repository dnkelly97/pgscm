from django.urls import path
from student.views import createPage, student
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', student, name='student'),
    path('create/', csrf_exempt(createPage), name='create'),
]