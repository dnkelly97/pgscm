from django.shortcuts import render, redirect
from .models import Pipeline
from .models import SavedQuery
from django.contrib.auth.decorators import login_required
from pipeline.forms import CreateForm


# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    pipelines = Pipeline.objects.all()
    saved_queries = SavedQuery.objects.all()
    return render(request, 'dashboard.html', {'pipelines': pipelines, 'saved_queries': saved_queries})


@login_required(login_url='login')
def createPage(response):
    pipelines = Pipeline.objects.all()
    if response.method == 'POST':
        form = CreateForm(response.POST)
        if form.is_valid():
            pipeline = form.save()
            response = redirect('dashboard')
            return response
        context = {'form': form}
        return render(response, 'create_pipeline.html', context)
    form = CreateForm
    context = {'form': form, 'pipelines':pipelines}
    return render(response, 'create_pipeline.html', context)
