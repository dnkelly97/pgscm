from django.shortcuts import render
from .models import Pipeline
from .models import SavedQuery


# Create your views here.

def dashboard(request):
    pipelines = Pipeline.objects.all()
    saved_queries = SavedQuery.objects.all()
    return render(request, 'dashboard.html', {'pipelines': pipelines, 'saved_queries': saved_queries})
