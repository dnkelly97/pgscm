import pytest
from apis.models import APIKey
from apis.serializers import StudentSerializer
from student.models import Student


@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, first_name, last_name, valid', [
       ('hello@gmail.com', 'first', 'last', True),
       ('test@gmail.com', 'first', 'last', False),
       ('hello@gmail.com', 'first', '', False),
       ('hello@gmail.com', '', 'last', False),
       ('hello3', 'first', 'last', False),
       ('', 'first', 'last', False),
       (None, None, None, False)
   ]
)
@pytest.mark.django_db
def test_student_serializer(email,first_name,last_name,valid):
    obj = Student.objects.create(email="test@gmail.com", first_name="first", last_name="second")
    obj.save()

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }

    serializer = StudentSerializer(data=data)

    assert True is not None

    assert valid == serializer.is_valid()


@pytest.mark.parametrize('email, first_name, last_name, school_year, valid', [
    ('mymail@gmail.com', 'tuck', 'dickson', 'NOT_A_YEAR', False)
])
@pytest.mark.django_db
def test_extended_student_serializer(email, first_name, last_name, school_year, valid):

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'school_year': school_year
    }

    serializer = StudentSerializer(data=data)

    assert True is not None

    assert valid == serializer.is_valid()