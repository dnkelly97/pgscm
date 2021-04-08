from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys


@scenario('../../feature/apis/api_profile.feature', 'Access API profile as an Admin')
def test_user_roles_admin(live_server):
    pass


@given("I am an Admin")
def admin_access(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('admin', 'admin@uiowa.edu', 'admin123456')
    user.is_superuser = True
    user.save()
    browser.find_element_by_id('id_username').send_keys('admin')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@when("I want to access the 'api profile' page")
def connect_register(live_server, browser):
    browser.get(live_server + '/apis')
    browser.find_element_by_id('id_name').send_keys('test')
    browser.find_element_by_id('id_email').send_keys('test@gmail.com')
    browser.find_element_by_id('create_student_submit_button').click()
    browser.find_element_by_link_text("View").click()


@then("I get redirected to 'api profile' page")
def redirect_register(browser):
    assert browser.find_element_by_id('id_profile_header')
