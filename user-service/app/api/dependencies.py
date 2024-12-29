from app.db.repository import UserRepository
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from fastapi import Depends


def get_user_repository(db=Depends(get_db)):
    return UserRepository(db)


def get_user_service(repo=Depends(get_user_repository)):
    return UserService(repo)


def get_auth_service(repo=Depends(get_user_repository)):
    return AuthService(repo)
