from typing import Generic, TypeVar

from app.core.security import get_password_hash
from app.db.repositories.base_repo import BaseRepository
from app.exceptions import NotFoundError
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository

    def _get_model_name(self) -> str:
        return self.repository.model.__name__

    async def create(self, create_data: CreateSchemaType) -> ModelType:
        data_dict = create_data.model_dump()
        if "password" in data_dict:
            data_dict["hashed_password"] = get_password_hash(data_dict.pop("password"))

        valid_fields = {
            key: value
            for key, value in data_dict.items()
            if hasattr(self.repository.model, key)
        }

        return await self.repository.create(valid_fields)

    async def get_by_id(self, id: int) -> ModelType:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {id} not found"
            )
        return entity

    async def get_by_field(self, field_name: str, value: any) -> list[ModelType]:
        return await self.repository.get_by_field(field_name, value)

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
        return await self.repository.get_all(skip, limit)

    async def update(self, id: int, update_data: UpdateSchemaType) -> ModelType:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {id} not found"
            )
        return await self.repository.update(
            id, update_data.model_dump(exclude_unset=True)
        )

    async def delete(self, id: int) -> bool:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {id} not found"
            )
        return await self.repository.delete(id)
