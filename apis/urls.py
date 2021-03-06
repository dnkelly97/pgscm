from django.urls import path
from . import views, post_views

urlpatterns = [
    path('', views.apis, name='api'),
    path('create/', views.apis, name='create_api'),
    path('api_profile/<str:key>', views.apiProfile, name='api_profile'),
    path('regenerate_api/', views.ajax_api_regenerate, name='regenerate_api'),
    path('delete_api/', views.ajax_api_delete, name='delete_api'),
    path('api_profile/<str:key>/update', views.apiUpdate, name='update_api'),
    path('create_json/', post_views.CreateStudents.json_view, name='create_student_json'),
    path('create_form/', post_views.CreateStudents.form_view, name='create_student_form'),
    path('execute_pipeline/', post_views.execute_pipeline, name='execute_pipeline'),
]
