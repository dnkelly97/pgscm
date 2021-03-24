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
def createPage(response):
    pipelines = Pipeline.objects.all()
    pipeline_id = Pipeline.objects.all().order_by('id').last()
    if response.method == 'POST':
        if 'create_pipeline_submit' in response.POST:
            form = CreateForm(response.POST)
            if form.is_valid():
                pipeline = form.save()
                pipeline_id = pipeline.id
                stages = Stage.objects.filter(pipeline=pipeline_id)
                stageforms = []
                for i in range(len(stages)):
                    stageforms.append(UpdateStageForm(instance=stages.filter(stage_number=i).first()))
                return render(response, 'define_stages.html', {"forms": stageforms, "stages": stages})
            context = {'form': form, 'pk': pipeline_id}
            return render(response, 'create_pipeline.html', context)

        else:
            form = UpdateStageForm(response.POST)
            if form.is_valid():
                stage = form.save()
            if not form.is_valid():
                render(response, 'dashboard.html')


@login_required(login_url='login')
def build_pipeline_page(request):
    context = {'form': CreateForm}
    return render(request, 'create_pipeline.html', context)


@login_required(login_url='login')
def ajax_create_pipeline(request):
    form = CreateForm(request.POST)
    if form.is_valid():
        success = True
        pipeline = form.save()
        stages = Stage.objects.filter(pipeline=pipeline.id)
        stageforms = []
        for i in range(len(stages)):
            stageforms.append(UpdateStageForm(instance=stages.filter(stage_number=i).first()))
        partial = render_to_string('define_stages.html', {'forms': stageforms})
    else:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial, 'pipeline_id': pipeline.id})



@login_required(login_url='login')
def define_stages(request, pipeline_id):
    stages = Stage.objects.filter(pipeline=pipeline_id)
   # breakpoint()

    post_values = request.POST.copy()
 #it needs this shit earlier than it gets here (when the form is sent)
    post_values['pipeline'] = pipeline_id
    form = UpdateStageForm(post_values)#took away instance
    if form.is_valid():
        success = True
        stage = form.save()
    else:
        success = False
    return redirect(reverse('dashboard'))



# def stagedefinition(request, pk):
#     stages = Stage.objects.filter(pipeline=29)  # this 29 needs to be changed to pk at some point
#     stageforms = []
#     for i in range(len(stages)):
#         stageforms.append(UpdateStageForm(instance=stages.filter(stage_number=i).first()))
#         if stageforms[i].is_valid():
#             stage = stageforms[i].save()
#         else:
#             render(request, 'dashboard.html')
#     return render(request, 'define_stages.html', {"forms": stageforms, "formy": UpdateStageForm, "stages": stages})
