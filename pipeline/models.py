from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
# Create your models here.
from student.models import Student
from django.contrib.postgres.fields import JSONField
import json
from pipeline.management.dispatch.dispatch_requests import *
import datetime


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
    students = models.ManyToManyField(Student, through='StudentStage')
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

    class FormOptions(models.TextChoices):
        NONE = 'None', _('None')
        DEMOGRAPHICS_FORM = 'DF', _('Demographics Form')
        RESEARCH_INTERESTS_FORM = 'RIF', _('Research Interests Form')

    form = models.CharField(max_length=4, choices=FormOptions.choices, default=FormOptions.NONE)


class StudentStage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date_joined = models.DateField()
    batch_id = models.IntegerField(blank=True, null=True)  # if form received is advancement condition, we may not need to use dispatch (?)
    member_id = models.CharField(max_length=100, blank=True)

    def email_was_read(self):
        response = json.loads(dispatch_message_get(self.member_id).content)
        try:
            if response['receiptDate']:
                return True
            return False
        except KeyError:
            return False
        # todo: I couldn't find out from the API documentation what is returned for 'receiptDate' if the email hasn't
        #  been read. I assumed the key would either not be included or the string would be empty. Both cases are
        #  supported, but if the response is different this will not work. Both cases are tested for

    def time_window_has_passed(self):
        time_passed = datetime.date.today() - self.date_joined
        days_passed = time_passed.days
        return days_passed >= self.stage.time_window

    def form_received(self):
        if self.stage.form == 'RIF':
            return self.student.submitted
        elif self.stage.form == 'DF':
            return self.student.submit_demo
        else:
            return True

