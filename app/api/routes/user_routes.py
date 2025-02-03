from uuid import UUID

from fastapi import APIRouter, Depends, status
from loguru import logger

from app.api.dependencies import get_current_user, get_user_service
from app.exceptions import NotFoundError, handle_service_exceptions
from app.schemas.user import UserCreate, UserRetrieve, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserRetrieve)
async def get_current_user_profile(
    email: str = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserRetrieve:
    logger.info(f"Fetching current user (email: {email})")
    user = await service.get_by_field(field_name="email", value=email)
    if not user:
        logger.warning(f"User with email {email} not found")
        raise NotFoundError(detail="User not found")
    logger.info(f"User retrieved: {user[0]}")
    return user[0]


@router.post("/", response_model=UserRetrieve)
@handle_service_exceptions
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    return await service.create(user)


@router.get("/by-email", response_model=UserRetrieve)
async def get_user_by_email(
    email: str, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    logger.info(f"Fetching user with email: {email}")
    result = await service.get_by_field(field_name="email", value=email)
    if not result:
        logger.warning(f"User with email {email} not found")
        raise NotFoundError(detail=f"User with email {email} not found")
    return result[0]


@router.get("/{user_id}", response_model=UserRetrieve)
async def get_user(
    user_id: UUID, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    logger.info(f"Fetching user with ID: {user_id}")
    result = await service.get_by_id(user_id)
    if result is None:
        logger.warning(f"User with ID {user_id} not found")
        raise NotFoundError(detail=f"User with ID {user_id} not found")
    logger.info(f"User retrieved: {result}")
    return result


@router.get("/", response_model=list[UserRetrieve])
async def get_users(
    service: UserService = Depends(get_user_service),
) -> list[UserRetrieve]:
    logger.info("Fetching all users")
    result = await service.get_all()
    logger.info(f"Retrieved {len(result)} users")
    return result


@router.put("/{user_id}", response_model=UserRetrieve)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserRetrieve:
    logger.info(
        f"Updating user with ID: {user_id} with data: {user_update.model_dump()}"
    )
    result = await service.update(user_id, user_update)
    if not result:
        raise NotFoundError(detail=f"User with ID {user_id} not found")
    return result


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    logger.info(f"Deleting user with ID: {user_id}")
    success = await service.delete(user_id)
    if not success:
        logger.warning(f"User with ID {user_id} not found")
        raise NotFoundError(detail=f"User with ID {user_id} not found")
    logger.info(f"User with ID {user_id} deleted successfully.")
