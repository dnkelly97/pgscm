from django.urls import path
from . import views, post_views

urlpatterns = [
    path('', views.apis, name='api'),
    path('create/', views.createAPI, name = 'create_api'),
    path('create_json/', post_views.json_view, name='create_student_json'),
    path('create_form/', post_views.form_view, name='create_student_form')
]
