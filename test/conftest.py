import pytest
from selenium import webdriver
from pytest_factoryboy import register
from factories import PipelineFactory, SavedQueryFactory


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
    # create chromedriver
    driver = webdriver.Chrome(options=ops)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
