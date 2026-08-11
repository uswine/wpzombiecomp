"""Endpoint tests with the Graph client mocked out — no network, no secrets."""

import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

API_KEY = "test-key:sekrit"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("ZC_MAIL_TENANT_ID", "tenant")
    monkeypatch.setenv("ZC_MAIL_CLIENT_ID", "client")
    monkeypatch.setenv("ZC_MAIL_CLIENT_SECRET", "secret")
    monkeypatch.setenv("ZC_MAIL_FROM", "ahall@zombiecomponents.com")
    monkeypatch.setenv("ZC_MAIL_API_KEYS", API_KEY)
    monkeypatch.setenv("ZC_MAIL_HOURLY_CAP", "3")
    monkeypatch.setenv("ZC_MAIL_RECIPIENT_CAP", "20")
    monkeypatch.setenv("ZC_MAIL_STATE_FILE", str(tmp_path / "state.json"))

    import app as app_module
    importlib.reload(app_module)
    app = app_module.create_app()

    sent = []

    class FakeGraph:
        def send_mail(self, **kwargs):
            sent.append(kwargs)

    app.state.graph = FakeGraph()
    test_client = TestClient(app)
    test_client.sent = sent
    return test_client


def payload(**overrides):
    base = {
        "to": ["dest@example.com"],
        "subject": "hello",
        "body": "test body",
    }
    base.update(overrides)
    return base


def test_send_ok(client):
    r = client.post("/api/v1/email/send", json=payload(),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 200
    assert r.json()["status"] == "sent"
    assert r.json()["recipients"] == 1
    assert client.sent[0]["to"] == ["dest@example.com"]
    assert client.sent[0]["body_type"] == "text"


def test_missing_api_key_is_401(client):
    r = client.post("/api/v1/email/send", json=payload())
    assert r.status_code == 401
    assert client.sent == []


def test_wrong_api_key_is_401(client):
    r = client.post("/api/v1/email/send", json=payload(),
                    headers={"X-API-Key": "test-key:wrong"})
    assert r.status_code == 401


def test_no_recipients_is_400(client):
    r = client.post("/api/v1/email/send", json=payload(to=[]),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 400


def test_recipient_cap_is_400(client):
    many = [f"user{i}@example.com" for i in range(21)]
    r = client.post("/api/v1/email/send", json=payload(to=many),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 400
    assert client.sent == []


def test_invalid_address_rejected(client):
    r = client.post("/api/v1/email/send", json=payload(to=["not-an-email"]),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 422


def test_attachments_rejected(client):
    r = client.post("/api/v1/email/send",
                    json=payload(attachments=[{"name": "x.pdf"}]),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 422
    assert client.sent == []


def test_bad_body_type_rejected(client):
    r = client.post("/api/v1/email/send", json=payload(body_type="markdown"),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 422


def test_hourly_cap_is_429(client):
    for _ in range(3):
        assert client.post("/api/v1/email/send", json=payload(),
                           headers={"X-API-Key": API_KEY}).status_code == 200
    r = client.post("/api/v1/email/send", json=payload(),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 429
    assert len(client.sent) == 3


def test_from_is_not_a_request_parameter(client):
    r = client.post("/api/v1/email/send",
                    json=payload(from_address="attacker@example.com"),
                    headers={"X-API-Key": API_KEY})
    assert r.status_code == 422
