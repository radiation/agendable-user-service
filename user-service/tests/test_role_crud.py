import json

import pytest


@pytest.mark.asyncio
async def test_role_crud_operations(test_client, mock_redis_client):
    role_data = {"name": "crudrole", "description": "Role for CRUD operations"}

    # Create a role
    response = await test_client.post("/roles/", json=role_data)
    assert response.status_code == 200
    role_data = response.json()
    assert role_data["name"] == "crudrole"

    mock_redis_client.publish.assert_awaited_with(
        "role-events",
        json.dumps(
            {
                "event_type": "create",
                "model": "Role",
                "payload": {
                    "name": "crudrole",
                    "description": "Role for CRUD operations",
                    "id": str(role_data["id"]),
                },
            }
        ),
    )

    # Read a role by name
    response = await test_client.get("/roles/by-name?name=crudrole")
    assert response.status_code == 200
    role_data = response.json()
    role_id = role_data["id"]
    assert role_data["name"] == "crudrole"

    # Update the role
    response = await test_client.put(
        f"/roles/{role_data['id']}",
        json={"id": role_data["id"], "name": "updatedrole"},
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["name"] == "updatedrole"

    mock_redis_client.publish.assert_awaited_with(
        "role-events",
        json.dumps(
            {
                "event_type": "update",
                "model": "Role",
                "payload": {"id": int(role_id), "name": "updatedrole"},
            }
        ),
    )

    # Delete the role
    response = await test_client.delete(
        f"/roles/{role_data['id']}",
    )
    assert response.status_code == 204

    mock_redis_client.publish.assert_awaited_with(
        "role-events",
        json.dumps(
            {
                "event_type": "delete",
                "model": "Role",
                "payload": {"id": int(role_id)},
            }
        ),
    )
