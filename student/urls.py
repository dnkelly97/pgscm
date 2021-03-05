from django.urls import include, path
from student.views import createPage, homePage

urlpatterns = [
    path('', homePage, name='home')
]