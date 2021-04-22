import pytest
from pytest_httpserver import httpserver
from pipeline.management.dispatch.dispatch_requests import *

def test_json_request(httpserver):
    httpserver.expect_request("/templates/").respond_with_json(["http://127.0.0.1:8001/templates/1"])
    assert get_templates() == ["http://127.0.0.1:8001/templates/1"]

def test_get_template(httpserver):
    httpserver.expect_request("/templates/1").respond_with_json({'content': 'yourmom'})
    assert get_template(httpserver.url_for("/templates/1")) == {'content': 'yourmom'}

def test_get_all_template_data(httpserver):
    httpserver.expect_request("/templates/").respond_with_json(["http://127.0.0.1:8001/templates/1"])
    httpserver.expect_request("/templates/1").respond_with_json({'content': 'yourmom'})
    assert get_all_template_data() == [{'content': 'yourmom'}]

def test_get_template_url():
    assert get_template_url("1_test_123") == "http://127.0.0.1:8001/templates/123"

def test_jsononify_placeholders():
    keys = ['1_content_123', '1_name_123']
    values = [['test1'], ['test2']]

    results = {
        'content': 'test1',
        'name': 'test2'
    }
    assert jsonify_placeholders(keys,values) == results