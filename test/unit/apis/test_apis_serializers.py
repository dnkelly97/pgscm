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


@pytest.mark.parametrize('email, first_name, last_name, school_year, research_interests, degree, '
                         'university, gpa, ethnicity, gender, country, us_citizenship, first_generation,'
                         'military, valid', [
    ('mymail@gmail.com', 'tuck', 'dickson', 'NOT_A_YEAR', None, "", "", None, "U", "U", None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "", "", None, "U", "U", None, None, None, None, True),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', 'NOT_AN_ARRAY', "", "", None, "U", "U", None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', ['AI', 'Medical Imaging'], "", "", None, "U", "U", None, None, None, None, True),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, None, "", None, "U", "U", None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, "U", "U", None, None, None, None, True),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", None, None, "U", "U", None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", "NOT_A_FLOAT", "U", "U", None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, None, "U", None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, "U", None, None, None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, "U", "U", "NOT_A_COUNTRY", None, None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, "U", "U", None, "NOT_A_BOOLEAN", None, None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, "U", "U", None, None, "NOT_A_BOOLEAN", None, False),
    ('mymail@gmail.com', 'tuck', 'dickson', 'FR', None, "MSEE", "", None, "U", "U", None, None, None, "NOT_A_BOOLEAN", False),
])
@pytest.mark.django_db
def test_extended_student_serializer(email, first_name, last_name, school_year, research_interests, degree,
                                     university, gpa, ethnicity, gender, country, us_citizenship, first_generation,
                                     military, valid):

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'school_year': school_year,
        'research_interests': research_interests,
        'degree': degree,
        'university': university,
        'gpa': gpa,
        'ethnicity': ethnicity,
        'gender': gender,
        'country': country,
        'us_citizenship': us_citizenship,
        'first_generation': first_generation,
        'military': military,
    }

    serializer = StudentSerializer(data=data)

    assert True is not None

    assert serializer.is_valid() == valid
