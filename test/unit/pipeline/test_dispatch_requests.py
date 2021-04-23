import pytest
from pytest_httpserver import httpserver
from pipeline.management.dispatch.dispatch_requests import *
import json
import random


def test_dispatch_url():
    assert DISPATCH_URL == "http://127.0.0.1:8001"


def test_dispatch_auth():
    assert DISPATCH_AUTH != "https://dispatchlite.azurewebsites.net/"


def test_json_request(httpserver,authorization_header):
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(["http://127.0.0.1:8001/templates/1"])
    assert get_templates() == ["http://127.0.0.1:8001/templates/1"]


def test_get_template(httpserver,authorization_header):
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json({'content': 'test'})
    assert get_template(httpserver.url_for("/templates/1")) == {'content': 'test'}


def test_get_all_template_data(httpserver,authorization_header):
    httpserver.expect_request("/templates/", headers=authorization_header).respond_with_json(["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1", headers=authorization_header).respond_with_json({'content': 'test'})
    assert get_all_template_data() == [{'content': 'test'}]


def test_get_template_url():
    assert get_template_url("1_test_123") == "http://127.0.0.1:8001/templates/123"


def test_jsononify_placeholders_valid():
    keys = ['1_content_123', '1_name_123']
    values = [['test1'], ['test2']]

    results = {
        'content': 'test1',
        'name': 'test2'
    }
    assert jsonify_placeholders(keys,values) == results


def test_jsononify_placeholders_invalid():
    keys = ['1_content_123', '1_name_123']
    values = [['test1'], ['']]

    assert jsonify_placeholders(keys,values) == "Invalid"


@pytest.mark.django_db
def test_valid_communications_post():
    pipeline_id = random.randint(1, 2147483646)  # this is not deterministic so this test may fail bc of duplication of keys, but it is very unlikely
    pipeline_name = 'Test Pipeline'
    response = dispatch_campaign_post(pipeline_id, pipeline_name)
    stage_id = random.randint(1, 2147483646)
    name = 'my stage'
    placeholders = {'content': 'hello amigo'}
    template = 'http://fake.template.url.com/templates/789'
    campaign = "http://unimportant.campaign.url.com/campaigns/700"
    response = dispatch_communication_post(pipeline_id, stage_id, name, placeholders, template, campaign)
    assert response.status_code == 201
    assert json.loads(response.content) == "http://127.0.0.1:8001/communications/" + str(stage_id)


@pytest.mark.django_db
def test_invalid_communications_post():
    bad_pipeline_id = 2147483647  # id reserved for failure case
    stage_id = random.randint(1, 2147483646)
    name = 'my stage'
    placeholders = {'content': 'hello amigo'}
    template = 'http://fake.template.url.com/templates/789'
    campaign = "http://unimportant.campaign.url.com/campaigns/700"
    response = dispatch_communication_post(bad_pipeline_id, stage_id, name, placeholders, template, campaign)
    assert response.status_code == 400
    assert json.loads(response.content) == "Bad Request"


def test_valid_campaign_post():
    pipeline_id = random.randint(1, 2147483646)  # this is not deterministic so this test may fail bc of duplication of keys, but it is very unlikely
    pipeline_name = 'Test Pipeline'
    response = dispatch_campaign_post(pipeline_id, pipeline_name)
    assert response.status_code == 201
    assert json.loads(response.content) == 'http://127.0.0.1:8001/campaigns/' + str(pipeline_id)
    # todo: delete the campaign created? for db cleanliness
    # todo: can I hardcode the development dispatch url into this test? How will this work in our CI?


def test_invalid_campaign_post():
    pipeline_id = random.randint(1, 2147483646)  # this is not deterministic so this test may fail bc of duplication of keys, but it is very unlikely
    pipeline_name = 'Test Pipeline'
    dispatch_campaign_post(pipeline_id, pipeline_name)
    response = dispatch_campaign_post(pipeline_id, pipeline_name)
    assert response.status_code == 400
    assert json.loads(response.content) == 'Bad Request'
    # todo: delete the campaign created? for db cleanliness
