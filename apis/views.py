from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .decorators import admin_api_func
from .forms import CreateForm


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
        partial = render_to_string('api_profile.html', context, request)
        success = True
    except APIKey.DoesNotExist:
        partial = None
        success = False
    return JsonResponse({'success': success, 'html': partial})

@admin_api_func
def apiUpdate(request, key):
    api_keys = APIKey.objects.order_by('-created')
    api_key = APIKey.objects.get(prefix=key)

    if request.method == 'POST':
        form = CreateForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            APIKey.objects.assign_key(obj)
            obj.save()
            context = {'api_keys': api_keys, 'api_key': api_key}
            response = render(request, 'api_profile.html', context)
            messages.success(request, 'Update successful...')
            return response

        else:
            messages.error(request, 'Email already in system')

        context = {'api_keys': api_keys, 'api_key': api_key, 'form': form}
        return render(request, 'api_profile.html', context)

    form = CreateForm(initial={'name': api_key.name, 'email': api_key.email, 'expiry_date': api_key.expiry_date})

    context = {'api_keys': api_keys, 'api_key': api_key, 'form': form}
    return render(request, 'api_update.html', context)
