def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login_user(client):
    # Primeiro registra
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123"}
    )
    # Depois tenta o login
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()