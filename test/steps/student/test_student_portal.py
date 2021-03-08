from pytest_bdd import scenario, given, when, then
import pytest
from student.models import Student
from django.urls import reverse


@pytest.mark.django_db
@scenario("../../feature/student_portal.feature", "I am on the student page and I want to create a student")
def test_student_display(live_server):
    pass

@given("I am on the student portal")
def student_setup(live_server, browser):
    # todo once login is done: driver.post(liveserver + '/login/')
    browser.get(live_server + reverse('student'))

@when("I click the create student button")
def student_create_click(live_server, browser):
    # todo once login is done: driver.post(liveserver + '/login/')
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
