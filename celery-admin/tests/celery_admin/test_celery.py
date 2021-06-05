import pytest
import json
from celery_admin import celery

test_fernet_key = "BFrJh-fIWvhwokDhsIIhjMuHxcgDXjyNZY_JIQZD78M="


@pytest.fixture(autouse=True)
def run_around_tests(monkeypatch):
    monkeypatch.setenv("FERNET_SECRET_KEY", test_fernet_key)

    def dummy_write(content):
        pass

    celery.write_task_result_file = dummy_write

    yield


# SOCKET PING


def test_celery_socket_ping_not_listening():
    body = {
        "name": "testtask",
        "params": {"host": "127.0.0.1", "port": 55555, "socket_type": "TCP"},
    }

    result = celery.socket_ping(body=body)

    assert result["level"] == "error"
    assert result["status"] == "error"
    assert "down" in result["result"]["error"]


## HTTP


def test_celery_http_no_params():
    body = {"name": "testtask"}

    result = celery.http(body=body)

    assert "No params" in result["result"]["error"]
    assert result["status"] == "error"


def test_celery_http_happy_path(requests_mock):

    requests_mock.get("http://myrequest.com/test", text='{"this": "is"}')

    body = {"name": "testtask", "params": {"url": "http://myrequest.com/test"}}

    result = celery.http(body=body)

    print(result)

    assert result["level"] == "info"
    assert result["status"] == "success"
    assert result["body"] == body
    assert result["result"]["content"] == '{"this": "is"}'
    assert result["result"]["status"] == 'success'
    assert result["result"]["status_code"] == 200
    assert result["result"]["duration"] > 0


def test_celery_http_exception_on_call(requests_mock):
    params = {"url": "http://myrequest.com/testexception", "timeout": 3}

    result = celery.http(body={"params": params})

    assert result["level"], "error"
    assert result["status"], "error"
    assert result["body"] == {"params": params}
    assert "No mock address" in result["result"]["error"]
    assert result["result"]["duration"] > 0
