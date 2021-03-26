from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


@scenario('../../feature/authentication/create_user.feature', 'Create New User as an Admin')
def test_create_user(live_server):
    pass


@given("I am an Admin")
def admin_access(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('admin', 'admin@uiowa.edu', 'admin123456')
    user.is_superuser = True
    user.save()
    browser.find_element_by_id('id_username').send_keys('admin')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@when("I want to create a new user")
def new_user_register(live_server, browser):
    browser.get(live_server + '/register')
    browser.find_element_by_id("id_username").send_keys('harry')
    browser.find_element_by_id("id_email").send_keys('harry@uiowa.edu')
    browser.find_element_by_id("id_password1").send_keys('passleft123')
    browser.find_element_by_id("id_password2").send_keys('passleft123')
    browser.find_element_by_id('id_submit')


@then("I get redirected back to 'dashboard' page")
def redirect_dashboard(live_server, browser):
    browser.get(live_server + '/')  # This needs to change later down the line
    assert browser.find_element_by_id('id_dashboard')


@scenario('../../feature/authentication/create_user.feature', 'Unable to create user as non admin')
def test_non_admin_cannot_create_user(live_server):
    pass


@given("I am a non admin user")
def admin_access(live_server, browser):
    user = User.objects.create_user('user', 'user@uiowa.edu', 'user123456')
    user.save()

@when("I login into the application")
def new_user_register(live_server, browser):
    browser.get(live_server + '/login')
    browser.find_element_by_id("id_username").send_keys('user')
    browser.find_element_by_id("id_password").send_keys('user123456')
    browser.find_element_by_id('id_login_submit').click()

@then("I cannot use a register button")
def redirect_dashboard(live_server, browser):
    try:
        browser.find_element_by_id('id_register_link')
        assert False
    except NoSuchElementException:
        assert True
