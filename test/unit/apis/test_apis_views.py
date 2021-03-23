import pytest
from apis.models import APIKey
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


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

    @pytest.mark.django_db
    def test_student_portal(self):
        url = reverse('api')
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_student(self):
        url = reverse('create_api')
        response = self.client.get(url)
        assert response.status_code == 200
