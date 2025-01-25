# tests/test_api/test_logs.py
def test_get_logs(authorized_client):
    response = authorized_client.get("/api/v1/logs")
    assert response.status_code == 200
    assert "logs" in response.json()
    assert "total_lines" in response.json()

def test_clear_logs(authorized_client):
    response = authorized_client.delete("/api/v1/logs")
    assert response.status_code == 200
    assert "message" in response.json()