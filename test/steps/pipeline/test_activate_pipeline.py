import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse
from factories import SavedQueryFactory, PipelineFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb
import time


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
@scenario("../../feature/pipeline/activate_pipeline.feature", "Activate a pipeline (button)")
def test_activate_button_popup(logged_in_browser, pipeline):
    pass

@given("I am on the dashboard page")
def dashboard(live_server, logged_in_browser):
    logged_in_browser.get(live_server + reverse('dashboard'))

@when("I have selected a pipeline")
def select_pipeline(logged_in_browser, pipeline):
    logged_in_browser.find_element_by_id(pipeline.name + " radio button").click()


@then("a button should appear asking if I would like to activate pipeline")
def assert_popup_appears(logged_in_browser):
    assert 'display: inline-block;' in logged_in_browser.find_element_by_id("activate_pipeline_button").get_attribute('style')

@pytest.mark.django_db
@scenario("../../feature/pipeline/activate_pipeline.feature", "Activate a pipeline (popup)")
def test_activate_modal_popup(logged_in_browser, pipeline):
    pass

@given("I have selected a pipeline")
def select_pipeline(logged_in_browser, pipeline):
    logged_in_browser.find_element_by_id(pipeline.name + " radio button").click()

@when("I click a button to activate the pipeline")
def select_pipeline(logged_in_browser, pipeline):
    logged_in_browser.find_element_by_id("activate_pipeline_button").click()

@then("a modal will appear to confirm the activation")
def assert_popup_appears(logged_in_browser):
    WebDriverWait(logged_in_browser, 20).until(
        EC.presence_of_element_located((By.ID, "confirm_activate_message")))


@pytest.mark.django_db
@scenario("../../feature/pipeline/activate_pipeline.feature", "Activate a pipeline (confirm)")
def test_activate_modal_confirm(logged_in_browser, pipeline):
    pass

@when("I confirm I want to activate the pipeline")
def confirm_pipeline_activation(logged_in_browser, pipeline):
    WebDriverWait(logged_in_browser, 20).until(
        EC.presence_of_element_located((By.ID, "confirm_activate_message")))
    logged_in_browser.find_element_by_id("final_activate_button").click()

@then("I should not see the pipeline on the menu")
def assert_pipeline_activity_changes(logged_in_browser):
    time.sleep(5)
    assert 'Inactive' not in logged_in_browser.page_source
    assert 'Active' in logged_in_browser.page_source

