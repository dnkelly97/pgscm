import pytest
from selenium import webdriver
from pytest_factoryboy import register
from factories import PipelineFactory, SavedQueryFactory
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.keys import Keys

register(PipelineFactory)
register(SavedQueryFactory)


# browser fixture taken from of Group 2:
# https://github.com/UIOWAjohnsonhj/002_SEP2021/blob/main/tests/step_defs/conftest.py
@pytest.fixture
def browser():
    ops = webdriver.ChromeOptions()
    ops.add_argument('headless')
    ops.add_argument('--no-sandbox')
    ops.add_argument('--disable-gpu')
    ops.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=ops)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_browser(browser, live_server):
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = False
    user.save()
    browser.get(live_server + reverse('login'))
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    yield browser


@pytest.fixture
def admin_logged_in_browser(browser, live_server):
    user = User.objects.create_user('administrator', 'administrator@uiowa.edu', 'admin123456')
    user.is_superuser = True
    user.save()
    browser.get(live_server + reverse('login'))
    browser.find_element_by_id('id_username').send_keys('administrator')
    browser.find_element_by_id('id_password').send_keys('admin123456', Keys.RETURN)
    yield browser


@pytest.fixture
def logged_in_client(client, user):
    username = 'bob'
    password = 'bobpass123'
    email = 'bob@uiowa.edu'
    User.objects.create_user(username, email, password)
    client.login(username=username, password=password)
    return client


@pytest.fixture
def user(db):
    username = 'tom'
    password = 'tompass123'
    email = 'tom@uiowa.edu'
    return User.objects.create_user(username, email, password)
