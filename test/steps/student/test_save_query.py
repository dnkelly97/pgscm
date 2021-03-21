import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse
from factories import SavedQueryFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.django_db
@given("there is a saved query in the database with name 'Query 0'")
def add_query_to_db():
    saved_query = SavedQueryFactory.build()
    saved_query.query_name = 'Query 0'
    saved_query.save()

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


@pytest.mark.django_db
@scenario("../../feature/student/save_query.feature", "Click 'Save Query' button on the popup")
def test_click_save_query(logged_in_browser):
    pass


@given("I fill out the query name with <name>")
def fill_query(live_server, logged_in_browser, name):
    logged_in_browser.get(live_server + reverse('student'))
    logged_in_browser.find_element_by_id('id_save_query').click()
    logged_in_browser.find_element_by_id('modal_query_name').send_keys(name)


@when("I click the 'Save Query' button")
def click_save_query(logged_in_browser):
    logged_in_browser.find_element_by_id('modal_save_query').click()


@then("I should see an alert in the popup saying <message>")
def assert_alert_message(logged_in_browser, message):
    if 'success' in message:
        WebDriverWait(logged_in_browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )
    else:
        WebDriverWait(logged_in_browser, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
        )
    assert message in logged_in_browser.page_source


@then("the alert should be <color>")
def assert_alert_color(logged_in_browser, color):
    if color == 'green':
        assert logged_in_browser.find_element_by_id('save_success_message').get_attribute('style') == 'display: block;'
        assert logged_in_browser.find_element_by_id('save_failure_message').get_attribute('style') == 'display: none;'
        assert logged_in_browser.find_element_by_id('save_success_message').get_attribute('class') == 'alert alert-success'
    elif color == 'red':
        assert logged_in_browser.find_element_by_id('save_success_message').get_attribute('style') == 'display: none;'
        assert logged_in_browser.find_element_by_id('save_failure_message').get_attribute('style') == 'display: block;'
        assert logged_in_browser.find_element_by_id('save_failure_message').get_attribute('class') == 'alert alert-danger'



# Scenario Outline: Click 'Save Query' button on the popup
#         Given I fill out the query name with <name>
#         When I click the 'Save Query' button
#         Then I should see an alert in the popup saying <message>
#         And the alert should be <color>

# |    | Save Failed - Invalid query name.   | red |
#         | Query 0 | Save Failed - A query with this name already exists. | red |