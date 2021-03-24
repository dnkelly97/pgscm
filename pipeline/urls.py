from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import ajax_create_pipeline, build_pipeline_page


urlpatterns = [
    path('build/', build_pipeline_page, name='build_pipeline'),
    #path('define_stages/<str:pk>/', views.stagedefinition),
    path('create/', ajax_create_pipeline, name='create_pipeline')
]
