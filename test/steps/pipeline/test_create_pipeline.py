from pytest_bdd import scenario, given, when, then
import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from factories import PipelineFactory, SavedQueryFactory
from pipeline.models import Pipeline, Stage
from pytest_httpserver import httpserver
from selenium.webdriver.support.select import Select
import time


@pytest.fixture
def savedquery():
    return SavedQueryFactory.create(query_name="my test saved query")


@pytest.fixture
def pipeline():
    return PipelineFactory.create(name="my test pipeline")


@pytest.mark.django_db
@scenario("../../feature/pipeline/create_pipeline.feature", "Change the number of stages")
def test_change_num_stages(logged_in_browser):
    pass


@when("I change the number of stages")
def change_num_stages(logged_in_browser, httpserver,authorization_header):
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json({'name': 'yourmom'})

    logged_in_browser.find_element_by_id("id_num_stages").send_keys('2')
    logged_in_browser.find_element_by_id("id_name").click()  # click elsewhere on the page to produce change event on num_stages


@then("I should see fields for creating a stage equal to the number of stages selected")
def assert_fields_for_correct_num_stages(logged_in_browser):
    assert len(logged_in_browser.find_elements_by_xpath("//input[@name='time_window']")) == 2
    assert len(logged_in_browser.find_elements_by_xpath("//select[@name='advancement_condition']")) == 2
    assert len(logged_in_browser.find_elements_by_xpath("//input[@name='name']")) == 3


@pytest.mark.parametrize(
    ['name', 'num_stages'],
    [
        ('t', 1)
        # ('t2', 2)
    ]
)
@scenario("../../feature/pipeline/create_pipeline.feature",
          "I am on the create pipeline page and I successfully create a pipeline")
def test_pipeline_create_display(live_server, name, num_stages, savedquery):
    pass


@given("I am on the create pipeline page")
def pipeline_create_setup(live_server, logged_in_browser):
    logged_in_browser.get(live_server + reverse('build_pipeline'))


@when("I fill out a name: <name>")
def fill_out_name(browser, name, savedquery):
    browser.find_element_by_id('id_name').send_keys(name)
    browser.find_element_by_id('id_sources').click()


@when("I fill out number of stages: <num_stages>")
def fill_out_num_stages(logged_in_browser, num_stages,httpserver,authorization_header):
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json({'name': 'Basic Template','content':'<@placeholder name="content" type="richtext" />','id': '123'})

    logged_in_browser.find_element_by_id('id_num_stages').send_keys(num_stages)
    logged_in_browser.find_element_by_id("id_name").click()  # click elsewhere on the page to produce change event on num_stages

@when("I click the create pipeline submit button")
def create_pipeline_submit(logged_in_browser):
    logged_in_browser.find_element_by_id('create_pipeline_submit_button').click()


@then("I should be on the dashboard")
def assert_on_dashboard(logged_in_browser):
    WebDriverWait(logged_in_browser, 10).until(
        EC.presence_of_element_located((By.ID, "create_query_button")))


# Scenario: I try to create a pipeline with a name that exists
# #         Given I am on the create pipeline page
# #         When I fill out a pipeline name that exists
# #         And I click the create pipeline submit button
# #         Then I should see an alert saying a pipeline with that name already exists

@scenario("../../feature/pipeline/create_pipeline.feature", "I try to create a pipeline with a name that exists")
def test_create_pipeline_with_existing_name(logged_in_browser, pipeline, savedquery):
    pass


@when("I fill out a pipeline name that exists")
def fill_out_existing_name(logged_in_browser, pipeline, savedquery ,httpserver,authorization_header):
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json(
        {'name': 'Basic Template', 'content': '<@placeholder name="content" type="richtext" />', 'id': '123'})

    logged_in_browser.find_element_by_id('id_name').send_keys(pipeline.name)
    logged_in_browser.find_element_by_id('id_sources').click()
    logged_in_browser.find_element_by_id('id_num_stages').send_keys(1)
    logged_in_browser.find_element_by_id("id_name").click()  # click elsewhere on the page to produce change event on num_stages


@then("I should see an alert saying a pipeline with that name already exists")
def assert_error_message_displayed(logged_in_browser):
    WebDriverWait(logged_in_browser, 10).until(
        EC.visibility_of_element_located((By.ID, "message")))
    assert "A pipeline with that name already exists" in logged_in_browser.page_source

