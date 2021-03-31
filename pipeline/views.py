from django.shortcuts import render, redirect, reverse
from .models import Pipeline, Stage, SavedQuery
from django.contrib.auth.decorators import login_required
from pipeline.forms import CreateForm, UpdateStageForm
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import JsonResponse
import pdb

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    pipelines = Pipeline.objects.all()
    saved_queries = SavedQuery.objects.all()
    return render(request, 'dashboard.html', {'pipelines': pipelines, 'saved_queries': saved_queries})


@login_required(login_url='login')
def build_pipeline_page(request):
    context = {'form': CreateForm}
    return render(request, 'create_pipeline.html', context)


@login_required(login_url='login')
def ajax_get_stages(request):
    num_stages = int(request.GET['num_stages'])
    stage_forms = []
    for i in range(num_stages):
        stage = Stage(name="Stage " + str(i + 1))
        stage_forms.append(UpdateStageForm(instance=stage))
    partial = render_to_string('define_stages.html', {'forms': stage_forms})
    return JsonResponse({'success': True, 'html': partial})


@login_required(login_url='login')
def create_pipeline(request):
    pass


@login_required(login_url='login')
def ajax_create_pipeline(request):
    # breakpoint()
    form = CreateForm(request.POST)
    pipeline = Pipeline.objects.all().order_by('id').last()
    if form.is_valid():
        success = True
        pipeline = form.save()
        stages = Stage.objects.filter(pipeline=pipeline.id)
        stageforms = []
        for i in range(len(stages)):
            instance = stages.filter(stage_number=i).first()
            stageforms.append(UpdateStageForm(instance=instance))
        partial = render_to_string('define_stages.html', {'forms': stageforms, 'stages': stages})
    else:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial, 'pipeline_id': pipeline.id})


@login_required(login_url='login')
def define_stages(request, pipeline_id):
    stages = Stage.objects.filter(pipeline=pipeline_id)
    success = True
    post = dict(request.POST)
    for i in range(len(stages)):
        fields = {'name': post['name'][i], 'stage_number': i+1, 'time_window': post['time_window'][i], 'advancement_condition': post['advancement_condition'][i], 'pipeline': pipeline_id}
        form = UpdateStageForm(fields, instance=stages[i])
        if form.is_valid():
            stage = form.save()
        else:
            success = False
    return redirect(reverse('dashboard'))


@login_required(login_url='login')
def delete_query(request):
    try:
        SavedQuery.objects.get(query_name=request.POST['selected_query']).delete()
        context = {'saved_queries': SavedQuery.objects.all()}
        partial = render_to_string('saved_query_menu.html', context, request)
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
        partial = render_to_string('pipeline_menu.html', context, request)
        success = True
    except Pipeline.DoesNotExist:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial})
