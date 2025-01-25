# tests/test_api/test_server.py
from fastapi.testclient import TestClient
import pytest

def test_get_server_stats(authorized_client):
    response = authorized_client.get("/api/v1/server/stats")
    assert response.status_code == 200
    assert "cpu" in response.json()
    assert "memory" in response.json()
    assert "disk" in response.json()