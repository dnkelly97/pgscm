import pytest
from student.models import Student

from django.urls import reverse


# @pytest.fixture
# def student():
#     data = {
#         'email': user,
#         'first_name': obj.name,
#         'last_name': obj.price
#     }
#
#     form = ProductForm(data=data)
#     yield form

@pytest.mark.django_db
def test_student_portal(client):
    url = reverse('student')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_student(client):
    url = reverse('create')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, first_name, last_name, school_year, ethnicity,gender, status_code', [
       ("hello@gmail.com", 'first', 'last',Student.YearInSchool.UNKNOWN,
        Student.Ethnicity.UNKNOWN,
        Student.Gender.UNKNOWN, 200),
       ("hello1@gmail.com", 'first',"second",Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, 302)
   ]
)

@pytest.mark.django_db
def test_create_student_submit(client,email,first_name,last_name,school_year,ethnicity,gender,status_code):
    student = Student.objects.create(email="hello@gmail.com", first_name="first", last_name="second")
    student.save()
    url = reverse('create')
    data={
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'school_year': school_year,
        'ethnicity': ethnicity,
        'gender': gender
    }
    response = client.post(url,data=data)
    assert response.status_code == status_code


