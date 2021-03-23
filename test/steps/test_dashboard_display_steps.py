from pytest_bdd import scenario, given, when, then
import pytest
from pipeline.models import Pipeline, SavedQuery
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User


@pytest.mark.django_db
@scenario("../feature/dashboard_display.feature", "I am on the dashboard page")
def test_dashboard_display(live_server):
    pass


@given("I am a user that is logged in")
def login(live_server, browser):
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.get(live_server + reverse('login'))
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)

@given("I am on the dashboard")
def dashboard_setup(live_server, browser, pipeline_factory, saved_query_factory):
    for i in range(3):
        pipeline_factory()
        saved_query_factory()
    # todo once login is done: driver.post(liveserver + '/login/')
    browser.get(live_server + reverse('dashboard'))


@then("I should see existent pipelines")
def assert_existent_pipelines_displayed(browser):
    pipelines = Pipeline.objects.all()
    pipeline_names = [pipeline.name for pipeline in pipelines]
    for name in pipeline_names:
        assert name in browser.page_source


@then("I should see existent saved queries")
def assert_existent_saved_queries_displayed(browser):
    saved_queries = SavedQuery.objects.all()
    saved_query_names = [query.query_name for query in saved_queries]
    for name in saved_query_names:
        assert name in browser.page_source


@then("I should see buttons for creating, deleting, and editing pipelines")
def assert_pipeline_buttons(browser):
    assert browser.find_element_by_id('create_pipeline_button')
    assert browser.find_element_by_id('delete_pipeline_button')
    assert browser.find_element_by_id('edit_pipeline_button')


@then("I should see buttons for creating, deleting, and editing saved queries")
def assert_saved_query_buttons(browser):
    assert browser.find_element_by_id('create_query_button')
    assert browser.find_element_by_id('delete_query_button')
    assert browser.find_element_by_id('edit_query_button')


@then("each pipeline and query should have a checkbox to select it")
def assert_queries_and_pipelines_have_checkboxes(browser):
    for pipeline in Pipeline.objects.all():
        assert browser.find_element_by_id(pipeline.name + ' radio button')
    for query in SavedQuery.objects.all():
        assert browser.find_element_by_id(query.query_name + ' radio button')

