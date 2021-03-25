import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse
from factories import SavedQueryFactory, PipelineFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb


@pytest.fixture
def saved_query():
    return SavedQueryFactory.create()


@pytest.fixture
def saved_query_2():
    return SavedQueryFactory.create()


@pytest.fixture
def pipeline():
    return PipelineFactory.create()


@pytest.fixture
def pipeline_2():
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
@scenario("../../feature/pipeline/delete_query.feature", "Delete a query (popup)")
def test_delete_query_popup(logged_in_browser, saved_query):
    pass


@given("I am on the dashboard page and the confirm delete query popup is visible")
def show_popup(live_server, logged_in_browser, saved_query):
    logged_in_browser.get(live_server + reverse('dashboard'))
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()
    logged_in_browser.find_element_by_id("delete_query_button").click()


@when("I click the popup Delete button again")
@when("I click the popup Delete button")
def click_delete_query(logged_in_browser):
    logged_in_browser.find_element_by_id("final_delete_button").click()


@then("I should see a confirmation message")
def assert_confirmation_message(logged_in_browser):
    WebDriverWait(logged_in_browser, 20).until(
        EC.presence_of_element_located((By.ID, "confirm_delete_message")))


@then("I should not see the query I selected listed anymore")
def assert_query_not_listed(logged_in_browser, saved_query):
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, saved_query.query_name + " radio button")))


#####################################################################################

@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_query.feature", "Delete multiple queries")
def test_multiple_query_delete(logged_in_browser, saved_query, saved_query_2):
    pass


@when("I go to delete another query from the dashboard")
def close_popup_select_query_open_popup(logged_in_browser, saved_query_2):
    WebDriverWait(logged_in_browser, 20).until(
        EC.presence_of_element_located((By.ID, "confirm_delete_message")))
    logged_in_browser.find_element_by_id('escape_popup').click()
    logged_in_browser.find_element_by_id(saved_query_2.query_name + " radio button").click()
    logged_in_browser.find_element_by_id("delete_query_button").click()


@then("neither of the queries I deleted should be listed anymore")
def assert_both_queries_unlisted(logged_in_browser, saved_query, saved_query_2):
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, saved_query.query_name + " radio button")))
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, saved_query_2.query_name + " radio button")))


##########################################################################################################

@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_pipeline.feature", "Delete a pipeline (dashboard)")
def test_delete_pipeline_dashboard(logged_in_browser, pipeline):
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
@scenario("../../feature/pipeline/delete_pipeline.feature", "Delete a pipeline (popup)")
def test_delete_pipeline_popup(logged_in_browser, pipeline):
    pass


@given("I am on the dashboard page and the confirm delete pipeline popup is visible")
def show_popup(live_server, logged_in_browser, pipeline):
    logged_in_browser.get(live_server + reverse('dashboard'))
    logged_in_browser.find_element_by_id(pipeline.name + " radio button").click()
    logged_in_browser.find_element_by_id("delete_pipeline_button").click()


@then("I should not see the pipeline I selected listed anymore")
def assert_query_not_listed(logged_in_browser, pipeline):
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, pipeline.name + " radio button")))


#############################################################################################

@pytest.mark.django_db
@scenario("../../feature/pipeline/delete_pipeline.feature", "Delete multiple pipelines")
def test_multiple_pipeline_delete(logged_in_browser, pipeline, pipeline_2):
    pass


@when("I go to delete another pipeline from the dashboard")
def close_popup_select_pipeline_open_popup(logged_in_browser, pipeline_2):
    WebDriverWait(logged_in_browser, 20).until(
        EC.presence_of_element_located((By.ID, "confirm_delete_message")))
    logged_in_browser.find_element_by_id('escape_popup').click()
    logged_in_browser.find_element_by_id(pipeline_2.name + " radio button").click()
    logged_in_browser.find_element_by_id("delete_pipeline_button").click()


@then("neither of the pipelines I deleted should be listed anymore")
def assert_both_pipelines_unlisted(logged_in_browser, pipeline, pipeline_2):
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, pipeline.name + " radio button")))
    WebDriverWait(logged_in_browser, 20).until(
        EC.invisibility_of_element_located((By.ID, pipeline_2.name + " radio button")))
