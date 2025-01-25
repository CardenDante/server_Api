# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_token():
    return create_access_token(data={"sub": "testuser"})

@pytest.fixture
def authorized_client(client, test_token):
    client.headers = {
        "Authorization": f"Bearer {test_token}"
    }
    return client
