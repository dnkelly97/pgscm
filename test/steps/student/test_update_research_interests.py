from pytest_bdd import scenario, given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@scenario("../../feature/student/update_research_interests.feature",
          "Send out Research Interest Form to Prospective Student")
def test_research_interests(live_server):
    pass


@given("I am an Administrator")
def research_interests_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@when("I access the Student Portal")
def access_portal(live_server, browser):
    browser.get(live_server + reverse('student'))


@when("I create a specific user")
def create_user(browser):
    browser.find_element_by_id("create_student_button").click()
    browser.find_element_by_id("id_first_name").send_keys("Test")
    browser.find_element_by_id("id_last_name").send_keys("Test")
    browser.find_element_by_id("id_email").send_keys("test@test.com")
    browser.find_element_by_id("create_student_submit_button").click()


@when("I access that user's profile page")
def access_student_profile(browser):
    browser.find_element_by_link_text("View").click()


@when("I press the 'Request Update' button")
def send_email(browser):
    browser.find_element_by_id("submit_student_email_button").click()


@then("I should get a response that the email was sent successfully")
def success_message(browser):
    assert "Email sent..." in browser.page_source


@then("I should be able to enter the Form url for that user")
def access_form(live_server, browser):
    browser.get(live_server + "/student/research_interests/test@test.com")
    assert "Test" in browser.page_source


@scenario("../../feature/student/update_research_interests.feature",
          "Access Research Interests Form")
def test_access_to_form(live_server):
    pass


@when("I go to Research Interests Form Page")
def go_to_form(live_server, browser):
    browser.get(live_server + "/student/research_interests/test@test.com")


@when("I submit the form as is")
def submit_form(browser):
    browser.find_element_by_id("update_student_submit_button").click()


@then("I should get a confirmation message")
def get_message(browser):
    assert "Thank you for updating this..." in browser.page_source


@then("I should no longer be able to access this page")
def try_access_again(live_server, browser):
    browser.get(live_server + "/student/research_interests/test@test.com")
    assert "ERROR, you do not have access to this website..." in browser.page_source