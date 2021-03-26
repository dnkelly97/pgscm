import pytest
from pipeline.models import Pipeline, Stage
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

    @pytest.mark.django_db
    def test_define_stages_submit_valid(self):
        self.pipeline = Pipeline.objects.create(name="gabrielspipeline", num_stages=1 )
        self.pipeline.save()
        values = {"name": "Stage 1", "stage_number": 1, "time_window": 30,
                  "advancement_condition": Stage.ConditionsForAdvancement.NONE,
                  "pipeline_id": self.pipeline.id}
        self.stage = Stage.objects.create(name="Stage 1", stage_number=1, time_window=30, pipeline_id=self.pipeline.id)
        self.stage.save()
        url = reverse('define_stages', kwargs={'pipeline_id': 43})
        self.data = {
            'name': values["name"],
            'stage_number': values["stage_number"],
            'time_window': values["time_window"],
            'advancement_condition': values["advancement_condition"],
            'pipeline_id': values["pipeline_id"]
        }
        response = self.client.post(url, data=self.data)
        assert response.status_code == 302