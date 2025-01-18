from app.api.dependencies import get_user_service
from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.models import User
from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRetrieve
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, Header, HTTPException, status
from loguru import logger
from pydantic import BaseModel, EmailStr

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", response_model=Token)
async def register_user(
    user_create: UserCreate,
    service: UserService = Depends(get_user_service),
) -> Token:
    logger.info(f"Registering user with data: {user_create.model_dump()}")
    existing_user: list[User] = await service.get_by_field(
        field_name="email", value=user_create.email
    )
    if existing_user:
        logger.warning(f"User with email {user_create.email} already exists")
        raise ValidationError("User with this email already exists")
    else:
        try:
            new_user: User = await service.create(user_create)
            logger.info(f"User created successfully with ID: {new_user.id}")
            token = create_access_token(data={"sub": new_user.email, "id": new_user.id})
            logger.debug(f"Token: {token}")
            return {"access_token": token, "token_type": "bearer"}
        except Exception:
            logger.exception("Unexpected error while creating user")
            raise ValidationError("An unexpected error occurred. Please try again.")


@router.post("/login", response_model=Token)
async def login_user(
    login_request: LoginRequest,
    service: UserService = Depends(get_user_service),
) -> Token:
    user: list[User] = await service.get_by_field(
        field_name="email", value=login_request.email
    )
    if not user:
        raise NotFoundError(f"User with email {login_request.email} not found")
    if not verify_password(login_request.password, user[0].hashed_password):
        raise ForbiddenError(f"Invalid password for user {login_request.email}")
    token = create_access_token(data={"sub": user[0].email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/protected-route", response_model=UserRetrieve)
async def protected_route(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        )

    token = authorization.split(" ")[1]
    try:
        payload = decode_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return {"id": 1, "email": payload["sub"]}
