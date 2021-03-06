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
from student.filters import StudentFilter


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

    def load_pipeline(self):
        '''
        Loads eligible students into stage 0 of the pipeline. Eligible students are those returned by the pipeline's
        source queries that are not already somewhere in the pipeline
        '''
        stage0 = Stage.objects.get(pipeline=self.id, name='Stage 0')
        for source in self.sources.all():
            saved_query = source.query
            students = Student.objects.all()
            student_filter = StudentFilter(saved_query, queryset=students)
            sourced_students = student_filter.qs
            for student in sourced_students:
                student_in_pipeline = False
                for stage in Stage.objects.filter(pipeline=self.id):
                    try:
                        StudentStage.objects.get(stage=stage, student=student)
                        student_in_pipeline = True
                        break
                    except StudentStage.DoesNotExist:
                        pass
                if not student_in_pipeline:
                    StudentStage.objects.create(stage=stage0, student=student, date_joined=datetime.date.today())

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
            Stage.objects.create(name="Stage 0", stage_number=0, pipeline=self, advancement_condition='none', time_window=0)
            for i in range(self.num_stages):
                Stage.objects.create(name="Stage " + str(i + 1), stage_number=i+1, pipeline=self,
                                     advancement_condition='none').save()


class SavedQueryForm(ModelForm):
    class Meta:
        model = SavedQuery
        fields = ['query_name', 'description', 'query']


class Stage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, null=True)
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
    template_url = models.CharField(max_length=400, blank=True)

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

    def is_last_stage_in_pipeline(self):
        pipeline = Pipeline.objects.get(id=self.pipeline.id)
        return pipeline.num_stages == self.stage_number


class StudentStage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date_joined = models.DateField()
    batch_id = models.IntegerField(blank=True, null=True)  # if form received is advancement condition, we may not need to use dispatch (?)
    member_id = models.CharField(max_length=100, blank=True)

    def advance_student(self):  # IMPORTANT: This function should only be called if should_advance() has been called and evaluated to True
        next_stage_id = self.stage.id + 1
        next_stage = Stage.objects.get(id=next_stage_id)
        self.stage = next_stage
        self.member_id = ''
        self.batch_id = None
        self.date_joined = datetime.date.today()
        if self.stage.advancement_condition == 'FR':
            if self.stage.form == 'DF':
                self.student.submit_demo = False
                self.student.save()
            elif self.stage.form == 'RIF':
                self.student.submitted = False
                self.student.save()
        self.save()

    def should_advance(self):
        if self.stage.is_last_stage_in_pipeline():
            return False
        if self.time_window_has_passed():
            if self.stage.advancement_condition == 'ER':
                return self.email_was_read()
            elif self.stage.advancement_condition == 'FR':
                return self.form_received()
            else:
                return True
        return False

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

