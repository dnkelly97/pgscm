import pytest
from pipeline.models import Pipeline, SavedQuery


@pytest.fixture
def create_pipeline_1(db):
    p = Pipeline()
    p.name = "Test Pipeline 1"
    p.save()


class TestDashboardView:

    def test_dashboard(self):
        pass


@pytest.mark.django_db()
class TestPipelineModel:

    def test_name_field(self, create_pipeline_1):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')