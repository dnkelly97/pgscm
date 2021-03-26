import pytest
from pytest_bdd import given, when, then, scenario
from django.urls import reverse
from factories import SavedQueryFactory
from student.models import Student


@pytest.fixture
def saved_query():
    query = SavedQueryFactory.build()
    query.query_name = 'test_query'
    query.query['name'] = 'mo'
    query.save()
    return query


@pytest.fixture
def student1():
    return Student.objects.create(email="hello1@gmail.com", first_name="Michael B. Jordan", last_name="second")


@pytest.fixture
def student2():
    return Student.objects.create(email="h@gmail.com", first_name="Monty", last_name="second")


@scenario("../../feature/student/run_saved_query.feature", "Run a saved query")
def test_run_saved_query(logged_in_browser, saved_query, student1, student2):
    pass


@given("I select a query from the dashboard")
def select_query_from_dashboard(live_server, logged_in_browser, saved_query):
    logged_in_browser.get(live_server + reverse("dashboard"))
    logged_in_browser.find_element_by_id(saved_query.query_name + " radio button").click()


@when("I click the Run Query button")
def click_run_query(logged_in_browser):
    logged_in_browser.find_element_by_id("run_saved_query_button").click()


@then("I should see students that met the query conditions displayed on the student page")
def assert_queried_students_displayed(logged_in_browser, student2):
    assert student2.first_name in logged_in_browser.page_source


@then("I should not see other students")
def assert_other_students_not_displayed(logged_in_browser, student1):
    assert student1.first_name not in logged_in_browser.page_source
