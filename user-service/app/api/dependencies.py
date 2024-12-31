from app.core.security import oauth2_scheme
from app.core.settings import settings
from app.db.repositories.user_repo import UserRepository
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo=Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_auth_service(repo=Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
