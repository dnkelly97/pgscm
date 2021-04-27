from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
# Create your models here.
from student.models import Student
from django.contrib.postgres.fields import JSONField


class SavedQuery(models.Model):
    query_name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    query = models.JSONField(null=True)

    def __str__(self):
        return self.query_name


class Pipeline(models.Model):
    sources = models.ManyToManyField(SavedQuery, blank=True, null=True, default=None)
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    num_stages = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    active = models.BooleanField(default=False)

    def add_sources(self, source_list):
        for source_str in source_list:
            self.add_source(int(source_str))

    def remove_sources(self, source_list, boot_current_members=False):
        for source_str in source_list:
            self.remove_source(int(source_str), boot_current_members)

    def add_source(self, source_id):
        self.sources.add(SavedQuery.objects.get(id=source_id))

    def remove_source(self, source_id, boot_current_members=False):
        self.sources.remove(SavedQuery.objects.get(id=source_id))
        if boot_current_members:
            # todo:
            pass

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
    placeholders = models.JSONField(default=dict)
    template_url = models.CharField(max_length=55, blank=True)

    class ConditionsForAdvancement(models.TextChoices):
        NONE = 'None', _('None')
        EMAIL_READ = 'ER', _('Email Read')
        FORM_RECEIVED = 'FR', _('Form Received')

    advancement_condition = models.CharField(
        max_length=100,
        choices=ConditionsForAdvancement.choices,
        default=ConditionsForAdvancement.NONE
    )
