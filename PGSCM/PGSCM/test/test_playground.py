import pytest

def capital_case(x):
    return x.capitalize()

def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'


@pytest.fixture
def the_number_six():
    return 6

def test_that_six_is_six(the_number_six):
    assert the_number_six == 6