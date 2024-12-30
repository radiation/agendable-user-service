import pytest


@pytest.mark.asyncio
async def test_user_registration(test_client):
    # Valid registration
    response = await test_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "securepassword"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert "token_type" in token_data

    # Duplicate registration
    response = await test_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "securepassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is already registered"
