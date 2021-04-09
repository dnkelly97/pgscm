from django.urls import path
from . import views

urlpatterns = [
    path('', views.student, name='student'),
    path('ajax_save_query/', views.ajax_save_query, name='save_query'),
    path('create/', views.createPage, name='create_student'),
    path('delete_student/<str:key>', views.deleteStudent, name='delete_student'),
    path('update_student/<str:key>', views.updateStudent, name='update_student'),
    path('run_query/<str:query_name>', views.run_saved_query, name='run_saved_query'),
    path('student_prfile/<str:key>', views.studentProfile, name='student_profile'),
    path('update_query/<str:query_name>', views.update_query, name='update_query'),
    path('send_email', views.sendEmail, name='send_email'),
    path('self_create', views.form_email, name='self_form')
]

