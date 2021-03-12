import pytest
from student.models import Student
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
        self.user.save()
        self.client.login(username=self.username, password=self.password)

    @pytest.mark.django_db
    def test_student_portal(self):
        url = reverse('student')
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_student(self):
        url = reverse('create')
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_student_submit_valid(self):
        values = {"email": "hello@gmail.com", "first_name": 'first', "last_name": 'last', "school_year": Student.YearInSchool.UNKNOWN,
                  "ethnicity": Student.Ethnicity.UNKNOWN, "gender": Student.Gender.UNKNOWN}
        self.student = Student.objects.create(email="hello1@gmail.com", first_name="first", last_name="second")
        self.student.save()
        url = reverse('create')
        self.data = {
            'email': values["email"],
            'first_name': values["first_name"],
            'last_name': values["last_name"],
            'school_year': values["school_year"],
            'ethnicity': values["ethnicity"],
            'gender': values["gender"]
        }
        response = self.client.post(url, data=self.data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_student_submit_invalid(self):
        values = {"email": "hello1@gmail.com", "first_name": 'first', "last_name": 'second',
                  "school_year": Student.YearInSchool.UNKNOWN,
                  "ethnicity": Student.Ethnicity.UNKNOWN, "gender": Student.Gender.UNKNOWN}
        self.student = Student.objects.create(email="hello1@gmail.com", first_name="first", last_name="second")
        self.student.save()
        url = reverse('create')
        self.data = {
            'email': values["email"],
            'first_name': values["first_name"],
            'last_name': values["last_name"],
            'school_year': values["school_year"],
            'ethnicity': values["ethnicity"],
            'gender': values["gender"]
        }
        response = self.client.post(url, data=self.data)
        assert response.status_code == 302
