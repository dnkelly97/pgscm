from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@pytest.mark.django_db
@scenario("../../feature/student/update_student.feature",
          "Update student information")
def test_update_student(live_server):
    pass


@given("I am logged in and on the student page")
def student_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    browser.get(live_server + reverse('student'))


@when("I create a student that I plan on updating")
def create_student(live_server, browser):
    browser.get(live_server + reverse('create'))
    browser.find_element_by_id('id_email').send_keys('test@test.com')
    browser.find_element_by_id('id_first_name').send_keys('test_first')
    browser.find_element_by_id('id_last_name').send_keys('test_last')
    browser.find_element_by_id('create_student_submit_button').click()


@when("I click the update button to update this student's information")
def click_to_update(live_server, browser):
    assert browser.find_element_by_id('create_student_button')
    assert "test_first" in browser.page_source
    browser.find_element_by_link_text("Update").click()


@then("I should be redirected to the update student page")
def confirm_update(browser):
    browser.find_element_by_id('id_first_name').send_keys('test_first_change')
    browser.find_element_by_id('update_student_submit_button').click()
    assert browser.find_element_by_id('create_student_button')


@then("I should see the updated student on the student portal")
def student_deleted(browser):
    assert "test_first_change" in browser.page_source
