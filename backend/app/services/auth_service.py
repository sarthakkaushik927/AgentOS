from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.core.config import settings
from app.db.models.user import User
from app.schemas.auth import Token
from app.services.interfaces import AuthProviderProtocol

class JWTAuthProvider(AuthProviderProtocol):
    def _create_jwt(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def create_tokens(self, user: User) -> Token:
        access_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        access_token = self._create_jwt({"sub": str(user.id), "type": "access"}, access_delta)
        refresh_token = self._create_jwt({"sub": str(user.id), "type": "refresh"}, refresh_delta)
        
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
