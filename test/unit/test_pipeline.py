import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def create_pipeline_1(db):
    p = Pipeline()
    p.name = "Test Pipeline 1"
    p.save()


@pytest.mark.client
class TestDashboardView:

    def test_dashboard_view(self, client):
        url = reverse('dashboard')
        response = client.get(url)
        assertTemplateUsed(response, 'dashboard.html')


@pytest.mark.django_db()
class TestPipelineModel:

    def test_name_field(self, create_pipeline_1):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')
