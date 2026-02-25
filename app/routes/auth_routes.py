from fastapi import APIRouter, Depends, status
from app.schemas import UserRegisterSchema, UserLoginSchema
from app.services.auth_service import AuthService
from app.dependencies.user_depend import get_user_repo

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_auth_service(user_repo=Depends(get_user_repo)):
    return AuthService(user_repo)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Handle user registration requests.

    Expects user registration details, hashes the password, and returns a
    standardized success response with user data and a JWT access token.
    """
    return await auth_service.register(user_data)


@router.post("/login")
async def login(
    login_data: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Handle user login requests.

    Authenticates the user using email and password, and returns a
    standardized success response with user data and a JWT access token.
    """
    return await auth_service.login(login_data)
