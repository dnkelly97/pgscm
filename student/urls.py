from django.urls import path
from student.views import createPage, homePage

urlpatterns = [
    path('', homePage, name='home'),
    path('create/', createPage, name='create')
]