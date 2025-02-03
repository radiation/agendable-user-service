from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Role
from app.db.repositories.base_repo import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: AsyncSession):
        super().__init__(model=Role, db=db)
