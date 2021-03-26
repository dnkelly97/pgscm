import pytest
from apis.models import APIKey
from django.urls import reverse
from rest_framework.test import APIClient
from student.models import Student

@pytest.mark.django_db
def test_student_portal_valid():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",

    )
    key = APIKey.objects.assign_key(obj)
    obj.save()

    length = len(Student.objects.all())

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 201
    assert 1 == length+1

@pytest.mark.django_db
def test_student_portal_false_api():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + '12345678.ascdfbcjashfksndascdfbcjashfksnd')

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
def test_student_portal_no_api():
    client = APIClient()

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, first_name, last_name, code', [
       ('test@gmail.com', 'first', 'last', 400),
       ('hello@gmail.com', 'first', '', 400),
       ('hello@gmail.com', '', 'last', 400),
       ('hello3', 'first', 'last', 400),
       ('', 'first', 'last', 400)
   ]
)

@pytest.mark.django_db
def test_student_portal_invalid(email,first_name,last_name,code):
    student = Student.objects.create(email="test@gmail.com", first_name="first", last_name="second")
    student.save()
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",

    )

    key = APIKey.objects.assign_key(obj)
    obj.save()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }

    response = client.post(reverse('create_student_json'),
                           data, format='json')

    assert response.status_code == code