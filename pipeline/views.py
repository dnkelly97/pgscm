from django.shortcuts import render, redirect
from .models import Pipeline
from .models import SavedQuery
from django.contrib.auth.decorators import login_required
from pipeline.forms import CreateForm
from django.template.loader import render_to_string
from django.http import JsonResponse
import pdb

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
    context = {'form': form, 'pipelines': pipelines}
    return render(response, 'create_pipeline.html', context)


@login_required(login_url='login')
def delete_query(request):
    try:
        SavedQuery.objects.get(query_name=request.POST['selected_query']).delete()
        context = {'saved_queries': SavedQuery.objects.all()}
        partial = render_to_string('saved_query_menu.html', context)
        success = True
    except SavedQuery.DoesNotExist:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial})


@login_required(login_url='login')
def delete_pipeline(request):
    try:
        Pipeline.objects.get(name=request.POST['selected_pipeline']).delete()
        context = {'pipelines': Pipeline.objects.all()}
        partial = render_to_string('pipeline_menu.html', context)
        success = True
    except SavedQuery.DoesNotExist:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial})
