from app.api.dependencies import get_role_service
from app.exceptions import NotFoundError, ValidationError
from app.schemas.roles import RoleCreate, RoleRetrieve, RoleUpdate
from app.services.role_service import RoleService
from fastapi import APIRouter, Depends, status
from loguru import logger

router = APIRouter()


@router.post("/", response_model=RoleRetrieve)
async def create_role(
    role: RoleCreate, service: RoleService = Depends(get_role_service)
) -> RoleRetrieve:
    try:
        logger.info(f"Creating role with data: {role.model_dump()}")
        result = await service.create(role)
        logger.info(f"Role created successfully with ID: {result.id}")
        return result
    except ValidationError as ve:
        logger.warning(f"Validation error: {ve}")
        raise
    except Exception:
        logger.exception("Unexpected error while creating role")
        raise ValidationError("An unexpected error occurred. Please try again.")


@router.get("/by-name", response_model=RoleRetrieve)
async def get_role_by_name(
    name: str, service: RoleService = Depends(get_role_service)
) -> RoleRetrieve:
    role = await service.get_by_field("name", name)
    if not role:
        raise NotFoundError(f"Role with name {name} not found")
    return role[0]


@router.get("/{role_id}", response_model=RoleRetrieve)
async def get_role(
    role_id: int, service: RoleService = Depends(get_role_service)
) -> RoleRetrieve:
    return await service.get_by_id(role_id)


@router.get("/", response_model=list[RoleRetrieve])
async def get_roles(
    service: RoleService = Depends(get_role_service),
) -> list[RoleRetrieve]:
    return await service.get_all()


@router.put("/{role_id}", response_model=RoleRetrieve)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    service: RoleService = Depends(get_role_service),
) -> RoleRetrieve:
    return await service.update(role_id, role_update)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int, service: RoleService = Depends(get_role_service)
) -> None:
    success = await service.delete(role_id)
    if not success:
        raise NotFoundError(f"Role with ID {role_id} not found")
