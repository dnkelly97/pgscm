import pytest
from django.urls import reverse
from pipeline.views import *
from pytest_django.asserts import assertTemplateUsed
from django.test import TestCase, Client
from django.contrib.auth.models import User
from factories import SavedQueryFactory, PipelineFactory
from pipeline.models import Pipeline, SavedQuery
from django.template.loader import render_to_string
import json
from pipeline.management.dispatch.dispatch_requests import *
from pytest_httpserver import httpserver


@pytest.fixture
def pipeline_with_sources(db):
    queries = []
    for i in range(4):
        queries.append(SavedQueryFactory.create())
    pipeline = PipelineFactory.create(name="test_pipeline_1")
    pipeline.sources.add(queries[0])
    pipeline.sources.add(queries[1])
    return pipeline


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
        httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json({'name': 'yourmom'})

        response = ajax_get_stages(request)
        response_dict = json.loads(response.content)
        assert response.status_code == 200
        assert "Stage 3" in response_dict['html']
        assert "yourmom" in response_dict['html']

    def test_create_pipeline(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None'], '1_content_123': ['hello']}
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
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None'], '1_content_123': ['']}
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
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None']}
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
                        'num_stages': ['0'], 'time_window': ['30'], 'advancement_condition': ['None']}
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

    def test_create_pipeline_bad_stage(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'sources': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['-1'], 'advancement_condition': ['None']}
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