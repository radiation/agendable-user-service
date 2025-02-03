from typing import Optional

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    id: int


class GroupRetrieve(GroupBase):
    id: int

    model_config = {"from_attributes": True}