@when("I select a template for each of the <num_stages>")
def logged_in_browser(logged_in_browser, num_stages):
    for i in range(num_stages):
        logged_in_browser.find_element_by_id('Stage_'+str(i+1)+'_dropdown_initalizer').click()
        WebDriverWait(logged_in_browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[text()="Basic Template"]'))).click()

@when("I fill in content for of the <num_stages> templates")
def logged_in_browser(logged_in_browser, num_stages):
    for i in range(num_stages):
        WebDriverWait(logged_in_browser, 10).until(
            EC.visibility_of_element_located((By.NAME, str(i + 1) + '_content' + '_123'))).send_keys("testing")

@pytest.mark.parametrize(
    ['name', 'num_stages'],
    [
        ('t', 1)
    ]
)
@scenario("../../feature/pipeline/create_pipeline.feature", "I try to create a pipeline with selecting a template")
def test_create_pipeline_without_specifying_template(live_server, name, num_stages, savedquery):
    pass

@then("I should see an alert saying the stage does not have a template specified")
def assert_error_message_displayed_for_no_template_specified(logged_in_browser):
    WebDriverWait(logged_in_browser, 10).until(
        EC.visibility_of_element_located((By.ID, "message")))
    assert "Stage 1 does not have a template selected" in logged_in_browser.page_source

@pytest.mark.parametrize(
    ['name', 'num_stages'],
    [
        ('t', 1)
    ]
)
@scenario("../../feature/pipeline/create_pipeline.feature", "I try to create a pipeline without specifying input for a selected template")
def test_create_pipeline_without_specifying_template_data(live_server, name, num_stages, savedquery):
    pass

@then("I should see an alert saying the stage does not have its template data filled out")
def assert_error_message_displayed_for_no_template_data(logged_in_browser):
    WebDriverWait(logged_in_browser, 10).until(
        EC.visibility_of_element_located((By.ID, "message")))
    assert "Stage 1 does not have it's template content filled out" in logged_in_browser.page_source


# Scenario: I select a form to be sent with a stage when creating a pipeline
#         Given I am on the create pipeline page
#         And I have filled out a pipeline's required fields
#         When I change the advancement condition of a stage to 'Form Read'
#         Then I should see an option to select the demographics form or the research interests form

@scenario("../../feature/pipeline/select_form.feature", "I select a form to be sent with a stage when creating a pipeline")
def test_add_form_to_stage(live_server, logged_in_browser):
    pass


@given("I have filled out a pipeline's required fields")
def fill_out_pipeline_fields(logged_in_browser, httpserver, authorization_header):
    logged_in_browser.find_element_by_id('id_name').send_keys("pipelinus")
    logged_in_browser.find_element_by_id('id_sources').click()
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(
        ["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json(
        {'name': 'Basic Template', 'content': '<@placeholder name="content" type="richtext" />', 'id': '123'})
    logged_in_browser.find_element_by_id('id_num_stages').send_keys(1)
    logged_in_browser.find_element_by_id("id_name").click()


@when("I change the advancement condition of a stage to 'Form Received'")
def make_advancement_condition_form_read(logged_in_browser):
    logged_in_browser.find_element_by_xpath("//select[@name='advancement_condition']/option[text()='Form Received']").click()


@then("I should see an option to select the demographics form or the research interests form")
def assert_form_select_present(logged_in_browser):
    logged_in_browser.find_element_by_id("id_form").is_displayed()


    # Scenario: I create a pipeline with 'Form Read' advancement condition
    #     Given I create a pipeline with a stage that has 'Form Read' as the advancement condition
    #     Then that stage should have the correct form associated with it
@scenario("../../feature/pipeline/select_form.feature", "I create a pipeline with 'Form Received' advancement condition")
def test_create_form_received_stage(live_server, logged_in_browser, saved_query):
    pass


@given("I create a pipeline with a stage that has 'Form Received' as the advancement condition")
def create_pipeline_with_form_received_stage(live_server, logged_in_browser, httpserver, authorization_header):
    logged_in_browser.get(live_server + reverse('build_pipeline'))
    logged_in_browser.find_element_by_id('id_name').send_keys("pipelinus")
    logged_in_browser.find_element_by_id('id_sources').click()
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(
        ["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json(
        {'name': 'Basic Template', 'content': '<@placeholder name="content" type="richtext" />', 'id': '123'})
    logged_in_browser.find_element_by_id('id_num_stages').send_keys(1)
    logged_in_browser.find_element_by_id("id_name").click()
    logged_in_browser.find_element_by_xpath(
        "//select[@name='advancement_condition']/option[text()='Form Received']").click()
    logged_in_browser.find_element_by_xpath("//select[@name='form']/option[text()='Demographics Form']").click()
    logged_in_browser.find_element_by_id('Stage_1_dropdown_initalizer').click()
    logged_in_browser.find_element_by_xpath("//button[@class='dropdown-item']").click()
    logged_in_browser.find_element_by_xpath("//textarea[@class='form-control']").send_keys('pipelinus content')
    logged_in_browser.find_element_by_id('create_pipeline_submit_button').click()

@pytest.mark.django_db
@then("that stage should have the correct form associated with it")
def assert_stage_has_correct_form(logged_in_browser):
    time.sleep(1)
    pipeline = Pipeline.objects.get(name='pipelinus')
    assert Stage.objects.get(pipeline=pipeline.id).form == 'DF'
