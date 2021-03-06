from selenium import webdriver
import pytest
from pipeline.models import Pipeline, SavedQuery
from pytest_factoryboy import register
from factories import PipelineFactory, SavedQueryFactory


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


register(PipelineFactory)
register(SavedQueryFactory)


# @pytest.fixture(scope="session")
# @pytest.mark.parametrize("name", ["Pipeline 1", "Pipeline 2", "Pipeline 3"])
# def create_test_pipelines(name, db):
#     p = Pipeline()
#     p.name = name
#     p.save()
