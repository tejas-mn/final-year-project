import pytest
from flask import Flask

#gave some top level import error so used these
# import sys
# sys.path.append("..")

from ..config import create_app

# Create a test Flask application
@pytest.fixture()
def app():
    app = create_app()
    yield app

@pytest.fixture()
def client(app):
    client = app.test_client()
    return client
