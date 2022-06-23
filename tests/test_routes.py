import pytest

from app import app


@pytest.fixture()
def client():
    return app.test_client()


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"I am a human" in response.data


def test_homepage_cache(client):
    response = client.get("/")
    assert "Cache-Control" in response.headers
    assert "max-age=4320000" in response.headers["Cache-Control"]
