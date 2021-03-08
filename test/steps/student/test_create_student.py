from pytest_bdd import scenario, given, when, then
import pytest
from student.models import Student
from django.urls import reverse


@pytest.mark.parametrize(
    ['email', 'first_name','last_name'],
    [
        ('test@gmail.com', 'test_first', 'test_last')
    ]
)

@pytest.mark.django_db
@scenario("../../feature/create_student.feature", "I am on the create student page and I successfully create a student")
def test_student_create_display(live_server,email,first_name,last_name):
    pass

@given("I am on the create student page")
def student_create_setup(live_server, browser):
    # todo once login is done: driver.post(liveserver + '/login/')
    browser.get(live_server + reverse('create'))

@when("I fill out a email: <email>")
def fill_out_email(browser,email):
    browser.find_element_by_id('id_email').send_keys(email)

@when("I fill out a first name: <first_name>")
def fill_out_first_name(browser,first_name):
    browser.find_element_by_id('id_first_name').send_keys(first_name)

@when("I fill out a last name: <last_name>")
def fill_out_last_name(browser,last_name):
    browser.find_element_by_id('id_last_name').send_keys(last_name)

@when("I click the create student submit button")
def create_student_submit(browser):
    browser.find_element_by_id('create_student_submit_button').click()

@then("I should be on the student portal")
def assert_create_student_submit(browser):
    assert browser.find_element_by_id('create_student_button')

