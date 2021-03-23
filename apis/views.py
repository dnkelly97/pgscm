from django.shortcuts import render, redirect
from .models import *
from .decorators import admin_api_func
from .forms import CreateForm

@admin_api_func
def apis(request):
    keys = APIKey.objects.order_by('-created')
    context = {'keys': keys}
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