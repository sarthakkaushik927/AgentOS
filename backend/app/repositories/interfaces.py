from typing import Protocol, Optional
from uuid import UUID
from app.db.models.user import User
from app.schemas.user import UserCreate

class UserRepositoryProtocol(Protocol):
    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        ...

    async def create(self, user_in: UserCreate, hashed_password: str) -> User:
        ...
