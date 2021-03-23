import pytest
from django.urls import reverse
from pipeline.views import *
from pytest_django.asserts import assertTemplateUsed
from django.test import TestCase, Client
from django.contrib.auth.models import User
from factories import SavedQueryFactory
from pipeline.models import Pipeline, SavedQuery
from django.template.loader import render_to_string
import json


class TestPipelineViews:

    @pytest.mark.django_db
    def test_dashboard_view(self, logged_in_client):
        url = reverse('dashboard')
        response = logged_in_client.get(url)
        assertTemplateUsed(response, 'dashboard.html')

    def test_delete_pipeline_view(self, rf):
        assert False

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


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'query_name')
        assert hasattr(SavedQuery, 'description')
        assert hasattr(SavedQuery, 'query')
