from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
import time


@pytest.mark.django_db
@scenario("../../feature/student/delete_student.feature",
          "Delete Student Popup Confirmation")
def test_delete_student_popup(live_server):
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


@given("I create a student that I plan on removing")
def create_student(live_server, browser):
    browser.get(live_server + reverse('create_student'))
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


@then("I should see a modal popup to confirm I want to delete a student")
def confirm_delete(browser):
    assert browser.find_element_by_id("final_student_delete_button").get_attribute('style') == 'display: block;'

@pytest.mark.django_db
@scenario("../../feature/student/delete_student.feature",
          "Delete Student Popup Cancel")
def test_delete_student_cancel(live_server):
    pass

@when("I cancel the deletion of the student")
def click_to_delete(live_server, browser):
    browser.find_element_by_id('escape_student_popup').click()

@then("I should still be on the student's profile page")
def confirm_delete(browser):
    assert 'test@test.com' in browser.page_source
    assert 'test_first' in browser.page_source
    assert 'test_last' in browser.page_source


@pytest.mark.django_db
@scenario("../../feature/student/delete_student.feature",
          "Delete Student Submit")
def test_delete_student_submit(live_server):
    pass

@when("I confirm I want to remove this student")
def click_to_submit_deletion(live_server, browser):
    browser.find_element_by_id('final_student_delete_button').click()
    time.sleep(3) #wait for modal to disappear

@then("I should not see the student on the student portal page")
def confirm_student_deleted(browser):
    assert 'test@test.com' not in browser.page_source
    assert 'test_first' not in browser.page_source
    assert 'test_last' not in browser.page_source