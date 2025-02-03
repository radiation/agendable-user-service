from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Group
from app.db.repositories.base_repo import BaseRepository


class GroupRepository(BaseRepository[Group]):
    def __init__(self, db: AsyncSession):
        super().__init__(model=Group, db=db)
