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

    data = {
        "students": [{
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }]}

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 201
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

    data = {"students":[
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
    ]}

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 201
    assert len(Student.objects.all()) == length+2

@pytest.mark.django_db
def test_student_portal_no_students():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",

    )
    key = APIKey.objects.assign_key(obj)
    obj.save()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = {}

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 400
    assert len(Student.objects.all()) == 0

@pytest.mark.django_db
def test_student_portal_multiple_invalid():
    student = Student.objects.create(email="tester@uiowa.edu", first_name="first", last_name="second")
    student.save()
    obj = APIKey(name="tester",email="tester@uiowa.edu")

    key = APIKey.objects.assign_key(obj)
    obj.save()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = {
        "students":[
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
        ]}

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 400
    assert len(Student.objects.all()) == 1

@pytest.mark.django_db
def test_student_portal_multiple_save_valid():
    student = Student.objects.create(email="tester@uiowa.edu", first_name="first", last_name="second")
    student.save()
    obj = APIKey(name="tester",email="tester@uiowa.edu")

    key = APIKey.objects.assign_key(obj)
    obj.save()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = {
        "save_valid": True,
        "students":[
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
        ]}

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 207
    assert len(Student.objects.all()) == 2

@pytest.mark.django_db
def test_not_allowed_method():
    obj = APIKey(name="tester",email="tester@uiowa.edu")
    key = APIKey.objects.assign_key(obj)
    obj.save()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    data = {}

    response = client.get(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 405

@pytest.mark.django_db
def test_student_portal_false_api():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + '12345678.ascdfbcjashfksndascdfbcjashfksnd')

    data = [{
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }]

    response = client.post(reverse('create_student_json'),
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

    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, first_name, last_name, code, student_code', [
       ('test@gmail.com', 'first', 'last', 400, 409),
       ('hello@gmail.com', 'first', '', 400, 400),
       ('hello@gmail.com', '', 'last', 400, 400),
       ('hello3', 'first', 'last', 400, 400),
       ('', 'first', 'last', 400, 400)
   ]
)

@pytest.mark.django_db
def test_student_portal_invalid(email,first_name,last_name,code,student_code):
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

    data = {"students": [{
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }]}

    response = client.post(reverse('create_student_json'),
                           data, format='json')

    assert str(student_code) in response.content.decode("utf-8")
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
    data = {"students":[{
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'normal_gpa': 4.1,
        'military': True
    }]}
    response = client.post(reverse('create_student_json'),
                           data, format='json')
    assert response.status_code == 201
    new_student = Student.objects.get(first_name='boz')
    assert new_student.first_name == "boz"
    assert new_student.last_name == "scaggs"
    assert new_student.email == "yes@gmail.com"
    assert new_student.school_year == "SR"
    assert new_student.research_interests == ['AI', 'Medical Imaging', 'Art of Dance']
    assert new_student.degree == ""
    assert new_student.normal_gpa == 4.1
    assert new_student.military
    assert new_student.gender == 'U'
    assert new_student.ethnicity == 'U'
    assert new_student.country == ""
    assert not new_student.first_generation
    assert new_student.university == ""
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
    data = {"students":[{
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'normal_gpa': 4.1,
        'military': True,
        'resume': tmp_file
    }]}
    response = client.post(reverse('create_student_json'), data, format='json')
    assert response.status_code == 400

