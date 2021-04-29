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


def test_campaign_post(httpserver, authorization_header):
    response = ["http://127.0.0.1:8001/campaigns/1"]
    httpserver.expect_request("/campaigns/", headers=authorization_header).respond_with_json(response)
    assert dispatch_campaign_post(pipeline_id=1, pipeline_name='test pipeline').json() == response


@pytest.mark.django_db
def test_communications_post(httpserver, authorization_header):
    response = ["http://127.0.0.1:8001/communications/1"]
    httpserver.expect_request("/campaigns/233/communications", headers=authorization_header).respond_with_json(response)
    pipeline_id = 233
    stage_id = 1
    name = 'my stage'
    placeholders = {'content': 'hello amigo'}
    template = 'http://fake.template.url.com/templates/789'
    assert dispatch_communication_post(pipeline_id, stage_id, name, placeholders, template).json() == response


def test_message_request(httpserver, authorization_header):
    response = {'receiptDate': 'today'}
    httpserver.expect_request("/messages/12-aq1", headers=authorization_header).respond_with_json(response)
    assert json.loads(dispatch_message_get('12-aq1').content) == response


def test_batch_request(httpserver, authorization_header):
    response = {'members': []}
    httpserver.expect_request("/batches/12-aq1", headers=authorization_header).respond_with_json(response)
    assert json.loads(dispatch_batch_get('12-aq1').content) == response


# @pytest.mark.django_db
# def test_valid_communications_post():
#     pipeline_id = random.randint(1, 2147483646)  # this is not deterministic so this test may fail bc of duplication of keys, but it is very unlikely
#     pipeline_name = 'Test Pipeline'
#     response = dispatch_campaign_post(pipeline_id, pipeline_name)
#     stage_id = random.randint(1, 2147483646)
#     name = 'my stage'
#     placeholders = {'content': 'hello amigo'}
#     template = 'http://fake.template.url.com/templates/789'
#     response = dispatch_communication_post(pipeline_id, stage_id, name, placeholders, template)
#     assert response.status_code == 201
#     assert json.loads(response.content) == "http://127.0.0.1:8001/communications/" + str(stage_id)
#
#
# @pytest.mark.django_db
# def test_invalid_communications_post():
#     bad_pipeline_id = 2147483647  # id reserved for failure case
#     stage_id = random.randint(1, 2147483646)
#     name = 'my stage'
#     placeholders = {'content': 'hello amigo'}
#     template = 'http://fake.template.url.com/templates/789'
#     response = dispatch_communication_post(bad_pipeline_id, stage_id, name, placeholders, template)
#     assert response.status_code == 400
#     assert json.loads(response.content) == "Bad Request"
#
#
# def test_valid_campaign_post():
#     pipeline_id = random.randint(1, 2147483646)  # this is not deterministic so this test may fail bc of duplication of keys, but it is very unlikely
#     pipeline_name = 'Test Pipeline'
#     response = dispatch_campaign_post(pipeline_id, pipeline_name)
#     assert response.status_code == 201
#     assert json.loads(response.content) == 'http://127.0.0.1:8001/campaigns/' + str(pipeline_id)
#
#
# def test_invalid_campaign_post():
#     pipeline_id = random.randint(1, 2147483646)  # this is not deterministic so this test may fail bc of duplication of keys, but it is very unlikely
#     pipeline_name = 'Test Pipeline'
#     dispatch_campaign_post(pipeline_id, pipeline_name)
#     response = dispatch_campaign_post(pipeline_id, pipeline_name)
#     assert response.status_code == 400
#     assert json.loads(response.content) == 'Bad Request'
