from pipeline.models import Pipeline, Stage, StudentStage
from pipeline.management.dispatch.dispatch_requests import *


def pipeline_executor():
    active_pipelines = Pipeline.objects.filter(active=True)
    print([p.name for p in active_pipelines])
    for pipeline in active_pipelines:
        pipeline_stages = Stage.objects.filter(pipeline=pipeline.id)
        for stage in pipeline_stages:
            batch = []
            student_stages = StudentStage.objects.filter(stage=stage.id)
            print([ss.student.name for ss in student_stages])
            for student_stage in student_stages:
                pass
                # check if student has met advancement conditions
                # if so, add to batch
            # send batch
            # get batch and update each student's member id in the student_stage
            # for each student in batch, update their student_stage relationship to
            # advance to next stage... anything else need to be updated?
            # if next stage advancement condition is form read, make sure the student's form read field gets set to false
