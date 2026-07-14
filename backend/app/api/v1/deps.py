from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import JWTAuthProvider
from app.services.interfaces import AuthProviderProtocol
from app.core.exceptions import UnauthorizedError
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

def get_auth_provider() -> AuthProviderProtocol:
    return JWTAuthProvider()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_provider: AuthProviderProtocol = Depends(get_auth_provider),
    user_service: UserService = Depends(get_user_service)
) -> User:
    try:
        payload = auth_provider.verify_token(token)
        if payload.get("type") != "access":
            raise UnauthorizedError("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid token payload")
        return await user_service.get_user_by_id(user_id)
    except Exception:
        raise UnauthorizedError("Invalid or expired token")
