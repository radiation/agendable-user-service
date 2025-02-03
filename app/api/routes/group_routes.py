from fastapi import APIRouter, Depends, status
from loguru import logger

from app.api.dependencies import get_group_service
from app.exceptions import NotFoundError, handle_service_exceptions
from app.schemas.groups import GroupCreate, GroupRetrieve, GroupUpdate
from app.services.group_service import GroupService

router = APIRouter()


@router.post("/", response_model=GroupRetrieve)
@handle_service_exceptions
async def create_group(
    group: GroupCreate, service: GroupService = Depends(get_group_service)
) -> GroupRetrieve:
    return await service.create(group)


@router.get("/by-name", response_model=GroupRetrieve)
async def get_group_by_name(
    name: str, service: GroupService = Depends(get_group_service)
) -> GroupRetrieve:
    logger.info(f"Fetching group with name: {name}")
    group = await service.get_by_field("name", name)
    if not group:
        logger.warning(f"Group with name {name} not found")
        raise NotFoundError(f"Group with name {name} not found")
    logger.info(f"Group retrieved: {group}")
    return group[0]


@router.get("/{group_id}", response_model=GroupRetrieve)
async def get_group(
    group_id: int, service: GroupService = Depends(get_group_service)
) -> GroupRetrieve:
    logger.info(f"Fetching group with ID: {group_id}")
    result = await service.get_by_id(group_id)
    if result is None:
        logger.warning(f"Group with ID {group_id} not found")
        raise NotFoundError(f"Group with ID {group_id} not found")
    logger.info(f"Group retrieved: {result}")
    return result


@router.get("/", response_model=list[GroupRetrieve])
async def get_groups(
    service: GroupService = Depends(get_group_service),
) -> list[GroupRetrieve]:
    logger.info("Fetching all groups")
    result = await service.get_all()
    logger.info(f"Retrieved {len(result)} groups")
    return result


@router.put("/{group_id}", response_model=GroupRetrieve)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    service: GroupService = Depends(get_group_service),
) -> GroupRetrieve:
    logger.info(
        f"Updating group with ID: {group_id} with data: {group_update.model_dump()}"
    )
    result = await service.update(group_id, group_update)
    if result is None:
        logger.warning(f"Group with ID {group_id} not found")
        raise NotFoundError(f"Group with ID {group_id} not found")
    logger.info(f"Group updated: {result}")
    return result


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int, service: GroupService = Depends(get_group_service)
) -> None:
    logger.info(f"Deleting group with ID: {group_id}")
    response_status = await service.delete(group_id)
    if not response_status:
        logger.warning(f"Group with ID {group_id} not found")
        raise NotFoundError(f"Group with ID {group_id} not found")
