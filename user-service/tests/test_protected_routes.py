import pytest


@pytest.mark.asyncio
async def test_protected_route_access(test_client):
    # Access protected route without a token
    response = await test_client.get("/protected-route")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    # Register and get a valid token
    response = await test_client.post(
        "/auth/register",
        json={"email": "protected@example.com", "password": "securepassword"},
    )
    token = response.json()["access_token"]

    # Access protected route with token
    response = await test_client.get(
        "/protected-route", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
