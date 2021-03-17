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

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            for i in range(self.num_stages):
                Stage.objects.create(name="Stage " + str(i + 1), stage_number=i, pipeline=self,
                                     advancement_condition='none').save()


class SavedQuery(models.Model):
    name = models.CharField(max_length=60, unique=True)


class Stage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stage_number = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    time_window = models.IntegerField(
        default=30,
        validators=[
            MinValueValidator(0)
        ]
    )
    advancement_condition = models.CharField(max_length=100)
