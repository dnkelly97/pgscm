from django.urls import path
from . import views

urlpatterns = [
    path('', views.apis, name='api'),
    path('create/', views.createAPI, name = 'create_api')
]
