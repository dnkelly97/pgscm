from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

class Pipeline(models.Model):
    name = models.CharField(max_length=60, unique=True)
    num_stages = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )


class SavedQuery(models.Model):
    name = models.CharField(max_length=60, unique=True)

