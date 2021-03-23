import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse
from factories import SavedQueryFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def saved_query():
    return SavedQueryFactory.create()


@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_query.feature", "Delete a query")
def test_delete_query(logged_in_browser, saved_query):
    pass


@given("I am on the dashboard page")
def dashboard(live_server, logged_in_browser):
    logged_in_browser.get(live_server + reverse('dashboard'))


@given("I have selected a query")
def select_query(logged_in_browser, saved_query):
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()


@when("I click the Delete Query button")
def delete_query(logged_in_browser):
    logged_in_browser.find_element_by_id("delete_query_button").click()


@then("I should not see the query listed anymore")
def assert_query_not_listed(logged_in_browser, saved_query):
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, saved_query.query_name + " radio button")))
