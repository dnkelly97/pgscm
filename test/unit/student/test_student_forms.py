import pytest
from student.models import Student
from student.forms import CreateForm


@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, first_name, last_name, school_year, ethnicity,gender, valid', [
       ('hello@gmail.com', '', '',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       ('hello@gmail.com', '', 'last',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       ('hello@gmail.com', 'first', '',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       ('hello3@gmail.com', 'first', 'last',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, True),
       (None, None, None,Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       (None, 'first', 'last',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       ('hello@gmail.com', None, 'last',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       ('hello@gmail.com', 'first', None,Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False),
       ('test@gmail.com', 'first', 'last',Student.YearInSchool.UNKNOWN,Student.Ethnicity.UNKNOWN,Student.Gender.UNKNOWN, False)
   ]
)

def test_product_form_with_data(email,first_name,last_name,school_year,ethnicity,gender,valid):
    student = Student.objects.create(email='test@gmail.com', first_name='first', last_name='last')

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'school_year': school_year,
        'ethnicity': ethnicity,
        'gender': gender
    }

    form = CreateForm(data=data)

    assert True is not None

    # Helper for finding errors in forms
    # form.non_field_errors()
    # field_errors = [(field.label, field.errors) for field in form]
    # print(field_errors)

    assert valid == form.is_valid()