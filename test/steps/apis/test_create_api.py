import pytest
from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys


# @pytest.mark.django_db
# @scenario('../../feature/apis/create_api.feature', 'Create API Key Page')
# def test_view_create_api_form(live_server):
#     pass
#
# @given("I am an Admin")
# def admin_access(live_server, browser):
#     browser.get(live_server + '/')
#     user = User.objects.create_user('admin', 'admin@uiowa.edu', 'admin123456')
#     user.is_superuser = True
#     user.save()
#     browser.find_element_by_id('id_username').send_keys('admin')
#     browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
#
#
# @given("I access the 'api portal' page")
# def connect_register(live_server,browser):
#     browser.get(live_server + '/apis')
#
# @when("I click the Create API Button")
# def redirect_register(browser):
#     browser.find_element_by_id('create_api_button').click()
#
# @then("I get redirected to 'Create API form' page")
# def redirect_register(browser):
#     assert browser.find_element_by_id('create_student_submit_button')

@pytest.mark.django_db
@scenario('../../feature/apis/create_api.feature', 'Submit New API Key',
          example_converters=dict(name=str, email=str, expiration_date=str, saved=str))
def test_submit_api_key(live_server):
    pass


@given("I access the Create API Form")
def redirect_register(live_server, browser):
    browser.get(live_server + '/apis/create')


@when("I fill out the Create API Form with <name>, <email>, <expiration_date>")
def redirect_register(browser, name, email, expiration_date):
    browser.find_element_by_id('id_name').send_keys(name)
    browser.find_element_by_id('id_email').send_keys(email)
    browser.find_element_by_id('id_expiry_date').send_keys(expiration_date)
    browser.find_element_by_id('create_student_submit_button').click()


@then("the API key was <saved>")
def redirect_register(browser, saved):
    if saved == 'saved':
        assert 'Creation successful...' in browser.page_source
    elif saved == 'not saved':
        assert 'Email already in system' in browser.page_source
