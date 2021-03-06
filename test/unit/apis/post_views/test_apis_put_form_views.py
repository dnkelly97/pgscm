import pytest
from apis.models import APIKey
from django.urls import reverse
from student.models import Student
from rest_framework.test import APIRequestFactory, APIClient
from apis.post_views import CreateStudents
from PIL import Image
import tempfile


@pytest.mark.django_db
def test_student_portal_valid_form():
    factory = APIRequestFactory()
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",
    )
    key = APIKey.objects.assign_key(obj)
    obj.save()

    student = Student.objects.create(email="test@gmail.com", first_name="first", last_name="second")
    student.save()

    length = len(Student.objects.all())

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first1',
        'last_name': 'last1'
    }

    request = factory.put(reverse('create_student_form'),
                          data=data)

    request.META['HTTP_AUTHORIZATION'] = 'Api-Key ' + key

    response = CreateStudents.form_view(request)

    assert response.status_code == 200
    assert 1 == length


@pytest.mark.django_db
def test_student_portal_false_api():
    factory = APIRequestFactory()

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first1',
        'last_name': 'last1'
    }

    request = factory.put(reverse('create_student_form'),
                          data=data)

    request.META['HTTP_AUTHORIZATION'] = 'Api-Key ' + '12345678.ascdfbcjashfksndascdfbcjashfksnd'

    response = CreateStudents.form_view(request)

    assert response.status_code == 403


@pytest.mark.django_db
def test_student_portal_no_api():
    factory = APIRequestFactory()

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first1',
        'last_name': 'last1'
    }

    request = factory.put(reverse('create_student_form'),
                           data=data)

    response = CreateStudents.form_view(request)

    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email, first_name, last_name, code', [
        ('test@gmail.com', 'first', 'last', 200),
        ('test@gmail.com', '', 'last', 400),
        ('test@gmail.com', 'first', '', 400),
        ('hello@gmail.com', 'first', '', 404),
        ('hello@gmail.com', '', 'last', 404),
        ('hello3', 'first', 'last', 404),
        ('', 'first', 'last', 404)
    ]
)
@pytest.mark.django_db
def test_student_portal_invalid(email, first_name, last_name, code):
    factory = APIRequestFactory()

    student = Student.objects.create(email="test@gmail.com", first_name="first", last_name="second")
    student.save()
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",

    )

    key = APIKey.objects.assign_key(obj)
    obj.save()

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }

    request = factory.put(reverse('create_student_form'),
                           data=data)


    request.META['HTTP_AUTHORIZATION'] = 'Api-Key ' + key

    response = CreateStudents.form_view(request)

    assert response.status_code == code


@pytest.mark.django_db
def test_api_add_student_with_some_extended_fields():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",
    )
    key = APIKey.objects.assign_key(obj)
    obj.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)
    student = Student.objects.create(email="yes@gmail.com", first_name="boz", last_name="scaggs",
                                     school_year='SR', research_interests=['AI'], normal_gpa=4.1, military=True)
    student.save()

    data = {
        'email': 'yes@gmail.com',
        'first_name': 'bozy',
        'last_name': 'saggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Machine Learning'],
        'university': 'University of Iowa',
        'degree': 'Electrical Engineering',
        'gender': 'M',
        'country': 'US',
        'ethnicity': 'A',
        'normal_gpa': 4.2,
        'military': True,
        'us_citizenship': False
    }

    response = client.put(reverse('create_student_form'), data)

    assert response.status_code == 200
    new_student = Student.objects.get(first_name='bozy')
    assert new_student.first_name == "bozy"
    assert new_student.last_name == "saggs"
    assert new_student.email == "yes@gmail.com"
    assert new_student.school_year == "SR"
    assert new_student.research_interests == ['AI', 'Machine Learning']
    assert new_student.degree == "Electrical Engineering"
    assert new_student.normal_gpa == 4.2
    assert new_student.military
    assert new_student.gender == 'M'
    assert new_student.ethnicity == 'A'
    assert new_student.country == "US"
    assert not new_student.first_generation
    assert new_student.university == "University of Iowa"
    assert not new_student.us_citizenship

