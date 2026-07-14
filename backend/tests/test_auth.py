import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register
    reg_response = await client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword"
    })
    assert reg_response.status_code == 200
    user_data = reg_response.json()
    assert user_data["email"] == "test@test.com"
    assert "id" in user_data

    # Login
    login_response = await client.post("/api/v1/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    
    # Access protected route
    me_response = await client.get("/api/v1/users/me", headers={
        "Authorization": f"Bearer {tokens['access_token']}"
    })
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "test@test.com"
    
    # Refresh
    refresh_response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": tokens["refresh_token"]
    })
    assert refresh_response.status_code == 200
    new_tokens = refresh_response.json()
    assert "access_token" in new_tokens
