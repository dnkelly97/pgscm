from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys


@scenario('../feature/creating_roles.feature', 'Access Create User Page as Admin')
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


@when("I want to access the 'register' page")
def connect_register(live_server, browser):
    browser.get(live_server + '/register')


@then("I get redirected to 'register' page")
def redirect_register(browser):
    assert browser.find_element_by_id('id_register_form')


@scenario('../feature/creating_roles.feature', 'Access Create User Page as Administrator')
def test_user_roles_administrator(live_server):
    pass


@given("I am an Administrator")
def administrator_access(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@then("I get redirected back to 'dashboard' page")
def redirect_dashboard(browser):
    assert browser.find_element_by_id('id_dashboard')
