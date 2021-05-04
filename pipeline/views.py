from django.shortcuts import render, redirect, reverse
from .models import Pipeline, Stage
from .models import SavedQuery
from django.contrib.auth.decorators import login_required
from pipeline.forms import CreatePipelineForm, UpdateStageForm, UpdatePipelineForm
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import JsonResponse
import pdb
from pipeline.management.dispatch.dispatch_requests import *


@login_required(login_url='/login/')
def dashboard(request):
    pipelines = Pipeline.objects.all()
    saved_queries = SavedQuery.objects.all()
    return render(request, 'dashboard.html', {'pipelines': pipelines, 'saved_queries': saved_queries})


@login_required(login_url='login')
def build_pipeline_page(request):
    context = {'form': CreatePipelineForm}
    return render(request, 'create_pipeline.html', context)


@login_required(login_url='login')
def ajax_get_stages(request):
    num_stages = int(request.GET['num_stages'])
    stage_forms = []
    templates = get_all_template_data()
    for i in range(num_stages):
        stage = Stage(name="Stage " + str(i + 1))
        stage_forms.append(UpdateStageForm(instance=stage))
    partial = render_to_string('define_stages.html', {'forms': stage_forms, 'templates': templates})
    return JsonResponse({'success': True, 'html': partial})


@login_required(login_url='login')
def create_pipeline(request):
    post = dict(request.POST)
    pipeline_info = {'name': post['name'].pop(0), 'description': post['description'][0], 'sources': post['sources'],
                     'num_stages': post['num_stages'][0]}
    pipeline_form = CreatePipelineForm(pipeline_info)
    if pipeline_form.is_valid():
        stage_errors = ""
        pipeline = pipeline_form.save()
        response = dispatch_campaign_post(pipeline.id, pipeline.name)
        # if response.status_code != 201:
        #     pipeline.delete()
        #     return JsonResponse({'success': False, 'message': 'While creating this pipeline a problem occurred with Dispatch.'})
        stages = Stage.objects.filter(pipeline=pipeline.id)
        for i in range(len(stages)):
            fields = {'name': post['name'][i], 'subject': post['subject'][i], 'stage_number': i + 1, 'time_window': post['time_window'][i],
                      'advancement_condition': post['advancement_condition'][i], 'form': post['form'][i], 'pipeline': pipeline.id}
            stage_form = UpdateStageForm(fields, instance=stages[i])
            if stage_form.is_valid():
                obj = stage_form.save()
                response = dispatch_communication_post(pipeline.id, post['subject'][i], obj.id, obj.name, obj.placeholders, obj.template_url)
                # if response.status_code != 201:
                #     pipeline.delete()
                #     return JsonResponse({'success': False, 'message': 'While creating this pipeline a problem occurred with Dispatch.'})
                values = [val for key, val in post.items() if str(i + 1)+'_' in key]
                keys = [key for key, val in post.items() if str(i + 1)+'_' in key]
                possible_new_content = jsonify_placeholders(keys, values)
                if (len(keys) == 0): #check if template was specified
                    stage_errors+="Stage "+ str(i+1) + " does not have a template selected\n"
                elif (possible_new_content == "Invalid"): #check if values were valid
                    stage_errors+="Stage "+ str(i+1) + " does not have it's template content filled out\n"
                else:
                    obj.placeholders = possible_new_content
                    obj.template_url = get_template_url(keys[0]) #only assign template if template was selected
                    obj.save()
            else:
                pipeline.delete()
                return JsonResponse({'success': False, 'message': f'Stage {i + 1} invalid'})

        if stage_errors != "": #return stage errors for templates
            pipeline.delete()
            return JsonResponse({'success': False, 'message': stage_errors})
        return JsonResponse({'success': True})
    message = ''
    for fields, error in pipeline_form.errors.items():
        if fields == 'name':
            message += "A pipeline with that name already exists\n"
        elif fields == 'num_stages':
            message += "A pipeline must have at least one stage\n"
        else:
            message += f"There was an issue with: {fields}\n"

    return JsonResponse({'success': False, 'message': message})


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


@login_required(login_url='login')
def update_pipeline_stage(request):
    try:
        pipeline = Pipeline.objects.get(name=request.POST['selected_pipeline'])
        pipeline.active = not pipeline.active
        pipeline.save()
        context = {'pipelines': Pipeline.objects.all()}
        success = True
        partial = render_to_string('pipeline_menu.html', context, request)
    except Pipeline.DoesNotExist:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial})


@login_required(login_url='login')
def update_pipeline(request, pipeline_name):
    pipeline = Pipeline.objects.get(name=pipeline_name)
    if request.method == 'GET':
        form = UpdatePipelineForm(instance=pipeline)
        return render(request, 'edit_pipeline.html', {"form": form, "pipeline_name": pipeline_name})
    elif request.method == 'POST':
        post = dict(request.POST)
        try:
            add_sources = post.pop('add_sources')
            pipeline.add_sources(add_sources)
        except KeyError:
            pass
        try:
            remove_sources = post.pop('remove_sources')
            pipeline.remove_sources(remove_sources)
        except KeyError:
            pass
        pipeline_info = {'name': post['name'][0], 'description': post['description'][0]}
        # breakpoint()
        form = UpdatePipelineForm(pipeline_info, instance=pipeline)
        if form.is_valid():
            pipeline = form.save()
            return redirect('dashboard')
        else:
            return render(request, 'edit_pipeline.html', {"form": form, "pipeline_name": pipeline_name, "message": "Pipeline name already in use."})
