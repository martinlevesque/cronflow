import pytest
import json
from celery_admin import celery

test_fernet_key = "BFrJh-fIWvhwokDhsIIhjMuHxcgDXjyNZY_JIQZD78M="


@pytest.fixture(autouse=True)
def run_around_tests(monkeypatch):
    monkeypatch.setenv("FERNET_SECRET_KEY", test_fernet_key)
    yield


def test_celery_http_no_params():
    body = {"name": "testtask"}

    result = celery.http(body=body)

    assert "No params available" in result


def test_celery_http_happy_path(requests_mock):

    requests_mock.get("http://myrequest.com/test", text='{"this": "is"}')

    body = {"name": "testtask", "params": {"url": "http://myrequest.com/test"}}

    result = celery.http(body=body)

    assert result == {
        "content": '{"this": "is"}',
        "status_code": 200,
        "status": "success",
    }


def test_celery_http_exception_on_call():
    params = {"url": "http://myrequest.com/testexception", "timeout": 3}

    result = celery.http(body={"params": params})

    assert result.get("content")
    assert result.get("status"), "error"
