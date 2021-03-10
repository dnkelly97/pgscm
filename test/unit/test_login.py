from django.contrib.auth.models import User
from django.test import Client
import unittest
from django.contrib.auth import get_user_model
from django.test import TestCase
import pytest
from django.urls import reverse


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

    def test_home_view(self):
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

