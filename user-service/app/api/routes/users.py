from app.api.dependencies import get_user_service
from app.schemas.user import UserCreate, UserRetrieve
from app.services.user_service import UserService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", response_model=UserRetrieve)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    return service.create_user(user)


@router.get("/{email}", response_model=UserRetrieve)
async def get_user(
    email: str, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    return await service.get_user_by_email(email)


@router.get("/", response_model=UserRetrieve)
async def get_users(service: UserService = Depends(get_user_service)) -> UserRetrieve:
    return await service.get_users()
