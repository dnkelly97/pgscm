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

    length = len(Student.objects.all())

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }

    request = factory.post(reverse('create_student_form'),
                           data=data)
    request.META['HTTP_AUTHORIZATION'] = 'Api-Key ' + key

    response = CreateStudents.form_view(request)

    assert response.status_code == 201
    assert 1 == length+1

@pytest.mark.django_db
def test_student_portal_false_api():
    factory = APIRequestFactory()

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }

    request = factory.post(reverse('create_student_form'),
                           data=data)
    request.META['HTTP_AUTHORIZATION'] = 'Api-Key ' + '12345678.ascdfbcjashfksndascdfbcjashfksnd'

    response = CreateStudents.form_view(request)

    assert response.status_code == 403

@pytest.mark.django_db
def test_student_portal_no_api():
    factory = APIRequestFactory()

    data = {
        'email': 'test@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }

    request = factory.post(reverse('create_student_form'),
                           data=data)

    response = CreateStudents.form_view(request)

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

    request = factory.post(reverse('create_student_form'),
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
    data = {
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.1,
        'military': True
    }
    response = client.post(reverse('create_student_form'), data)
    assert response.status_code == 201
    new_student = Student.objects.get(first_name='boz')
    assert new_student.first_name == "boz"
    assert new_student.last_name == "scaggs"
    assert new_student.email == "yes@gmail.com"
    assert new_student.school_year == "SR"
    assert new_student.research_interests == ['AI', 'Medical Imaging', 'Art of Dance']
    assert new_student.degree == ""
    assert new_student.gpa == 4.1
    assert new_student.military
    assert new_student.gender == 'U'
    assert new_student.ethnicity == 'U'
    assert new_student.country == ""
    assert not new_student.first_generation
    assert new_student.university == ""
    assert not new_student.us_citizenship


@pytest.mark.django_db
def test_image_and_data_post():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",
    )
    key = APIKey.objects.assign_key(obj)
    obj.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    data = {
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.1,
        'military': True,
        'profile_image': tmp_file
    }
    response = client.post(reverse('create_student_form'), data, format='multipart')
    student = Student.objects.get(email='yes@gmail.com')
    assert student.profile_image
    assert student.school_year == 'SR'


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

    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    tmp_file2 = tempfile.NamedTemporaryFile(suffix='.txt')
    tmp_file2.write(b'plz hire me')
    tmp_file2.seek(0)
    tmp_file3 = tempfile.NamedTemporaryFile(suffix='.txt')
    tmp_file3.write(b'all As bb')
    tmp_file3.seek(0)
    data = {
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.1,
        'military': True,
        'profile_image': tmp_file,
        'resume': tmp_file2,
        'transcript': tmp_file3
    }
    response = client.post(reverse('create_student_form'), data, format='multipart')
    student = Student.objects.get(email='yes@gmail.com')
    assert response.status_code == 201
    assert student.profile_image
    assert student.resume
    assert student.transcript
    assert student.school_year == 'SR'


@pytest.mark.django_db()
def test_bad_file_upload():
    obj = APIKey(
        name="tester",
        email="tester@uiowa.edu",
    )
    key = APIKey.objects.assign_key(obj)
    obj.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    tmp_file = tempfile.NamedTemporaryFile(suffix='.txt')
    # file contains no content so it should fail and product status code 400
    tmp_file.seek(0)
    data = {
        'email': 'yes@gmail.com',
        'first_name': 'boz',
        'last_name': 'scaggs',
        'school_year': 'SR',
        'research_interests': ['AI', 'Medical Imaging', 'Art of Dance'],
        'gpa': 4.1,
        'military': True,
        'resume': tmp_file
    }
    response = client.post(reverse('create_student_form'), data, format='multipart')
    assert response.status_code == 400
