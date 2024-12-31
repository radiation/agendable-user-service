import pytest


@pytest.mark.asyncio
async def test_user_crud_operations(test_client, db_session):
    # Create a user
    response = await test_client.post(
        "/auth/register",
        json={"email": "cruduser@example.com", "password": "securepassword"},
    )
    assert response.status_code == 200
    token_data = response.json()
    token = token_data["access_token"]

    # Read a user by email
    response = await test_client.get("/users/by-email?email=cruduser@example.com")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "cruduser@example.com"

    # Read the current user
    response = await test_client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "cruduser@example.com"

    # Update the user
    response = await test_client.put(
        f"/users/{user_data['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": user_data["id"], "email": "updateduser@example.com"},
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["email"] == "updateduser@example.com"

    # Delete the user
    response = await test_client.delete(
        f"/users/{user_data['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
