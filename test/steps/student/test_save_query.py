import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse


@scenario("../../feature/student/save_query.feature", "Open save query popup")
def test_open_save_query_popup(logged_in_browser):
    pass


@given("I am on the student page")
def fill_out_query_on_student_page(live_server, logged_in_browser):
    logged_in_browser.get(live_server + reverse('student'))


@given("I click the save query button")
def click_save_query(logged_in_browser):
    logged_in_browser.find_element_by_id('id_save_query').click()


@then('a popup should appear')
def popup_visible(logged_in_browser):
    assert logged_in_browser.find_element_by_id('save_query_modal').get_attribute('style') == 'display: block;'


@then('the popup should have fields for entering query name and query description')
def assert_popup_fields(logged_in_browser):
    assert logged_in_browser.find_element_by_id('modal_query_name')
    assert logged_in_browser.find_element_by_id('modal_query_description')


# Given I fill out a query on the student page
#         And I click the save query button
#         Then a popup should appear
#         And the popup should have fields for entering query name and query description
