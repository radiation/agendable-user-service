import json
from typing import Generic, TypeVar

from app.core.redis_client import RedisClient
from app.core.security import get_password_hash
from app.db.repositories.base_repo import BaseRepository
from app.exceptions import NotFoundError
from loguru import logger
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self, repository: BaseRepository[ModelType], redis_client: RedisClient
    ):
        self.repository = repository
        self.redis_client = redis_client

    def _get_model_name(self) -> str:
        return self.repository.model.__name__

    async def _publish_event(self, event_type: str, payload: dict):
        sensitive_fields = {"password", "hashed_password"}
        filtered_payload = {
            key: value for key, value in payload.items() if key not in sensitive_fields
        }
        event = {
            "event_type": event_type,
            "model": self._get_model_name(),
            "payload": filtered_payload,
        }
        channel = f"{self._get_model_name()}_events"
        logger.info(f"Publishing event to channel {channel}: {event}")
        await self.redis_client.publish(channel, json.dumps(event, default=str))

    async def create(self, create_data: CreateSchemaType) -> ModelType:
        data_dict = create_data.model_dump()
        if "password" in data_dict:
            data_dict["hashed_password"] = get_password_hash(data_dict.pop("password"))

        valid_fields = {
            key: value
            for key, value in data_dict.items()
            if hasattr(self.repository.model, key)
        }

        entity = await self.repository.create(valid_fields)
        await self._publish_event("create", valid_fields)
        return entity

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
        updated_fields = update_data.model_dump(exclude_unset=True)
        updated_entity = await self.repository.update(id, updated_fields)
        await self._publish_event("update", {"id": id, **updated_fields})
        return updated_entity

    async def delete(self, id: int) -> bool:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {id} not found"
            )

        success = await self.repository.delete(id)
        if success:
            await self._publish_event("delete", {"id": id})
        return success
