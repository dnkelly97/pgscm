from pipeline.models import Pipeline, Stage, StudentStage
from pipeline.management.dispatch.dispatch_requests import *
import json
from django.core.mail import send_mail
from django.conf import settings


def pipeline_executor():
    active_pipelines = Pipeline.objects.filter(active=True)
    for pipeline in active_pipelines:
        pipeline.load_pipeline()
        pipeline_stages = Stage.objects.filter(pipeline=pipeline.id)
        for stage in pipeline_stages:
            batch = []
            student_stages = StudentStage.objects.filter(stage=stage.id)
            for student_stage in student_stages:
                if student_stage.should_advance():
                    student_stage.advance_student()
                    batch.append(student_stage)
            if batch:
                batch_url = json.loads(dispatch_adhoc_communications_post(stage.id + 1, batch).content)
                batch_response = json.loads(dispatch_batch_get(batch_url).content)
                update_batch_with_response_info(batch, batch_response)
            # any other book keeping?


def update_batch_with_response_info(batch, batch_response):
    '''
    Updates batch of StudentStage objects to give each one a batch_id and member_id from Dispatch
    '''
    batch_id = batch_response['id']
    for member in batch_response['members']:
        for student_stage in batch:
            if student_stage.student.email == member['toAddress']:
                student_stage.batch_id = batch_id
                student_stage.member_id = member['id']
                student_stage.save()


def test_task():
    print('Test task running ...')


def deployment_test_task():
    send_mail(subject="PGSCM rate limit exceeded", message='the person who sent you this... is you from the past',
              from_email=settings.EMAIL_HOST_USER, recipient_list=['dropthehammer12@gmail.com'], fail_silently=False, auth_user=None,
              auth_password=None, connection=None, html_message=None)
