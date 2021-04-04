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
            return response
        context = {'keys': keys, 'form': form}
        return render(request, 'create_api.html', context)

    form = CreateForm

    context = {'keys': keys, 'form': form}
    return render(request, 'api_home.html', context)

@admin_api_func
def createAPI(response):
    if response.method == 'POST':
        form = CreateForm(response.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            APIKey.objects.assign_key(obj)
            obj.save()
            response = redirect('api')
            return response
        context = {'form': form}
        return render(response, 'create_api.html', context)

    form = CreateForm
    context = {'form': form}
    return render(response, 'create_api.html', context)

@admin_api_func
def apiProfile(request, key):
    api_keys = APIKey.objects.order_by('-created')
    api_key = APIKey.objects.get(prefix=key)

    context = {'api_keys': api_keys, 'api_key': api_key}
    return render(request, 'api_profile.html', context)
