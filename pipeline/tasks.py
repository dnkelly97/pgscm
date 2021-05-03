from pipeline.models import Pipeline, Stage, StudentStage
from pipeline.management.dispatch.dispatch_requests import *


def pipeline_executor():
    active_pipelines = Pipeline.objects.filter(active=True)