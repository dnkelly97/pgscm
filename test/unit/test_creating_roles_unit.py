from login import views
from django.urls import path
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client

path('register/', views.registerPage, name="register"),
path('', views.home, name="home")


class AdministratorView(TestCase):
    def setUp(self):
        self.username = 'bob'
        self.password = 'bobpass123'
        self.email = 'bob@uiowa.edu'
        self.client = Client()

        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_administrator_dash(self):
        self.user.is_staff = False
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_administrator_register(self):
        self.user.is_staff = False
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('register'))
        assert response.status_code == 302

    def test_administrator_logged(self):
        self.user.is_staff = False
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('login'))
        assert response.status_code == 302


class AdminView(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpass123'
        self.email = 'john@uiowa.edu'
        self.client = Client()

        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_admin_dash(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_admin_register(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('register'))
        assert response.status_code == 200

    def test_administrator_logged(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('login'))
        assert response.status_code == 302
