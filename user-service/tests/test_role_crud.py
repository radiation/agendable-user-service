import pytest


@pytest.mark.asyncio
async def test_role_crud_operations(test_client, db_session):
    payload = {"name": "crudrole", "description": "Role for CRUD operations"}
    # Create a role
    response = await test_client.post("/roles/", json=payload)
    assert response.status_code == 200
    role_data = response.json()
    assert role_data["name"] == "crudrole"

    # Read a role by name
    response = await test_client.get("/roles/by-name?name=crudrole")
    print(response.json())
    assert response.status_code == 200
    role_data = response.json()
    assert role_data["name"] == "crudrole"

    # Update the role
    response = await test_client.put(
        f"/roles/{role_data['id']}",
        json={"id": role_data["id"], "name": "updatedrole"},
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["name"] == "updatedrole"

    # Delete the role
    response = await test_client.delete(
        f"/roles/{role_data['id']}",
    )
    assert response.status_code == 204
