from django.db import models


# Create your models here.

class Pipeline(models.Model):
    name = models.CharField(max_length=60)


class SavedQuery(models.Model):
    name = models.CharField(max_length=60)

