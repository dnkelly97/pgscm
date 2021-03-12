from django.http import HttpResponse
from django.shortcuts import redirect


# Credit: https://github.com/divanov11/crash-course-CRM/blob/Part-16-User-Profile-Model/crm1_v16_use_profile/accounts
# /decorators.py

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# With more user types we can end up using this, but it might not be very useful currently

# def allowed_users(allowed_roles=None):
#     if allowed_roles is None:
#         allowed_roles = []
#
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#
#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse('ERROR: You cannot access this page')
#
#         return wrapper_func
#
#     return decorator


def admin_func(view_func):
    def wrapper_function(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('dashboard')

    return wrapper_function
