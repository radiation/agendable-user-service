from app.db.models import Role
from app.db.repositories.role_repo import RoleRepository
from app.schemas.roles import RoleCreate, RoleUpdate
from app.services.base_service import BaseService
from sqlalchemy.sql.expression import select


class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    def __init__(self, repository: RoleRepository):
        super().__init__(repository)

    async def set_default_role(self, role_id: int) -> Role:
        # Unset the current default
        await self.db.execute(
            select(Role).where(Role.default).update({"default": False})
        )

        # Set the new default
        role = await self.db.get(Role, role_id)
        if not role:
            raise ValueError("Role not found")

        role.default = True
        await self.db.commit()
        await self.db.refresh(role)
        return role
