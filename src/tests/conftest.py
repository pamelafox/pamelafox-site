import pytest

from flaskapp import app as flap


@pytest.fixture
def app():
    return flap
