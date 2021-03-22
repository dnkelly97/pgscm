from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from pipeline.views import createPage, delete_query


urlpatterns = [
    path('create/', csrf_exempt(createPage), name='create_pipeline'),
    path('delete_query/', delete_query, name="delete_query")
]
