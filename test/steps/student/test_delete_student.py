from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@pytest.mark.django_db
@scenario("../../feature/student/delete_student.feature",
          "Deleting student already in system")
def test_delete_student(live_server):
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


@when("I create a student that I plan on removing")
def create_student(live_server, browser):
    browser.get(live_server + reverse('create'))
    browser.find_element_by_id('id_email').send_keys('test@test.com')
    browser.find_element_by_id('id_first_name').send_keys('test_first')
    browser.find_element_by_id('id_last_name').send_keys('test_last')
    browser.find_element_by_id('create_student_submit_button').click()


@when("I click the delete button to remove this student")
def click_to_delete(live_server, browser):
    assert browser.find_element_by_id('create_student_button')
    assert "test_first" in browser.page_source
    browser.find_element_by_link_text("View").click()
    browser.find_element_by_link_text("Delete").click()


@then("I should be redirected to the delete student page")
def confirm_delete(browser):
    browser.find_element_by_id('confirm_button').click()
    assert browser.find_element_by_id('create_student_button')


@then("I should see student removed on student portal")
def student_deleted(browser):
    assert "test_first" not in browser.page_source
