from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .decorators import admin_api_func
from .forms import CreateForm
from django.http import JsonResponse
from django.urls import reverse


@admin_api_func
def apis(request):
    keys = APIKey.objects.order_by('-created')

    if request.method == 'POST':
        form = CreateForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            APIKey.objects.assign_key(obj)
            obj.save()
            response = redirect('api')
            messages.success(request, 'Creation successful...')
            return response

        else:
            messages.error(request, 'Email already in system')

        context = {'keys': keys, 'form': form}
        return render(request, 'api_home.html', context)

    form = CreateForm

    context = {'keys': keys, 'form': form}
    return render(request, 'api_home.html', context)


@admin_api_func
def apiProfile(request, key):
    api_keys = APIKey.objects.order_by('-created')
    api_key = APIKey.objects.get(prefix=key)

    context = {'api_keys': api_keys, 'api_key': api_key}
    return render(request, 'api_profile.html', context)

@admin_api_func
def ajax_api_regenerate(request):
    try:
        key = APIKey.objects.get(prefix=request.POST['prefix'])
        new_key = key
        key.delete()
        APIKey.objects.assign_key(new_key)
        new_key.save()
        success = True
        url = '/apis/api_profile/'+new_key.prefix
    except APIKey.DoesNotExist:
        url = None
        success = False
    return JsonResponse({'success': success, 'url': url})

@admin_api_func
def ajax_api_delete(request):
    try:
        key = APIKey.objects.get(prefix=request.POST['prefix'])
        name = key.name
        key.delete()
        success = True
        url = '/apis/'
    except APIKey.DoesNotExist:
        url = None
        success = False
    return JsonResponse({'success': success, 'url': url})

@admin_api_func
def apiUpdate(request, key):
    api_keys = APIKey.objects.order_by('-created')
    api_key = APIKey.objects.get(prefix=key)
    email = api_key.email

    form = CreateForm(request.POST or None, instance=api_key)
    if form.is_valid():
        obj = form.save()
        if(obj.email != email):
            new_obj = obj
            obj.delete()
            APIKey.objects.assign_key(new_obj)
            new_obj.save()
            return redirect(reverse('api_profile', kwargs={'key':new_obj.prefix}))

        return redirect(reverse('api_profile', kwargs={'key':obj.prefix}))


    context = {'api_keys': api_keys, 'api_key': api_key, 'form': form}
    return render(request, 'api_update.html', context)
