from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import ajax_create_pipeline, build_pipeline_page, define_stages


urlpatterns = [
    path('build/', build_pipeline_page, name='build_pipeline'),
    path('create/', ajax_create_pipeline, name='create_pipeline'),
    path('update_stages/<str:pipeline_id>', define_stages, name='define_stages')
]
