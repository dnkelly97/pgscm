from pipeline.models import Pipeline, Stage, StudentStage
from pipeline.management.dispatch.dispatch_requests import *
import json


def pipeline_executor():
    active_pipelines = Pipeline.objects.filter(active=True)
    print([p.name for p in active_pipelines])
    for pipeline in active_pipelines:
        pipeline_stages = Stage.objects.filter(pipeline=pipeline.id)
        for stage in pipeline_stages:
            batch = []
            student_stages = StudentStage.objects.filter(stage=stage.id)
            print([ss.student.first_name for ss in student_stages])
            for student_stage in student_stages:
                if student_stage.should_advance():
                    student_stage.advance_student()
                    batch.append(student_stage)
            if batch:
                batch_url = json.loads(dispatch_adhoc_communications_post(stage.id + 1, batch).content)
                batch_response = json.loads(dispatch_batch_get(batch_url).content)
                update_batch_with_response_info(batch, batch_response)
                # TODO: use batch response to add batch id and member id to each student_stage in batch

            # if next stage advancement condition is form read, make sure the student's form read field gets set to false --> look at amar's code for sending form and see what steps he takes, then recreate them here
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
