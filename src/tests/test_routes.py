import unittest.mock

import pytest

from flaskapp import app


@pytest.fixture()
def client():
    return app.test_client()


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"I am a human" in response.data


def test_projects(client):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert b"projects" in response.data


def test_talks(client):
    response = client.get("/talks/")
    assert response.status_code == 200
    assert b"talks" in response.data


def test_interviews(client):
    response = client.get("/interviews/")
    assert response.status_code == 200
    assert b"interviews" in response.data


def test_readinglist(client):
    response = client.get("/readinglist/")
    assert response.status_code == 200
    assert b"booklist" in response.data


def test_blogposts(client):
    with unittest.mock.patch("flaskapp.get_blogger_data", autospec=True) as mocked:
        mocked.return_value = [], [], None
        response = client.get("/blogposts/")
        assert response.status_code == 200
        assert b"blog posts" in response.data


def test_blogposts_tag(client):
    with unittest.mock.patch("flaskapp.get_blogger_data") as mocked:
        mocked.return_value = [], [], "a11y"
        response = client.get("/blogposts/a11y.html")
        assert mocked.call_args.args[0] == "a11y"
        assert response.status_code == 200
        assert b"blog posts" in response.data
