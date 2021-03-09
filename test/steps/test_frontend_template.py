from pytest_bdd import scenario, given, then, when
from django.urls import reverse


@scenario("../feature/frontend_template.feature", "I can see the navigation bar")
def test_navbar(live_server):
    pass


@given("I am on a page that inherits from the frontend template")
def go_to_dashboard(live_server, browser):
    url = live_server + reverse('dashboard')
    browser.get(url)


@then("I should see a navigation bar")
def assert_navbar(browser):
    assert browser.find_element_by_id('navbar')
