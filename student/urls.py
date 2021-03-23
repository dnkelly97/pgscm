from django.urls import path
from . import views

urlpatterns = [
    path('', views.student, name='student'),
    path('ajax_save_query/', views.ajax_save_query, name='save_query'),
    path('create/', views.createPage, name='create_student'),
    path('delete_student/<str:key>', views.deleteStudent, name='delete_student'),
    path('update_student/<str:key>', views.updateStudent, name='update_student')
]

