from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import create_pipeline_page


urlpatterns = [
    path('create/', create_pipeline_page, name='create_pipeline'),
    path('define_stages/<str:pk>/', views.stagedefinition),
]
