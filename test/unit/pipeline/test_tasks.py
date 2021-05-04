import pytest
from django.urls import reverse
from pipeline.views import *
from pytest_django.asserts import assertTemplateUsed
from django.test import TestCase, Client
from django.contrib.auth.models import User
from factories import SavedQueryFactory, PipelineFactory
from pipeline.models import Pipeline, SavedQuery, StudentStage
from student.models import Student
from django.template.loader import render_to_string
import json
from pipeline.management.dispatch.dispatch_requests import *
from pytest_httpserver import httpserver
import datetime
from pipeline.tasks import *


@pytest.fixture
def pipeline_setup(db):
    active_pipelines = Pipeline.objects.filter(active=True)
    for pipeline in active_pipelines:
        pipeline.active = False
        pipeline.save()
    pipeline = Pipeline.objects.create(name='executor pytest pipeline', num_stages=3, active=True)
    stage1 = Stage.objects.get(pipeline=pipeline.id, name='Stage 1')
    stage2 = Stage.objects.get(pipeline=pipeline.id, name='Stage 2')
    stage2.advancement_condition = 'FR'
    stage2.form = 'RIF'
    stage2.save()
    student1 = Student.objects.create(first_name='david', last_name='gilmour', email='dg@gmail.com')
    student2 = Student.objects.create(first_name='jeff', last_name='beck', email='jb@gmail.com')
    student3 = Student.objects.create(first_name='jimmy', last_name='page', email='jp@gmail.com')
    student_stage1 = StudentStage.objects.create(student=student1, stage=stage1, date_joined=datetime.date(2018, 1, 1))
    student_stage2 = StudentStage.objects.create(student=student2, stage=stage1, date_joined=datetime.date(2018, 1, 1))
    student_stage3 = StudentStage.objects.create(student=student3, stage=stage2, date_joined=datetime.date(2018, 1, 1))
    yield student_stage1, student_stage2, student_stage3


def test_pipeline_executor_dispatch_requests(pipeline_setup, httpserver, authorization_header):
    student_stage1, student_stage2, student_stage3 = pipeline_setup
    communication_id_1 = student_stage1.stage.id + 1
    communication_id_2 = student_stage3.stage.id + 1
    expected_data_1 = {
        'members': [
            {'toName': 'david gilmour', 'toAddress': 'dg@gmail.com', 'form': 'http://127.0.0.1:8001/student/research_interests/dg@gmail.com'},
            {'toName': 'jeff beck', 'toAddress': 'jb@gmail.com', 'form': 'http://127.0.0.1:8001/student/research_interests/jb@gmail.com'},
            # {'toName': 'jimmy page', 'toAddress': 'jp@gmail.com'}
        ],
        'includeBatchResponse': True
    }
    expected_data_2 = {
        'members': [
            {'toName': 'jimmy page', 'toAddress': 'jp@gmail.com'}
        ],
        'includeBatchResponse': True
    }
    batch_response_1 = {'id': '100', 'members': [
            {'toName': 'david gilmour', 'toAddress': 'dg@gmail.com', 'id': 'floyd'},
            {'toName': 'jeff beck', 'toAddress': 'jb@gmail.com', 'id': 'bird'},
            # {'toName': 'jimmy page', 'toAddress': 'jp@gmail.com', 'id': 'zep'}
        ]}
    batch_response_2 = {'id': '101', 'members': [
            {'toName': 'jimmy page', 'toAddress': 'jp@gmail.com', 'id': 'zep'}
        ]}
    httpserver.expect_request(f"/communications/{communication_id_1}/adhocs", headers=authorization_header, json=expected_data_1).respond_with_json("http://127.0.0.1:8001/batches/5")
    httpserver.expect_request("/batches/5", headers=authorization_header).respond_with_json(batch_response_1)
    httpserver.expect_request(f"/communications/{communication_id_2}/adhocs", headers=authorization_header, json=expected_data_2).respond_with_json("http://127.0.0.1:8001/batches/6")
    httpserver.expect_request("/batches/6", headers=authorization_header).respond_with_json(batch_response_2)
    pipeline_executor()
    httpserver.check_assertions()
    student_stage1 = StudentStage.objects.get(id=student_stage1.id)
    student_stage2 = StudentStage.objects.get(id=student_stage2.id)
    student_stage3 = StudentStage.objects.get(id=student_stage3.id)
    assert student_stage1.member_id == 'floyd'
    assert student_stage1.batch_id == int('100')
    assert student_stage2.member_id == 'bird'
    assert student_stage2.batch_id == int('100')
    assert student_stage3.member_id == 'zep'
    assert student_stage3.batch_id == int('101')
    assert student_stage1.stage.id == communication_id_1
    assert student_stage2.stage.id == communication_id_1
    assert student_stage3.stage.id == communication_id_2
