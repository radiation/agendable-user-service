import json
from typing import Generic, TypeVar

from loguru import logger
from pydantic import BaseModel

from app.core.redis_client import RedisClient
from app.core.security import get_password_hash
from app.db.repositories.base_repo import BaseRepository
from app.exceptions import NotFoundError

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
        channel = f"{self._get_model_name().lower()}-events"
        logger.info(f"Publishing event to channel {channel}: {event}")
        await self.redis_client.publish(channel, json.dumps(event, default=str))

    async def create(self, create_data: CreateSchemaType) -> ModelType:
        data_dict = create_data.model_dump()
        logger.debug(f"Creating {self._get_model_name()} with data: {data_dict}")

        # Hash password if it exists in the data
        if "password" in data_dict:
            data_dict["hashed_password"] = get_password_hash(data_dict.pop("password"))

        # Filter valid fields based on the model
        valid_fields = {
            key: value
            for key, value in data_dict.items()
            if hasattr(self.repository.model, key)
        }

        # Create the entity in the database
        entity = await self.repository.create(valid_fields)

        # Convert the ID to a string for the event payload
        valid_fields["id"] = str(entity.id)

        # Publish the creation event with the full payload
        await self._publish_event("create", valid_fields)
        return entity

    async def get_by_id(self, entity_id: int) -> ModelType:
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {entity_id} not found"
            )
        return entity

    async def get_by_field(self, field_name: str, value: any) -> list[ModelType]:
        return await self.repository.get_by_field(field_name, value)

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
        return await self.repository.get_all(skip, limit)

    async def update(self, entity_id: int, update_data: UpdateSchemaType) -> ModelType:
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {entity_id} not found"
            )
        updated_fields = update_data.model_dump(exclude_unset=True)
        updated_entity = await self.repository.update(entity_id, updated_fields)
        await self._publish_event("update", {"id": entity_id, **updated_fields})
        return updated_entity

    async def delete(self, entity_id: int) -> bool:
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise NotFoundError(
                detail=f"{self._get_model_name()} with ID {entity_id} not found"
            )

        success = await self.repository.delete(entity_id)
        if success:
            await self._publish_event("delete", {"id": entity_id})
        return success
