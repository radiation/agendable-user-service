from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserRetrieve(UserBase):
    id: UUID

    model_config = {"from_attributes": True}

    def model_dump(self, **kwargs):
        kwargs.setdefault("exclude", {"hashed_password"})
        return super().model_dump(**kwargs)
