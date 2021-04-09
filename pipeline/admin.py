from django.contrib import admin
from .models import Pipeline, SavedQuery

admin.site.register(Pipeline)
admin.site.register(SavedQuery)
