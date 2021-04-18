from pytest_bdd import scenario, given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@scenario("../../feature/student/self_create.feature",
          "Check accessibility to form online")
def test_student_access(live_server):
    pass


@given("I am a student")
def no_special_access():
    pass


@when("I click the link to access the form")
def access_form(live_server, browser):
    browser.get(live_server + reverse('self_form'))


@then("I should be able to enter my information")
def check_form(browser):
    assert browser.find_element_by_id("update_student_form")


@scenario("../../feature/student/self_create.feature",
          "Confirm student are being created with this student form")
def test_student_creation(live_server):
    pass


@given("I am an Administrator")
def login_as_administrator(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    browser.get(live_server + reverse('self_form'))


@when("a student creates a profile")
def create_student(browser):
    browser.find_element_by_id("id_first_name").send_keys("Test")
    browser.find_element_by_id("id_last_name").send_keys("Test")
    browser.find_element_by_id("id_email").send_keys("test@uiowa.edu")
    browser.find_element_by_id("update_student_submit_button").click()


@when("I go to the Student Portal")
def access_student_profile(live_server, browser):
    browser.get(live_server + reverse('student'))


@then("I should see the student in the database")
def confirm_student(browser):
    assert "Test" in browser.page_source


@scenario("../../feature/student/self_create.feature",
          "Check fail and success student creation")
def test_check_response(live_server):
    pass


@when("I press the submit button without information")
def submit_without_info(browser):
    browser.find_element_by_id("update_student_submit_button").click()


@then("I should see an error message")
def check_error(browser):
    assert "Creation successful..." not in browser.page_source


@when("I press the submit button with information")
def submit_with_info(browser):
    browser.find_element_by_id("id_first_name").send_keys("Test")
    browser.find_element_by_id("id_last_name").send_keys("Test")
    browser.find_element_by_id("id_email").send_keys("test@uiowa.edu")
    browser.find_element_by_id("update_student_submit_button").click()


@then("I should see a success message")
def check_success(browser):
    assert "Creation successful..." in browser.page_source


@when("I try to submit use the same email")
def submit_same_info(live_server, browser):
    browser.get(live_server + reverse('self_form'))

    browser.find_element_by_id("id_first_name").send_keys("Test")
    browser.find_element_by_id("id_last_name").send_keys("Test")
    browser.find_element_by_id("id_email").send_keys("test@uiowa.edu")
    browser.find_element_by_id("update_student_submit_button").click()

    browser.get(live_server + reverse('self_form'))

    browser.find_element_by_id("id_first_name").send_keys("Test")
    browser.find_element_by_id("id_last_name").send_keys("Test")
    browser.find_element_by_id("id_email").send_keys("test@uiowa.edu")
    browser.find_element_by_id("update_student_submit_button").click()


@then("I should see an error telling me that the email is already in use")
def duplicate_email(browser):
    assert "Email already exists..." in browser.page_source