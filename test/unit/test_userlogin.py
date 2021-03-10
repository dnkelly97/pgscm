from django.contrib.auth.models import User
from django.test import Client
import unittest
from django.contrib.auth import get_user_model
from django.test import TestCase
import pytest
from django.urls import reverse
from django.apps import apps
from django.test import TestCase
from login.apps import LoginConfig


class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(LoginConfig.name, 'login')
        self.assertEqual(apps.get_app_config('login').name, 'login')


class SimpleTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_correct_email(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username='temporary')
        self.assertEqual(user.email, 'temporary@gmail.com')

    def test_login(self):
        self.username = 'testy' + '@gmail.com'
        self.password = 'taco1234'
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()
        c = Client()
        c.login(username=self.username, password=self.password)
        return c, user

    def test_loginPage_view(self):
        url = reverse("login")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_logoutUser_view(self):
        url = reverse("logout")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_registerPage_view(self):
        url = reverse("register")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_resetPassword_view(self):
        url = reverse("reset_password")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class HomeView(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = 'johnpass123'
        self.email = 'john@uiowa.edu'
        self.client = Client()

        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_dash(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_loggedin(self):
        self.user.is_staff = False
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('login'))
        assert response.status_code == 302

    def test_register(self):
        self.user.is_staff = False
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('register'))
        assert response.status_code == 302














