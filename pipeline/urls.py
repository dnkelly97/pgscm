from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import *


urlpatterns = [
    path('build/', build_pipeline_page, name='build_pipeline'),
    path('get_stages/', ajax_get_stages, name="get_stages"),
    path('create/', ajax_create_pipeline, name='create_pipeline'),
    path('update_stages/<str:pipeline_id>', define_stages, name='define_stages'),
    path('delete_query/', delete_query, name="delete_query"),
    path('delete_pipeline/', delete_pipeline, name="delete_pipeline"),
]
