from app.core.security import oauth2_scheme
from app.core.settings import settings
from app.db.repositories.group_repo import GroupRepository
from app.db.repositories.role_repo import RoleRepository
from app.db.repositories.user_repo import UserRepository
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.group_service import GroupService
from app.services.role_service import RoleService
from app.services.user_service import UserService
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo=Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_group_repository(db=Depends(get_db)) -> GroupRepository:
    return GroupRepository(db)


def get_group_service(repo=Depends(get_group_repository)) -> GroupService:
    return GroupService(repo)


def get_role_repository(db=Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_role_service(repo=Depends(get_role_repository)) -> RoleService:
    return RoleService(repo)


def get_auth_service(repo=Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
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
