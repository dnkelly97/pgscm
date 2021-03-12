from pytest_bdd import scenario, given, then, when
from django.urls import reverse
import pytest
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def linked_urls():
    return {'Dashboard': reverse('dashboard'),
            'Student Portal': reverse('student'),
            'Logout': reverse('login')}


@scenario("../feature/frontend_template.feature", "I can see the navigation bar")
def test_navbar_present(logged_in_browser):
    pass


@given("I am on a page that inherits from the frontend template")
def go_to_dashboard(live_server, logged_in_browser):
    url = live_server + reverse('dashboard')
    logged_in_browser.get(url)


@then("I should see a navigation bar")
def assert_navbar(logged_in_browser):
    assert logged_in_browser.find_element_by_id('navbar')


@scenario("../feature/frontend_template.feature",
          "I click <page> on the navigation bar",
          example_converters=dict(page=str))
def test_click_navbar_link(logged_in_browser):
    pass


@given("I click the <page> option from the navigation bar")
def click_link(logged_in_browser, page):
    logged_in_browser.find_element_by_link_text(page).click()


@then("I should be redirected to the <page> page")
def assert_redirect_to_correct_page(live_server, logged_in_browser, page, linked_urls):
    expected_url = live_server + linked_urls[page]
    assert logged_in_browser.current_url == expected_url
