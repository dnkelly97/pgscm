from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.student, name='student'),
    path('create/', views.createPage, name='create'),
    path('delete_student/<str:key>', views.deleteStudent, name='delete_student'),
    path('update_student/<str:key>', views.updateStudent, name='update_student')
]