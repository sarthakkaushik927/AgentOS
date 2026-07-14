from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token, TokenRefresh
from app.services.user_service import UserService
from app.services.interfaces import AuthProviderProtocol
from app.api.v1.deps import get_user_service, get_auth_provider
from app.core.exceptions import UnauthorizedError

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.register(user_in)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
    auth_provider: AuthProviderProtocol = Depends(get_auth_provider)
):
    user = await user_service.authenticate(form_data.username, form_data.password)
    return auth_provider.create_tokens(user)

@router.post("/refresh", response_model=Token)
async def refresh_token(
    data: TokenRefresh,
    user_service: UserService = Depends(get_user_service),
    auth_provider: AuthProviderProtocol = Depends(get_auth_provider)
):
    try:
        payload = auth_provider.verify_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid token type")
        user = await user_service.get_user_by_id(payload.get("sub"))
        return auth_provider.create_tokens(user)
    except Exception:
        raise UnauthorizedError("Invalid refresh token")
