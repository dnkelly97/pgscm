from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import createPage


urlpatterns = [
    path('create/', csrf_exempt(createPage), name='create'),
]
