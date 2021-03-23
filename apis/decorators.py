from django.http import HttpResponse
from django.shortcuts import redirect

def admin_api_func(view_func):
    def wrapper_function(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # We should
            return redirect('dashboard')

    return wrapper_function