from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
# Create your models here.
from student.models import Student


class SavedQuery(models.Model):
    query_name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    query = models.JSONField(null=True)

    def __str__(self):
        return self.query_name


class Pipeline(models.Model):
    source = models.ForeignKey(SavedQuery, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
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


class SavedQueryForm(ModelForm):
    class Meta:
        model = SavedQuery
        fields = ['query_name', 'description', 'query']


class Stage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
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

    class ConditionsForAdvancement(models.TextChoices):
        NONE = 'None', _('None')
        EMAIL_READ = 'ER', _('Email Read')
        FORM_RECEIVED = 'FR', _('Form Received')

    advancement_condition = models.CharField(
        max_length=100,
        choices=ConditionsForAdvancement.choices,
        default=ConditionsForAdvancement.NONE
    )

