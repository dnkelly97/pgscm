from django.urls import path
from student.views import createPage, student
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.student, name='student'),
    path('create/', csrf_exempt(createPage), name='create'),
    path('delete_student/<str:key>', views.deleteStudent, name='delete_student'),
    path('update_student/<str:key>', views.updateStudent, name='update_student')
]