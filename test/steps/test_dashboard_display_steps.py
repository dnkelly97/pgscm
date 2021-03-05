from pytest_bdd import scenario, given, when, then
import pytest


@scenario("../feature/dashboard_display.feature", "I am on the dashboard page")
def test_dashboard_display():
    pass


@pytest.fixture
@given("I am on the dashboard")
def dashboard_response(live_server, driver):
    # driver.post(liveserver + '/login/')
    return driver.get(live_server + '/dashboard/')


@then("I should see existent pipelines")
def assert_existent_pipelines_displayed(dashboard_response):
    pass


@then("I should see existent saved queries")
def assert_existent_saved_queries_displayed(dashboard_response):
    pass


@then("I should see buttons for creating, deleting, and editing pipelines")
def assert_pipeline_buttons(dashboard_response):
    assert dashboard_response.find_by_id('create_pipeline_button')
    assert dashboard_response.find_by_id('delete_pipeline_button')
    assert dashboard_response.find_by_id('edit_pipeline_button')


@then("I should see buttons for creating, deleting, and editing saved queries")
def assert_saved_query_buttons(dashboard_response):
    assert dashboard_response.find_by_id('create_query_button')
    assert dashboard_response.find_by_id('create_query_button')
    assert dashboard_response.find_by_id('create_query_button')
