import pytest
from pytest_httpserver import httpserver

def test_json_request(httpserver):
    httpserver.expect_request("/templates/").respond_with_json(["http://127.0.0.1:8000/templates/1"])
    assert get_templates() == ["http://127.0.0.1:8000/templates/1"]

def test_get_template(httpserver):
    httpserver.expect_request("/templates/1").respond_with_json({'content': 'yourmom'})
    assert get_template(httpserver.url_for("/templates/1")) == {'content': 'yourmom'}

def test_get_wtf(httpserver):
    httpserver.expect_request("/templates/").respond_with_json(["http://127.0.0.1:8000/templates/1"])
    httpserver.expect_request("/templates/1").respond_with_json({'content': 'yourmom'})
    assert wtf() == [{'content': 'yourmom'}]