from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys


@scenario('../feature/create_user.feature', 'Create New User as an Admin')
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
