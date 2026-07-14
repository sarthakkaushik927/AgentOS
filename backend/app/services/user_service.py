from uuid import UUID
from app.repositories.interfaces import UserRepositoryProtocol
from app.schemas.user import UserCreate
from app.db.models.user import User
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import ConflictError, UnauthorizedError, NotFoundError

class UserService:
    def __init__(self, user_repo: UserRepositoryProtocol):
        self.user_repo = user_repo

    async def register(self, user_in: UserCreate) -> User:
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise ConflictError("Email already registered")
        hashed_pw = get_password_hash(user_in.password)
        return await self.user_repo.create(user_in, hashed_pw)

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        return user

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
