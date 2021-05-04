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


@pytest.fixture
def pipeline_with_sources(db):
    queries = []
    for i in range(4):
        queries.append(SavedQueryFactory.create())
    pipeline = PipelineFactory.create(name="test_pipeline_1")
    pipeline.sources.add(queries[0])
    pipeline.sources.add(queries[1])
    return pipeline


@pytest.fixture
def student_stage(db):
    pipeline = Pipeline.objects.create(name='test_pipeline', num_stages=2)
    stage1 = Stage.objects.create(name='test_stage_1', stage_number=1, pipeline=pipeline)
    stage2 = Stage.objects.create(name='test_stage_2', stage_number=2, pipeline=pipeline)
    student = Student.objects.create(first_name='harry', last_name='malkovich', email='F@gmail.com')
    student_stage = StudentStage.objects.create(student=student, stage=stage1, date_joined=datetime.date.today())
    return student_stage


@pytest.mark.django_db
class TestPipelineViews:

    def test_dashboard_view(self, logged_in_client):
        url = reverse('dashboard')
        response = logged_in_client.get(url)
        assertTemplateUsed(response, 'dashboard.html')

    def test_delete_saved_query_view(self, rf, user):
        saved_query = SavedQueryFactory.create()
        request = rf.get('/pipeline/delete_query')
        request.user = user
        request.POST = {'csrf_token': 'fake_token', 'selected_query': saved_query.query_name}
        response = delete_query(request)
        try:
            SavedQuery.objects.get(query_name=saved_query.query_name)
            assert False
        except SavedQuery.DoesNotExist:
            assert True
        response_dict = json.loads(response.content)
        assert saved_query.query_name not in response_dict['html']

    def test_delete_nonexistent_query(self, rf, user):
        request = rf.get('/pipeline/delete_query')
        request.user = user
        request.POST = {'csrf_token': 'fake_token', 'selected_query': 'nonexistent_query'}
        response = delete_query(request)
        response_dict = json.loads(response.content)
        assert not response_dict['success']
        assert not response_dict['html']

    def test_delete_pipeline_view(self, rf, user):
        pipeline = PipelineFactory.create()
        request = rf.get('/pipeline/delete_pipeline')
        request.user = user
        request.POST = {'csrf_token': 'fake_token', 'selected_pipeline': pipeline.name}
        response = delete_pipeline(request)
        try:
            Pipeline.objects.get(name=pipeline.name)
            assert False
        except Pipeline.DoesNotExist:
            assert True
        response_dict = json.loads(response.content)
        assert pipeline.name not in response_dict['html']

    def test_delete_nonexistent_pipeline(self, rf, user):
        request = rf.get('/pipeline/delete_pipeline')
        request.user = user
        request.POST = {'csrf_token': 'fake_token', 'selected_pipeline': 'nonexistent_pipeline'}
        response = delete_pipeline(request)
        response_dict = json.loads(response.content)
        assert not response_dict['success']
        assert not response_dict['html']

    def test_ajax_get_stages(self, rf, user, httpserver,authorization_header):
        request = rf.get('/pipeline/get_stages')
        request.user = user
        request.GET = {'num_stages': 3}

        httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(["http://127.0.0.1:8001/templates/1"])
        httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json({'name': 'test'})

        response = ajax_get_stages(request)
        response_dict = json.loads(response.content)
        assert response.status_code == 200
        assert "Stage 3" in response_dict['html']
        assert "test" in response_dict['html']

    def test_create_pipeline(self, rf, user, httpserver, authorization_header):
        response = ["http://127.0.0.1:8001/campaigns/1"]
        httpserver.expect_request("/campaigns/", headers=authorization_header).respond_with_json(response)
        response = ["http://127.0.0.1:8001/communications/1"]
        httpserver.expect_request("/campaigns/233/communications", headers=authorization_header).respond_with_json(response)
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None'], 'form': ['None'], '1_content_123': ['hello']}
        response = create_pipeline(request)
        assert response.status_code == 200
        assert json.loads(response.content)['success']
        assert Pipeline.objects.get(name="pipeline name")
        assert Stage.objects.get(name='stage 1 name')
        assert Stage.objects.all().filter(name='stage 1 name')[0].placeholders == {'content': 'hello'}
        assert Stage.objects.all().filter(name='stage 1 name')[0].template_url == "http://127.0.0.1:8001/templates/123"

    def test_create_pipeline_invalid_template_input(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None'], 'form': ['None'], '1_content_123': ['']}
        response = create_pipeline(request)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert not content['success']
        assert content['message'] == "Stage 1 does not have it's template content filled out\n"

    def test_create_pipeline_no_template_selected(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None'], 'form': ['None']}
        response = create_pipeline(request)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert not content['success']
        assert content['message'] == "Stage 1 does not have a template selected\n"

    def test_create_pipeline_bad_pipeline(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['0'], 'time_window': ['30'], 'advancement_condition': ['None'], 'form': ['None']}
        response = create_pipeline(request)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert not content['success']
        assert content['message'] == "A pipeline must have at least one stage\n"
        try:
            Pipeline.objects.get(name="pipeline name")
            assert False
        except Pipeline.DoesNotExist:
            assert True

    def test_create_pipeline_bad_stage(self, rf, user, httpserver, authorization_header):
        response = ["http://127.0.0.1:8001/campaigns/1"]
        httpserver.expect_request("/campaigns/", headers=authorization_header).respond_with_json(response)
        response = ["http://127.0.0.1:8001/communications/1"]
        httpserver.expect_request("/campaigns/233/communications", headers=authorization_header).respond_with_json(response)
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['-1'], 'advancement_condition': ['None'], 'form': ['None']}
        response = create_pipeline(request)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert not content['success']
        assert content['message'] == 'Stage 1 invalid'
        try:
            Pipeline.objects.get(name="pipeline name")
            assert False
        except Pipeline.DoesNotExist:
            assert True
        try:
            Stage.objects.get(name="stage 1 name")
            assert False
        except Stage.DoesNotExist:
            assert True

    def test_build_pipeline(self, logged_in_client):
        url = reverse('build_pipeline')
        response = logged_in_client.get(url)
        assert response.status_code == 200

    def test_get_update_pipeline(self, rf, user, pipeline_with_sources):
        request = rf.get('/pipeline/edit/')
        request.user = user
        response = update_pipeline(request, pipeline_with_sources.name)
        assert response.status_code == 200
        assert pipeline_with_sources.name in str(response.content)

    def test_post_update_pipeline_with_sources_changed(self, rf, user, pipeline_with_sources):
        request = rf.post('/pipeline/edit/')
        request.user = user
        remove_sources = [str(pipeline_with_sources.sources.all()[0].id)]
        add_sources = []
        for query in SavedQuery.objects.all():
            id = str(query.id)
            if id not in remove_sources:
                add_sources.append(id)
        post = {'csrfmiddlewaretoken': ['fake_token'], 'name': [pipeline_with_sources.name], 'description': ['asdf'], 'add_sources': add_sources, 'remove_sources': remove_sources, 'update_pipeline_submit': ['']}
        request.POST = post
        response = update_pipeline(request, pipeline_with_sources.name)
        assert response.status_code == 302
        for source in add_sources:
            assert int(source) in [p.id for p in pipeline_with_sources.sources.all()]
        for source in remove_sources:
            assert int(source) not in [p.id for p in pipeline_with_sources.sources.all()]

    def test_post_update_pipeline_no_sources(self, rf, user, pipeline_with_sources):
        request = rf.post('/pipeline/edit/')
        request.user = user
        post = {'csrfmiddlewaretoken': ['fake_token'], 'name': [pipeline_with_sources.name], 'description': ['asdf'], 'update_pipeline_submit': ['']}
        request.POST = post
        response = update_pipeline(request, pipeline_with_sources.name)
        assert response.status_code == 302
        updated_pipeline = Pipeline.objects.get(name=pipeline_with_sources.name)
        assert updated_pipeline.description == 'asdf'


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'query_name')
        assert hasattr(SavedQuery, 'description')
        assert hasattr(SavedQuery, 'query')


