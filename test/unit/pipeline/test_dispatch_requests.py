import pytest
from pytest_httpserver import httpserver
from pipeline.management.dispatch.dispatch_requests import *

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