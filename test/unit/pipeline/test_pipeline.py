import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.test import TestCase, Client
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestDashboardView(TestCase):

    def setUp(self):
        self.username = 'bob'
        self.password = 'bobpass123'
        self.email = 'bob@uiowa.edu'
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_dashboard_view(self):
        url = reverse('dashboard')
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)
        assertTemplateUsed(response, 'dashboard.html')


class TestPipelineModel:

    def test_name_field(self):
        assert hasattr(Pipeline, 'name')


class TestSavedQueryModel:

    def test_name_field(self):
        assert hasattr(SavedQuery, 'name')
