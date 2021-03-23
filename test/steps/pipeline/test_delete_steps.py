import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse
from factories import SavedQueryFactory, PipelineFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def saved_query():
    return SavedQueryFactory.create()


@pytest.fixture
def pipeline():
    return PipelineFactory.create()


@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_query.feature", "Delete a query (dashboard)")
def test_delete_query_dashboard(logged_in_browser, saved_query):
    pass


@given("I am on the dashboard page")
def dashboard(live_server, logged_in_browser):
    logged_in_browser.get(live_server + reverse('dashboard'))


@given("I have selected a query")
def select_query(logged_in_browser, saved_query):
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()


@when("I click the dashboard Delete Query button")
def delete_query(logged_in_browser):
    logged_in_browser.find_element_by_id("delete_query_button").click()


@then("a popup should appear asking me to confirm")
def assert_popup_appears(logged_in_browser):
    assert logged_in_browser.find_element_by_id("delete_modal").get_attribute('style') == 'display: block;'


###########################################################################################################

@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_query.feature", "Delete a query (dashboard)")
def test_delete_query_popup(logged_in_browser, saved_query):
    pass


@given("I am on the dashboard page and the confirm delete popup is visible")
def show_popup(live_server, logged_in_browser, saved_query):
    logged_in_browser.get(live_server + reverse('dashboard'))
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()
    logged_in_browser.find_element_by_id("delete_query_button").click()


@when("I click the popup Delete button")
def click_delete_query(logged_in_browser):
    logged_in_browser.find_element_by_id("final_delete_button").click()


@then("I should see a confirmation message")
def assert_confirmation_message(logged_in_browser):
    WebDriverWait(logged_in_browser, 20).until(
        EC.presence_of_element_located((By.ID, "confirmation_message")))


@then("I should not see the query listed anymore")
def assert_query_not_listed(logged_in_browser, saved_query):
    assert saved_query.query_name not in logged_in_browser.page_source


#####################################################################################

@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_pipeline.feature", "Delete a pipeline (dashboard)")
def test_delete_query_dashboard(logged_in_browser, pipeline):
    pass


@given("I have selected a pipeline")
def select_pipeline(logged_in_browser, pipeline):
    logged_in_browser.find_element_by_id(pipeline.name + " radio button").click()


@when("I click the dashboard Delete Pipeline button")
def delete_pipeline(logged_in_browser):
    logged_in_browser.find_element_by_id("delete_pipeline_button").click()


@then("a popup should appear asking me to confirm")
def assert_popup_appears(logged_in_browser):
    assert logged_in_browser.find_element_by_id("delete_modal").get_attribute('style') == 'display: block;'


##########################################################################################

@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_pipeline.feature", "Delete a pipeline (dashboard)")
def test_delete_query_popup(logged_in_browser, pipeline):
    pass


@given("I am on the dashboard page and the confirm delete pipeline popup is visible")
def show_popup(live_server, logged_in_browser, pipeline):
    logged_in_browser.get(live_server + reverse('dashboard'))
    logged_in_browser.find_element_by_id(pipeline.name + " radio button").click()
    logged_in_browser.find_element_by_id("delete_pipeline_button").click()


@then("I should not see the pipeline listed anymore")
def assert_query_not_listed(logged_in_browser, pipeline):
    assert pipeline.name not in logged_in_browser.page_source
