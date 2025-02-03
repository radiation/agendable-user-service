from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    id: int


class RoleRetrieve(RoleBase):
    id: int

    model_config = {"from_attributes": True}
