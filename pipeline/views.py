from django.shortcuts import render, redirect, reverse
from .models import Pipeline, Stage
from .models import SavedQuery
from django.contrib.auth.decorators import login_required
from pipeline.forms import CreateForm, UpdateStageForm
from django.http import JsonResponse
from django.template.loader import render_to_string
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
def ajax_create_pipeline(request):
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


#need to test this function with bdd test
@login_required(login_url='login')
def define_stages(request, pipeline_id):
    stages = Stage.objects.filter(pipeline=pipeline_id)
    success = True
    post = dict(request.POST)
    for i in range(len(stages)):
        fields = {'name': post['name'][i],
                  'stage_number': i+1,
                  'time_window': post['time_window'][i],
                  'advancement_condition': post['advancement_condition'][i],
                  'pipeline': pipeline_id}
        form = UpdateStageForm(fields, instance=stages[i])
        if form.is_valid():
            stage = form.save()
        else:
            success = False
    return redirect(reverse('dashboard'))