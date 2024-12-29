import pytest
from app.core.security import verify_password
from app.db.repository import UserRepository


@pytest.mark.asyncio
async def test_user_registration_and_login(test_client, db_session):
    # Registration payload
    user_data = {"email": "test@example.com", "password": "securepassword"}

    # Step 1: Register a new user
    response = await test_client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Check response contains a valid token
    token_data = response.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"

    # Verify user exists in the database
    user_repo = UserRepository(db_session)
    user = await user_repo.get_user_by_email(user_data["email"])
    assert user is not None
    assert user.email == user_data["email"]
    assert verify_password(user_data["password"], user.hashed_password)

    # Step 2: Login with the same credentials
    response = await test_client.post("/auth/login", json=user_data)
    assert response.status_code == 200

    # Check response contains a valid token
    login_token_data = response.json()
    assert "access_token" in login_token_data
    assert "token_type" in login_token_data
    assert login_token_data["token_type"] == "bearer"