class TestUpdatePipelineForm:

    def test_add_and_remove_field_options(self, pipeline_with_sources):
        form = UpdatePipelineForm(instance=pipeline_with_sources)
        source_query_ids = [p.id for p in pipeline_with_sources.sources.all()]
        not_source_query_ids = [q.id for q in SavedQuery.objects.all() if q.id not in source_query_ids]
        assert set([q.id for q in form.fields['add_sources'].queryset]) == set(not_source_query_ids)
        assert set([q.id for q in form.fields['remove_sources'].queryset]) == set(source_query_ids)

    def test_no_instance_raises_error(self):
        try:
            form = UpdatePipelineForm()
            assert False
        except ValueError as e:
            if e.args[0] == "No pipeline instance given":
                assert True
            else:
                assert False


class TestStudentStage:

    @pytest.mark.parametrize('receiptDate, expected', [(str(datetime.datetime.today()), True), (None, False), ("", False)])
    def test_email_was_read(self, student_stage, httpserver, authorization_header, receiptDate, expected):
        student_stage.member_id = '1a'
        response = {'receiptDate': receiptDate}
        httpserver.expect_request("/messages/" + student_stage.member_id, headers=authorization_header).respond_with_json(response)
        assert student_stage.email_was_read() == expected

    def test_time_window_has_passed(self, student_stage):
        student_stage.stage.time_window = 10
        student_stage.date_joined = datetime.date.today()
        assert not student_stage.time_window_has_passed()
        student_stage.date_joined = datetime.date(2018, 1, 12)
        assert student_stage.time_window_has_passed()

    @pytest.mark.parametrize('form, received', [('RIF', False), ('RIF', True), ('DF', False), ('DF', True), ('None', True)])
    def test_form_received(self, student_stage, form, received):
        student_stage.stage.form = form
        if form == 'RIF':
            student_stage.student.submitted = received
        elif form == 'DF':
            student_stage.student.submit_demo = received
        assert student_stage.form_received() == received

    @pytest.mark.parametrize('advancement_condition, form, form_received, email_read, time_window, last_stage, expected', [
        ('None', 'None', False, False, 0, True, False),  # last stage test
        ('None', 'None', False, False, 100, False, False),  # time window failing test
        ('None', 'None', False, False, 0, False, True),
        ('ER', 'None', False, True, 0, False, True),
        ('ER', 'None', False, False, 0, False, False),
        ('FR', 'RIF', True, False, 0, False, True),
        ('FR', 'RIF', False, False, 0, False, False),
        ('FR', 'DF', True, False, 0, False, True),
        ('FR', 'DF', False, False, 0, False, False),
    ])
    def test_should_advance(self, student_stage, httpserver, authorization_header, advancement_condition, form,
                            form_received, email_read, time_window, last_stage, expected):
        if last_stage:
            student_stage.stage.stage_number = 2
        student_stage.stage.time_window = time_window
        student_stage.stage.advancement_condition = advancement_condition
        student_stage.stage.form = form
        if form == 'RIF':
            student_stage.student.submitted = form_received
        elif form == 'DF':
            student_stage.student.submit_demo = form_received
        if advancement_condition == 'ER':
            student_stage.member_id = '1a'
            if email_read:
                response = {'receiptDate': str(datetime.datetime.today())}
            else:
                response = {}
            httpserver.expect_request("/messages/" + student_stage.member_id,
                                      headers=authorization_header).respond_with_json(response)
        assert student_stage.should_advance() == expected

    def test_advance_student(self, student_stage):
        old_stage_id = student_stage.stage.id
        student_stage.advance_student()
        assert student_stage.stage.id == old_stage_id + 1


class TestStage:

    @pytest.mark.django_db
    def test_is_last_stage_in_pipeline(self):
        pipeline = Pipeline.objects.create(name='test_pipeline', num_stages=2)
        stage1 = Stage.objects.create(name='test_stage_1', stage_number=1, pipeline=pipeline)
        stage2 = Stage.objects.create(name='test_stage_2', stage_number=2, pipeline=pipeline)
        assert not stage1.is_last_stage_in_pipeline()
        assert stage2.is_last_stage_in_pipeline()
