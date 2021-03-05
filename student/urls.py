from django.urls import path
from student.views import createPage, homePage
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', homePage, name='home'),
    path('create/', csrf_exempt(createPage), name='create')
]