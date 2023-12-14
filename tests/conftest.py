import pytest
from app import app, db
from flask_sqlalchemy import SQLAlchemy
from config import Config

@pytest.fixture
def app():
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


