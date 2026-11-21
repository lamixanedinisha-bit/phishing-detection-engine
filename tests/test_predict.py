"""Tests for the rebuilt phishing-detection engine.

These test the rebuilt demo model on illustrative examples only.
They do not reproduce the original capstone evaluation.
"""
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["model_trained"] is True


def test_benign_url():
    r = client.post("/predict", json={"url": "https://www.google.com"})
    assert r.status_code == 200
    assert r.json()["prediction"] == "benign"


def test_malicious_looking_url():
    r = client.post(
        "/predict",
        json={"url": "https://secure-login-verify-account-free-prize.com"},
    )
    assert r.status_code == 200
    assert r.json()["prediction"] == "malicious"


def test_invalid_url_rejected():
    r = client.post("/predict", json={"url": "not-a-url"})
    assert r.status_code == 422
