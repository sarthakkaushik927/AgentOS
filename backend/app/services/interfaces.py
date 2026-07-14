from typing import Protocol
from app.db.models.user import User
from app.schemas.auth import Token

class AuthProviderProtocol(Protocol):
    def create_tokens(self, user: User) -> Token:
        ...

    def verify_token(self, token: str) -> dict:
        ...
