from app.api.dependencies import get_current_user, get_user_service
from app.errors import NotFoundError
from app.schemas.user import UserCreate, UserRetrieve, UserUpdate
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.get("/me", response_model=UserRetrieve)
async def get_current_user_profile(
    email: str = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserRetrieve:
    user = await service.get_by_field(field_name="email", value=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user[0]


@router.post("/", response_model=UserRetrieve)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    return await service.create(user)


@router.get("/by-email", response_model=UserRetrieve)
async def get_user_by_email(
    email: str, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    user = await service.get_by_field(field_name="email", value=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user[0]


@router.get("/{user_id}", response_model=UserRetrieve)
async def get_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    return await service.get_by_id(user_id)


@router.get("/", response_model=UserRetrieve)
async def get_users(service: UserService = Depends(get_user_service)) -> UserRetrieve:
    return service.get_all()


@router.put("/{user_id}", response_model=UserRetrieve)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserRetrieve:
    print(user_update)
    updated_user = await service.update(user_id, user_update)
    if not updated_user:
        raise NotFoundError(detail=f"User with ID {user_id} not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    success = await service.delete(user_id)
    if not success:
        raise NotFoundError(detail=f"User with ID {user_id} not found")
