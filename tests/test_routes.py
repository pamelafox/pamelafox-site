import unittest.mock

import pytest

import src


@pytest.fixture()
def client():
    return src.app.test_client()


@pytest.fixture()
def fake_worksheet_data(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setattr(src, "get_worksheet_data", lambda _: [])


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"I am a human" in response.data


def test_homepage_cache(client):
    response = client.get("/")
    assert "Cache-Control" in response.headers
    assert "max-age=4320000" in response.headers["Cache-Control"]


def test_projects(client, fake_worksheet_data):
    response = client.get("/projects")
    assert response.status_code == 200
    assert b"projects" in response.data


def test_talks(client, fake_worksheet_data):
    response = client.get("/talks")
    assert response.status_code == 200
    assert b"talks" in response.data


def test_interviews(client, fake_worksheet_data):
    response = client.get("/interviews")
    assert response.status_code == 200
    assert b"interviews" in response.data


def test_readinglist(client):
    response = client.get("/readinglist")
    assert response.status_code == 200
    assert b"booklist" in response.data


def test_blogposts(client):
    with unittest.mock.patch("src.get_blogger_data", autospec=True) as mocked:
        mocked.return_value = [], [], None
        response = client.get("/blogposts")
        assert response.status_code == 200
        assert b"blog posts" in response.data


def test_blogposts_tag(client):
    with unittest.mock.patch("src.get_blogger_data") as mocked:
        mocked.return_value = [], [], "a11y"
        response = client.get("/blogposts?tag=a11y")
        assert mocked.call_args.args[0] == "a11y"
        assert response.status_code == 200
        assert b"blog posts" in response.data
