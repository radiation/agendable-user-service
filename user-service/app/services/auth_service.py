from datetime import timedelta

from app.core.security import create_access_token, verify_password
from app.db.repository import UserRepository

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token(self, user):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            {"sub": user.email}, expires_delta=access_token_expires
        )
