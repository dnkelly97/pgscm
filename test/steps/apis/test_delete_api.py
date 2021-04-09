import pytest
from django.contrib.auth.models import User
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.keys import Keys
import time

@scenario('../../feature/apis/delete_api.feature', 'Delete API Key Popup Confirmation')
def test_delete_api_key_modal(live_server):
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
def connect_register(live_server, browser):
    browser.get(live_server + '/apis')

@given("I select an API Form with <name>, <email>, <expiration_date> to view")
def connect_register(live_server,name, email, expiration_date, browser):
    browser.get(live_server + '/apis')
    browser.find_element_by_id('id_name').send_keys(name)
    browser.find_element_by_id('id_email').send_keys(email)
    browser.find_element_by_id('create_student_submit_button').click()
    browser.find_element_by_link_text("View").click()

@when("I select the delete API Key button")
def connect_register(live_server,name, email, expiration_date, browser):
    browser.find_element_by_id("delete_api_button").click()

@then("I should see a popup modal appear to confirm the deletion of the key")
def connect_register(browser):
    assert browser.find_element_by_id("final_delete_button").get_attribute('style') == 'display: block;'

@scenario('../../feature/apis/delete_api.feature', 'Delete API Key')
def test_delete_api_key_confirmation(live_server):
    pass

@when("I confirm I want to delete the API Key")
def connect_register(browser):
    print(browser.page_source)
    browser.find_element_by_id("final_delete_button").click()
    time.sleep(3) #needed for delay

@then("I should not see <name>, <email> or <expiration_date> on the api portal")
def connect_register(browser, name, email, expiration_date):
    assert name not in browser.page_source
    assert email not in browser.page_source
    assert expiration_date not in browser.page_source

@scenario('../../feature/apis/delete_api.feature', 'Delete API Key Cancel Modal')
def test_delete_api_key_modal_cancel(live_server):
    pass

@when("I cancel my delete API Key command")
def connect_register(browser):
    browser.find_element_by_id("escape_delete_popup").click()

@then("I should see <name>, <email> or <expiration_date> on the api profile page")
def connect_register(browser, name, email, expiration_date):
    assert name in browser.page_source
    assert email in browser.page_source
