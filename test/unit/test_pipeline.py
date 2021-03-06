import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


class TestDashboardView:

    def test_dashboard_view(self, client):
        url = reverse('dashboard')
        response = client.get(url)
        assertTemplateUsed(response, 'dashboard.html')


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'name')
