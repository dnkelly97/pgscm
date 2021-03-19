from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import createPage, defineStages


urlpatterns = [
    path('create/', csrf_exempt(createPage), name='create_pipeline'),
    path('define_stages/<str:pk>/', csrf_exempt(defineStages), name='define_stages'),
]
