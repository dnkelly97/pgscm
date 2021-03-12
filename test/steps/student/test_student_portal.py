from pytest_bdd import scenario, given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@scenario("../../feature/student/student_portal.feature", "I am on the student page and I want to create a student")
def test_student_display(live_server):
    pass


@given("I am on the student portal")
def student_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    browser.get(live_server + reverse('student'))


@when("I click the create student button")
def student_create_click(live_server, browser):
    browser.find_element_by_id('create_student_button').click()


@given("I should see a button for creating a new student")
def assert_student_buttons(browser):
    assert browser.find_element_by_id('create_student_button')


@then("I should see a create student form")
def assert_create_student_buttons(browser):
    assert browser.find_element_by_id('create_student_form')
    assert browser.find_element_by_id('create_student_submit_button')


@then("Then I should see a create student button")
def assert_create_student_submit_button(browser):
    assert browser.find_element_by_id('create_student_submit_button')
