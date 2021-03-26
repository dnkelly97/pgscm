import pytest
from pytest_bdd import given, when, then, scenario
from factories import SavedQueryFactory
from django.urls import reverse
from pipeline.models import SavedQuery


@pytest.fixture
def saved_query():
    query = SavedQueryFactory.build()
    query.query_name = "test_query"
    query.save()
    return query


@pytest.fixture
def saved_query2():
    query = SavedQueryFactory.build()
    query.query_name = "test_query2"
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


@scenario("../../feature/student/edit_query.feature", "Change name field to valid name")
def test_change_field_valid(logged_in_browser, saved_query, saved_query2):
    pass


@given("I am on the edit query page")
def navigate_to_edit_query_page(live_server, logged_in_browser, saved_query):
    url = live_server + reverse('dashboard')
    logged_in_browser.get(url)
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()
    logged_in_browser.find_element_by_id("edit_query_button").click()


@given("I change the name of a query to an available name")
def change_query_name_valid(logged_in_browser):
    logged_in_browser.find_element_by_id("id_query_name").clear()
    logged_in_browser.find_element_by_id("id_query_name").send_keys("my favorite query")


@when("I click the Update button")
def click_update_button(logged_in_browser, saved_query):
    logged_in_browser.find_element_by_id("update_query_button").click()


@then("I should be redirected to the dashboard page")
def assert_redirect_to_dashboard(logged_in_browser):
    assert "PGSCM Dashboard" in logged_in_browser.page_source


@then("the name of the query should be updated")
def assert_query_name_updated(logged_in_browser, saved_query):
    assert SavedQuery.objects.get(query_name="my favorite query")
    try:
        SavedQuery.objects.get(query_name=saved_query.query_name)
        assert False
    except SavedQuery.DoesNotExist:
        assert True


@scenario("../../feature/student/edit_query.feature", "Change name field to invalid name")
def test_change_field_invalid(logged_in_browser, saved_query, saved_query2):
    pass


@given("I change the name of a query to an unavailable name")
def change_query_name_invalid(logged_in_browser, saved_query2):
    logged_in_browser.find_element_by_id("id_query_name").clear()
    logged_in_browser.find_element_by_id("id_query_name").send_keys(saved_query2.query_name)


@then("I should see a message telling me the query couldn't be saved")
def assert_save_failure_message(logged_in_browser):
    assert "Query could not be saved because one or more fields were invalid." in logged_in_browser.page_source


@then("the name of the query should not be updated")
def assert_name_of_query_not_updated(logged_in_browser, saved_query):
    assert SavedQuery.objects.get(query_name=saved_query.query_name)
