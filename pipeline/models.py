from django.db import models
from django.forms import ModelForm

# Create your models here.

class Pipeline(models.Model):
    name = models.CharField(max_length=60, unique=True)


class SavedQuery(models.Model):
    query_name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    query = models.JSONField(null=True)


class SavedQueryForm(ModelForm):
    class Meta:
        model = SavedQuery
        fields = ['query_name', 'description', 'query']



