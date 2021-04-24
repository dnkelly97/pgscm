import pytest
from apis.models import APIKey
from django.urls import reverse
from rest_framework.test import APIClient
from student.models import Student
import tempfile


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

    data = [{
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }]

    client.post(reverse('create_student_json'),
                data, format='json')

    data = [{
        'email': 'test@gmail.com',
        'first_name': 'first1',
        'last_name': 'last1'
    }]

    response = client.put(reverse('create_student_json'),
                           data, format='json')

    assert response.status_code == 200
    assert len(Student.objects.all()) == length+1


@pytest.mark.django_db
def test_student_portal_multiple_valid():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",

    )
    key = APIKey.objects.assign_key(obj)
    obj.save()

    length = len(Student.objects.all())

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = [
        {
            'email': 'test@gmail.com',
            'first_name': 'first',
            'last_name': 'last'
        },
        {
            'email': 'test1@gmail.com',
            'first_name': 'first1',
            'last_name': 'last1'
        }
    ]

    client.post(reverse('create_student_json'),
                           data, format='json')

    data = [
        {
            'email': 'test@gmail.com',
            'first_name': 'first2',
            'last_name': 'last2'
        },
        {
            'email': 'test1@gmail.com',
            'first_name': 'first12',
            'last_name': 'last12'
        }
    ]

    response = client.put(reverse('create_student_json'),
                           data, format='json')

    assert response.status_code == 200
    assert len(Student.objects.all()) == length+2


@pytest.mark.django_db
def test_student_portal_multiple_invalid():
    student = Student.objects.create(email="tester@uiowa.edu", first_name="first", last_name="second")
    student.save()
    obj = APIKey(name="tester", email="tester@uiowa.edu")

    key = APIKey.objects.assign_key(obj)
    obj.save()

    length = len(Student.objects.all())

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = [
        {
            'email': 'tester@uiowa.edu',
            'first_name': 'first',
            'last_name': 'last'
        },
        {
            'email': 'test1@gmail.com',
            'first_name': 'first1',
            'last_name': 'last1'
        }
    ]

    response = client.put(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 400
    assert len(Student.objects.all()) == length

@pytest.mark.django_db
def test_student_portal_false_api():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + '12345678.ascdfbcjashfksndascdfbcjashfksnd')

    data = [{
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }]

    response = client.put(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
def test_student_portal_no_api():
    client = APIClient()

    data = [{
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }]

    response = client.put(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, first_name, last_name, code', [
       ('test@gmail.com', 'first', 'last', 200),
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

    data = [{
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }]

    response = client.put(reverse('create_student_json'),
                           data, format='json')

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
    data = [{
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.1,
        'military': True
    }]
    client.post(reverse('create_student_json'),
                           data, format='json')

    data = [{
        'email': 'yes@gmail.com',
        'first_name': 'bozy',
        'last_name': 'saggs',
        'school_year': 'SR',
        'university': 'University of Iowa',
        'degree': 'Electrical Engineering',
        'gender': 'M',
        'country': 'US',
        'ethnicity': 'A',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.2,
        'military': True,
        'us_citizenship': False
    }]
    response = client.put(reverse('create_student_json'),
                           data, format='json')

    assert response.status_code == 200
    new_student = Student.objects.get(first_name='bozy')
    assert new_student.first_name == "bozy"
    assert new_student.last_name == "saggs"
    assert new_student.email == "yes@gmail.com"
    assert new_student.school_year == "SR"
    assert new_student.research_interests == ['AI', 'Medical Imaging', 'Art of Dance']
    assert new_student.degree == "Electrical Engineering"
    assert new_student.gpa == 4.2
    assert new_student.military
    assert new_student.gender == 'M'
    assert new_student.ethnicity == 'A'
    assert new_student.country == "US"
    assert not new_student.first_generation
    assert new_student.university == "University of Iowa"
    assert not new_student.us_citizenship


@pytest.mark.django_db()
def test_multiple_file_upload():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",
    )
    key = APIKey.objects.assign_key(obj)
    obj.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    tmp_file = tempfile.NamedTemporaryFile(suffix='.txt')
    tmp_file.write(b'plz hire me')
    tmp_file.seek(0)
    data = [{
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.1,
        'military': True,
        'resume': tmp_file
    }]
    response = client.put(reverse('create_student_json'), data, format='json')
    assert response.status_code == 400

