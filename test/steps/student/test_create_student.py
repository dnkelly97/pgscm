from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@pytest.mark.parametrize(
    ['email', 'first_name', 'last_name'],
    [
        ('test@gmail.com', 'test_first', 'test_last')
    ]
)
@scenario("../../feature/student/create_student.feature",
          "I am on the create student page and I successfully create a student")
def test_student_create_display(live_server, email, first_name, last_name):
    pass


@given("I am on the create student page")
def student_create_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    browser.get(live_server + reverse('create_student'))


@when("I fill out a email: <email>")
def fill_out_email(browser, email):
    browser.find_element_by_id('id_email').send_keys(email)


@when("I fill out a first name: <first_name>")
def fill_out_first_name(browser, first_name):
    browser.find_element_by_id('id_first_name').send_keys(first_name)


@when("I fill out a last name: <last_name>")
def fill_out_last_name(browser, last_name):
    browser.find_element_by_id('id_last_name').send_keys(last_name)


@when("I click the create student submit button")
def create_student_submit(browser):
    browser.find_element_by_id('id_gpa').send_keys(2)
    browser.find_element_by_id('id_scale').send_keys(5)
    browser.find_element_by_id('create_student_submit_button').click()


@then("I should be on the student portal")
def assert_create_student_submit(browser):
    assert browser.find_element_by_id('create_student_button')
