import pytest
from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys
import time

@scenario('../../feature/apis/update_api.feature', 'Update API Key Page Redirect')
def test_regenerate_api_key_modal(live_server):
    pass


@given("I am an Admin")
def admin_access(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('admin', 'admin@uiowa.edu', 'admin123456')
    user.is_superuser = True
    user.save()
    browser.find_element_by_id('id_username').send_keys('admin')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)


@given("I go to the api portal")
def open_api_portal(live_server, browser):
    browser.get(live_server + '/apis')

@given("I select an API Form with <name>, <email>, <expiration_date> to view")
def create_and_select_api_key(live_server,name, email, expiration_date, browser):
    browser.get(live_server + '/apis')
    browser.find_element_by_id('id_name').send_keys(name)
    browser.find_element_by_id('id_email').send_keys(email)
    browser.find_element_by_id('create_student_submit_button').click()
    browser.find_element_by_link_text("View").click()

@when("I select the update API Key button")
def select_update_api_key(live_server,name, email, expiration_date, browser):
    browser.find_element_by_id("update_api_button").click()

@then("I should see 'Update <name>' on the Update Page")
def confirm_update_page(browser,name):
    assert 'Update '+name in browser.page_source

@scenario('../../feature/apis/update_api.feature', 'Update API Key Page Submit')
def test_regenerate_api_key_confirmation(live_server):
    pass

@when("I fill out the update form with a <new_name>, <new_email>, <new_expiration_date>")
def fill_out_update_form(browser,new_name, new_email, new_expiration_date):
    browser.find_element_by_id('id_name').clear()
    browser.find_element_by_id('id_email').clear()
    browser.find_element_by_id('id_name').send_keys(new_name)
    browser.find_element_by_id('id_email').send_keys(new_email)
    browser.find_element_by_id("update_api_submit_button").click()

@then("I should see <new_name>, <new_email>, <new_expiration_date> on the API Key's profile page")
def confirm_changed_values(browser, new_name, new_email, new_expiration_date):
    assert new_name in browser.page_source
    assert new_email in browser.page_source
