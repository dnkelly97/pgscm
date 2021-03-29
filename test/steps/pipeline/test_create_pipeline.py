from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@pytest.mark.django_db
@scenario("../../feature/pipeline/create_pipeline.feature", "Change the number of stages")
def test_change_num_stages(logged_in_browser):
    pass


@when("I change the number of stages")
def change_num_stages(logged_in_browser):
    logged_in_browser.find_element_by_id("id_num_stages").send_keys('2')
    logged_in_browser.find_element_by_id("id_num_stages").send_keys(Keys.RETURN)


@then("I should see fields for creating a stage equal to the number of stages selected")
def assert_fields_for_correct_num_stages(logged_in_browser):
    assert len(logged_in_browser.find_elements_by_xpath("//input[@name='time_window']")) == 2
    assert len(logged_in_browser.find_elements_by_xpath("//select[@name='advancement_condition']")) == 2
    assert len(logged_in_browser.find_elements_by_xpath("//input[@name='name']")) == 3


@pytest.mark.parametrize(
    ['name', 'num_stages'],
    [
        ('t', 1)
    ]
)
@scenario("../../feature/pipeline/create_pipeline.feature",
          "I am on the create pipeline page and I successfully create a pipeline")
def test_pipeline_create_display(live_server, name, num_stages):
    pass


@given("I am on the create pipeline page")
def pipeline_create_setup(live_server, logged_in_browser):
    logged_in_browser.get(live_server + reverse('build_pipeline'))


@when("I fill out a name: <name>")
def fill_out_name(browser, name):
    browser.find_element_by_id('id_name').send_keys(name)


@when("I fill out number of stages: <num_stages>")
def fill_out_name(browser, num_stages):
    browser.find_element_by_id('id_num_stages').send_keys(num_stages)


@when("I click the create pipeline submit button")
def create_pipeline_submit(browser):
    browser.find_element_by_id('create_pipeline_submit_button').click()


@then("I should be on the dashboard")
def assert_create_student_submit(browser):
    assert browser.find_element_by_id('create_pipeline_submit_button')