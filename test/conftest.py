import pytest
from selenium import webdriver


# browser fixture taken from of Group 2:
# https://github.com/UIOWAjohnsonhj/002_SEP2021/blob/main/tests/step_defs/conftest.py
@pytest.fixture
def browser():
    # add headless option to prevent browser window from popping up
    ops = webdriver.ChromeOptions()
    ops.add_argument('headless')
    # create chromedriver
    driver = webdriver.Chrome(options=ops)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
