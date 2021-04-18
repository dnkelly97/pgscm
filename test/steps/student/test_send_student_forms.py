from pytest_bdd import scenario, given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@scenario("../../feature/student/student_forms.feature",
          "Email can be sent to student to create full profile")
def test_student_forms(live_server):
    pass


@given("I am an administrator")
def student_forms_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    browser.get(live_server + reverse('student'))


@when("I go to the Student Portal and click Request Information Button")
def go_to_student_portal(browser):
    browser.find_element_by_id('email_student_button').click()


@then("I should be prompted to enter a student's email")
def assert_student_forms(browser):
    assert browser.find_element_by_id('send_email_submit_button')


@scenario("../../feature/student/student_forms.feature",
          "Email a student with a particular email")
def test_sending_email(live_server):
    pass


@when("I enter an email to send the form to")
def enter_student_email(browser):
    browser.find_element_by_id('id_from_email').send_keys('test@test.com')
    browser.find_element_by_id('send_email_submit_button').click()


@then("I should get a confirmation message saying I so successfully")
def confirm_sent_email(browser):
    assert "Email sent..." in browser.page_source


@scenario("../../feature/student/student_forms.feature",
          "Enter an invalid email")
def test_sending_email(live_server):
    pass


@when("I enter an invalid email format")
def enter_invalid_email(browser):
    browser.find_element_by_id('id_from_email').send_keys('test')
    browser.find_element_by_id('send_email_submit_button').click()


@then("I should get an error message saying that something went wrong")
def fail_sending_email(browser):
    assert "Email sent..." not in browser.page_source
