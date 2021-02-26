import pytest


def capital_case(x):
    return x.capitalize()


def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'


# Example of @pytest.mark.parametrize usage to parametrize test with many cases
@pytest.mark.parametrize("string, capitalized_string", [
    ('hello', 'Hello'),
    ("i'm dave", "I'm dave"),
    ("justice", "Justice"),
    ("Justice", "Justice")
])
def test_capitol_case_parametrized(string, capitalized_string):
    assert capital_case(string) == capitalized_string


# Example fixture usage
@pytest.fixture
def the_number_six():
    return 6


def test_that_six_is_six(the_number_six):
    assert the_number_six == 6


# Example testing fixture defined in conftest.py
def test_that_seven_is_seven(the_number_seven):
    assert the_number_seven == 7


# Example with the django_db mark
@pytest.mark.django_db
def test_something_that_requires_database():
    # if this test required the database (e.g. Student.objects.all()), it would fail without the mark above
    # currently it is being skipped, not sure why but might be because database isn't set up?
    pass
