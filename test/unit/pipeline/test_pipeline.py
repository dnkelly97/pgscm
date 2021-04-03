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

    def test_ajax_get_stages(self, rf, user):
        request = rf.get('/pipeline/get_stages')
        request.user = user
        request.GET = {'num_stages': 3}
        response = ajax_get_stages(request)
        response_dict = json.loads(response.content)
        assert response.status_code == 200
        assert "Stage 3" in response_dict['html']

    def test_create_pipeline(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'source': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
                        'num_stages': ['1'], 'time_window': ['30'], 'advancement_condition': ['None']}
        response = create_pipeline(request)
        assert response.status_code == 200
        assert json.loads(response.content)['success']
        assert Pipeline.objects.get(name="pipeline name")
        assert Stage.objects.get(name='stage 1 name')

    def test_create_pipeline_bad_pipeline(self, rf, user):
        request = rf.get('/pipeline/create')
        request.user = user
        saved_query = SavedQueryFactory.create()
        request.POST = {'csrf_token': 'fake_token', 'source': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
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
        request.POST = {'csrf_token': 'fake_token', 'source': [str(saved_query.id)], 'name': ['pipeline name', 'stage 1 name'], 'description': [""],
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


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'query_name')
        assert hasattr(SavedQuery, 'description')
        assert hasattr(SavedQuery, 'query')
