import pytest
from pipeline.models import Pipeline
from django.test import TestCase, Client
from django.contrib.auth.models import User

from django.urls import reverse


class PipelineView(TestCase):
    def setUp(self):
        self.username = 'bob'
        self.password = 'bobpass123'
        self.email = 'bob@uiowa.edu'
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()
        self.client.login(username=self.username, password=self.password)

    @pytest.mark.django_db
    def test_build_pipeline(self):
        url = reverse('build_pipeline')
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_pipeline_submit_invalid(self):
        values = {"name": "gabrielspipeline", "num_stages": 6 }
        self.pipeline = Pipeline.objects.create(name="gabrielspipeline", num_stages=7 )
        self.pipeline.save()
        url = reverse('create_pipeline')
        self.data = {
            'name': values["name"],
            'num_stages': values["num_stages"],
        }
        response = self.client.post(url, data=self.data)
        assert response.status_code == 200
