from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys


@scenario('../../feature/authentication/authentication.feature', 'Login into the application as an Administrator')
def test_authentication_success(live_server):
    pass


@given("I am an Administrator")
def administrator_access(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()


@when("I want to login into the application with correct information")
def login_with_correct_credentials(browser):
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@then("I get access to 'dashboard'")
def redirect_dashboard(browser):
    assert browser.find_element_by_id('id_dashboard')


@scenario('../../feature/authentication/authentication.feature', 'Login into the application with wrong credentials')
def test_authentication_fail(live_server):
    pass


@given("I am an Administrator")
def administrator_access(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()


@when("I want to login into the application with incorrect information")
def login_with_incorrect_credentials(browser):
    browser.find_element_by_id('id_username').send_keys('adminwhoops')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@then("I stay on the login page")
def maintain_login_page(browser):
    assert browser.find_element_by_id('id_login')
