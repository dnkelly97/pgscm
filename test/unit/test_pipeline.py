import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestPipelineViews:

    @pytest.mark.django_db
    def test_dashboard_view(self, logged_in_client):
        url = reverse('dashboard')
        response = logged_in_client.get(url)
        assertTemplateUsed(response, 'dashboard.html')

    def test_delete_pipeline_view(self):
        pass

    def test_delete_saved_query_view(self):
        pass


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'query_name')
        assert hasattr(SavedQuery, 'description')
        assert hasattr(SavedQuery, 'query')
