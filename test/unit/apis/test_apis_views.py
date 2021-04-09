import pytest
from apis.models import APIKey
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

class StudentView(TestCase):
    def setUp(self):
        self.username = 'bob'
        self.password = 'bobpass123'
        self.email = 'bob@uiowa.edu'
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        self.obj = APIKey(name="tester", email="tester@uiowa.edu")
        self.key = APIKey.objects.assign_key(self.obj)
        self.obj.save()

    @pytest.mark.django_db
    def test_api_portal(self):
        url = reverse('api')
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_api(self):
        url = reverse('create_api')
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_ajax_api_delete(self):
        url = reverse('delete_api')
        response = self.client.post(url, data={'prefix': self.obj.prefix})
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_ajax_api_delete_invalid(self):
        url = reverse('delete_api')
        response = self.client.post(url, data={'prefix': 'asdfasdf'})
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_ajax_api_regenerate(self):
        url = reverse('regenerate_api')
        response = self.client.post(url, data={'prefix': self.obj.prefix})
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_ajax_api_regenerate_invalid(self):
        url = reverse('regenerate_api')
        response = self.client.post(url, data={'prefix': 'asdfasdf'})
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_update_api(self):
        url = reverse('update_api', kwargs={'key':self.obj.prefix})
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_update_api(self):
        url = reverse('update_api', kwargs={'key':self.obj.prefix})
        response = self.client.post(url,json.dumps({'name':'new','email':'email@uiowa.edu'}), content_type='application/json')
        assert response.status_code == 200
