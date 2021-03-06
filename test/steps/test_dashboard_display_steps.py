from pytest_bdd import scenario, given, when, then
import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse


@pytest.mark.django_db
@scenario("../feature/dashboard_display.feature", "I am on the dashboard page")
def test_dashboard_display():
    pass


@given("I am on the dashboard")
def dashboard_setup(live_server, driver, pipeline_factory, saved_query_factory):
    for i in range(3):
        pipeline_factory()
        saved_query_factory()
    # todo once login is done: driver.post(liveserver + '/login/')
    print(reverse('dashboard'))
    driver.get(live_server + reverse('dashboard'))


@then("I should see existent pipelines")
def assert_existent_pipelines_displayed(driver):
    pipelines = Pipeline.objects.all()
    pipeline_names = [pipeline.name for pipeline in pipelines]
    for name in pipeline_names:
        assert name in driver.page_source


@then("I should see existent saved queries")
def assert_existent_saved_queries_displayed(driver):
    saved_queries = SavedQuery.objects.all()
    saved_query_names = [query.name for query in saved_queries]
    for name in saved_query_names:
        assert name in driver.page_source


@then("I should see buttons for creating, deleting, and editing pipelines")
def assert_pipeline_buttons(driver):
    assert driver.find_by_id('create_pipeline_button')
    assert driver.find_by_id('delete_pipeline_button')
    assert driver.find_by_id('edit_pipeline_button')


@then("I should see buttons for creating, deleting, and editing saved queries")
def assert_saved_query_buttons(driver):
    assert driver.find_by_id('create_query_button')
    assert driver.find_by_id('create_query_button')
    assert driver.find_by_id('create_query_button')

