from pytest_bdd import scenario, given, then, when
from django.urls import reverse
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait


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


@scenario("../feature/frontend_template.feature", "I click 'Dashboard' on the navigation bar")
def test_click_dashboard(live_server):
    pass


@given("I click the 'Dashboard' option from the navigation bar")
def click_dashboard(browser):
    browser.find_element_by_link_text("Dashboard").click()


@then("I should be redirected to the dashboard page")
def assert_redirect_to_dashboard(live_server, browser):
    expected_url = live_server + reverse('dashboard')
    assert browser.current_url == expected_url
