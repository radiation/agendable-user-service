from app.core.redis_client import RedisClient
from app.db.models import Group
from app.db.repositories.group_repo import GroupRepository
from app.schemas.groups import GroupCreate, GroupUpdate
from app.services.base_service import BaseService


class GroupService(BaseService[Group, GroupCreate, GroupUpdate]):
    def __init__(self, repository: GroupRepository, redis_client: RedisClient):
        super().__init__(repository, redis_client)
