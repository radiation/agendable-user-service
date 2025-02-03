from fastapi import APIRouter, Depends, status
from loguru import logger

from app.api.dependencies import get_role_service
from app.exceptions import NotFoundError, handle_service_exceptions
from app.schemas.roles import RoleCreate, RoleRetrieve, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter()


@router.post("/", response_model=RoleRetrieve)
@handle_service_exceptions
async def create_role(
    role: RoleCreate, service: RoleService = Depends(get_role_service)
) -> RoleRetrieve:
    return await service.create(role)


@router.get("/by-name", response_model=RoleRetrieve)
async def get_role_by_name(
    name: str, service: RoleService = Depends(get_role_service)
) -> RoleRetrieve:
    logger.info(f"Fetching role with name: {name}")
    role = await service.get_by_field("name", name)
    if not role:
        logger.warning(f"Role with name {name} not found")
        raise NotFoundError(f"Role with name {name} not found")
    logger.info(f"Role retrieved: {role}")
    return role[0]


@router.get("/{role_id}", response_model=RoleRetrieve)
async def get_role(
    role_id: int, service: RoleService = Depends(get_role_service)
) -> RoleRetrieve:
    logger.info(f"Fetching role with ID: {role_id}")
    result = await service.get_by_id(role_id)
    if result is None:
        logger.warning(f"Role with ID {role_id} not found")
        raise NotFoundError(f"Role with ID {role_id} not found")
    logger.info(f"Role retrieved: {result}")
    return result


@router.get("/", response_model=list[RoleRetrieve])
async def get_roles(
    service: RoleService = Depends(get_role_service),
) -> list[RoleRetrieve]:
    logger.info("Fetching all roles")
    result = await service.get_all()
    logger.info(f"Retrieved {len(result)} roles")
    return result


@router.put("/{role_id}", response_model=RoleRetrieve)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    service: RoleService = Depends(get_role_service),
) -> RoleRetrieve:
    logger.info(
        f"Updating role with ID: {role_id} with data: {role_update.model_dump()}"
    )
    result = await service.update(role_id, role_update)
    if result is None:
        logger.warning(f"Role with ID {role_id} not found")
        raise NotFoundError(f"Role with ID {role_id} not found")
    logger.info(f"Role updated successfully: {result}")
    return result


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int, service: RoleService = Depends(get_role_service)
) -> None:
    logger.info(f"Deleting role with ID: {role_id}")
    success = await service.delete(role_id)
    if not success:
        logger.warning(f"Role with ID {role_id} not found")
        raise NotFoundError(f"Role with ID {role_id} not found")
