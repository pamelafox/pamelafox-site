import pytest

from flaskapp import app as flap


@pytest.fixture
def app():
    flap.config["SERVER_NAME"] = "localhost"
    return flap
