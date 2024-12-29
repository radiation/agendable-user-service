from app.core.security import get_password_hash
from app.db.repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user_create: UserCreate):
        user_data = user_create.model_dump()
        user_data["password"] = get_password_hash(user_create.password)
        return await self.repo.create_user(**user_data)

    async def get_user_by_email(self, email: str):
        return await self.repo.get_user_by_email(email)

    async def get_users(self):
        return await self.repo.get_users()
