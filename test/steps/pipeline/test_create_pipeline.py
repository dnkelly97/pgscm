from pytest_bdd import scenario, given, when, then
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


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
def pipeline_create_setup(live_server, browser):
    browser.get(live_server + '/')
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    browser.get(live_server + reverse('build_pipeline'))#change back to build


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