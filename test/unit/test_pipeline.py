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


class TestPipelineViews:

    @pytest.mark.django_db
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
        assert response_dict['html'] == render_to_string('saved_query_menu.html')

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
        assert response_dict['html'] == render_to_string('pipeline_menu.html')

    def test_delete_nonexistent_pipeline(self, rf, user):
        request = rf.get('/pipeline/delete_pipeline')
        request.user = user
        request.POST = {'csrf_token': 'fake_token', 'selected_pipeline': 'nonexistent_pipeline'}
        response = delete_pipeline(request)
        response_dict = json.loads(response.content)
        assert not response_dict['success']
        assert not response_dict['html']


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'query_name')
        assert hasattr(SavedQuery, 'description')
        assert hasattr(SavedQuery, 'query')
