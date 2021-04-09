from pytest_bdd import scenario, given, when, then
import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse
from factories import SavedQueryFactory, PipelineFactory


@pytest.fixture
def source_query(db):
    return SavedQueryFactory.create()


@pytest.fixture
def not_source_query(db):
    return SavedQueryFactory.create()


@pytest.fixture
def pipeline_with_sources(db, source_query):
    pipeline = PipelineFactory.create(name='my test pipeline')
    pipeline.sources.add(source_query)
    pipeline.save()
    return pipeline


@scenario("../../feature/pipeline/edit_pipeline.feature", "I remove a source and add a source")
def test_add_and_remove_source(logged_in_browser, pipeline_with_sources, not_source_query):
    pass


@given("I am on the edit pipeline page")
def on_edit_pipeline_page(live_server, logged_in_browser, pipeline_with_sources):
    logged_in_browser.get(live_server + reverse("update_pipeline", kwargs={'pipeline_name': pipeline_with_sources.name}))


@given("I have selected a source to add")
def select_source_to_add(logged_in_browser):
    logged_in_browser.find_element_by_id('id_add_sources_0').click()


@given("I have selected a source to remove")
def select_source_to_remove(logged_in_browser):
    logged_in_browser.find_element_by_id('id_remove_sources_0').click()


@then("when I click Update the I should be redirected to the dashboard")
def assert_redirect_to_dashboard(logged_in_browser):
    logged_in_browser.find_element_by_id('update_pipeline_submit_button').click()
    assert 'dashboard' in logged_in_browser.current_url


@then("the source added should be added and the source removed should be removed")
def assert_sources_added_and_removed_properly(logged_in_browser, pipeline_with_sources, source_query, not_source_query):
    sources = pipeline_with_sources.sources.all()
    assert source_query not in sources
    assert not_source_query in sources

