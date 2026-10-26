import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_home_has_message_and_version(client):
    resp = client.get("/")
    data = resp.get_json()
    assert resp.status_code == 200
    assert "message" in data
    assert "version" in data

def test_add_returns_sum(client):
    resp = client.get("/api/add?a=2&b=3")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 5

def test_add_missing_param_is_400(client):
    resp = client.get("/api/add?a=2")
    assert resp.status_code == 400

def test_add_non_numeric_is_400(client):
    resp = client.get("/api/add?a=x&b=3")
    assert resp.status_code == 400
