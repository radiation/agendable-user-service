from app.db.models import Group
from app.db.repositories.base_repo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class GroupRepository(BaseRepository[Group]):
    def __init__(self, db: AsyncSession):
        super().__init__(model=Group, db=db)
