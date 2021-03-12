from django.shortcuts import render
from .models import Pipeline
from .models import SavedQuery
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    pipelines = Pipeline.objects.all()
    saved_queries = SavedQuery.objects.all()
    return render(request, 'dashboard.html', {'pipelines': pipelines, 'saved_queries': saved_queries})
