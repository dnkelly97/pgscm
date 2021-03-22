from django.shortcuts import render, redirect
from .models import *
from .decorators import admin_api_func

@admin_api_func
def apis(request):
    keys = APIKey.objects.order_by('-created')
    context = {'keys': keys}
    return render(request, 'api_home.html', context)
