# tests/test_api/test_nginx.py
def test_nginx_status(authorized_client):
    response = authorized_client.get("/api/v1/nginx/status")
    assert response.status_code == 200
    assert "running" in response.json()

def test_nginx_invalid_action(authorized_client):
    response = authorized_client.post("/api/v1/nginx/invalid")
    assert response.status_code == 400