import pytest
from student.models import Student
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from student.views import ajax_save_query
import json
from django.urls import reverse
from factories import SavedQueryFactory
from pipeline.models import SavedQuery


class StudentView(TestCase):
    def setUp(self):
        self.username = 'bob'
        self.password = 'bobpass123'
        self.email = 'bob@uiowa.edu'
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        self.factory = RequestFactory()

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
    def test_create_student_submit_invalid(self):
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
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_create_student_submit_valid(self):
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
        assert response.status_code == 200



@pytest.fixture
def user():
    username = 'bob'
    password = 'bobpass123'
    email = 'bob@uiowa.edu'
    user = User.objects.create_user(username, email, password)
    user.save()
    return user

@pytest.fixture
def saved_query():
    SavedQueryFactory.create()
#     query = {'query_name': 'Query 0', 'description': '', 'query': {'name': [''], 'school_year': [''], 'degree': [''], 'university': [''], 'gpa': [''], 'ethnicity': [''], 'gender': [''], 'country': [''], 'us_citizenship': ['unknown'], 'first_generation': ['unknown'], 'military': ['unknown']}}
#     sq = SavedQueryForm(query)
#     sq.save()

@pytest.mark.django_db
@pytest.mark.parametrize("post_dict,expected_response",
                         [({'csrfmiddlewaretoken': 'faketoken', 'name': 'andrew', 'school_year': 'FR', 'degree': '', 'university': '', 'gpa': '', 'ethnicity': '', 'gender': '', 'country': 'US', 'us_citizenship': 'true', 'first_generation': 'unknown', 'military': 'unknown', 'query_name': 'glouberman query', 'description': 'finding potential gloubermans'}, {'success': True, 'message': 'Query successfully saved!'}),
                          ({'csrfmiddlewaretoken': 'faketoken', 'name': 'andrew', 'school_year': 'FR', 'degree': '', 'university': '', 'gpa': '', 'ethnicity': '', 'gender': '', 'country': 'US', 'us_citizenship': 'true', 'first_generation': 'unknown', 'military': 'unknown', 'query_name': 'glouberman query jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj', 'description': 'finding potential gloubermans'}, {'success': False, 'message': "Save Failed - Query names must be less than 60 characters in length."}),
                          ({'csrfmiddlewaretoken': 'faketoken', 'name': 'andrew', 'school_year': 'FR', 'degree': '', 'university': '', 'gpa': '', 'ethnicity': '', 'gender': '', 'country': 'US', 'us_citizenship': 'true', 'first_generation': 'unknown', 'military': 'unknown', 'query_name': 'Query 2', 'description': 'finding potential gloubermans'}, {'success': False, 'message': "Save Failed - A query with this name already exists."}),
                          ({'csrfmiddlewaretoken': 'faketoken', 'name': 'andrew', 'school_year': 'FR', 'degree': '', 'university': '', 'gpa': '', 'ethnicity': '', 'gender': '', 'country': 'US', 'us_citizenship': 'true', 'first_generation': 'unknown', 'military': 'unknown', 'query_name': '', 'description': 'finding potential gloubermans'}, {'success': False, 'message': 'Save Failed - Invalid query name.'})
                          ])
def test_ajax_save_query(user, post_dict, expected_response):
    SavedQueryFactory.create()
    factory = RequestFactory()
    request = factory.post('/student/ajax_save_query')
    request.user = user
    post = request.POST.copy()
    post.update(post_dict)
    request.POST = post
    response = ajax_save_query(request)
    if expected_response['success']:
        SavedQuery.objects.get(query_name=post_dict['query_name'])
    assert json.loads(response.content) == expected_response

