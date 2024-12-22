import datetime
import os
import uuid
from typing import Any, Optional

import jwt
from app.db import User, get_user_db
from dotenv import load_dotenv
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

load_dotenv()

# Access the secret key
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables!")

# TODO: Remove this line in production
print(f"Loaded SECRET_KEY: {SECRET_KEY[:4]}...")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


class CustomJWTStrategy(JWTStrategy):
    async def write_token(self, user_id: Any) -> str:
        payload = {
            "sub": str(user_id),
            "iss": "user-service",
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=self.lifetime_seconds),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)


def get_jwt_strategy() -> CustomJWTStrategy:
    return CustomJWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
