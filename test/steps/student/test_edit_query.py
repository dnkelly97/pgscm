import pytest
from pytest_bdd import given, when, then, scenario
from factories import SavedQueryFactory
from django.urls import reverse


@pytest.fixture
def saved_query():
    query = SavedQueryFactory.build()
    query.query_name = "test_query"
    query.save()
    return query


@scenario("../../feature/student/edit_query.feature", "Click edit query from dashboard")
def test_click_edit_query(logged_in_browser, saved_query):
    pass


@given("I select a query from the dashboard page")
def select_a_query(live_server, logged_in_browser, saved_query):
    logged_in_browser.get(live_server + reverse('dashboard'))
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()


@when("I click the Edit Query button")
def click_edit_query(logged_in_browser):
    logged_in_browser.find_element_by_id("edit_query_button").click()


@then("I should be redirected to the edit query page for the selected query")
def assert_redirect_to_edit_query_page(live_server, logged_in_browser, saved_query):
    assert reverse('update_query', kwargs={'query_name': saved_query.query_name}) in logged_in_browser.current_url
