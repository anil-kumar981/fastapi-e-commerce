from fastapi import APIRouter, Depends
from typing import List
from app.schemas import UserCreateSchema, UserResponseSchema
from app.services import UserService
from app.dependencies import get_user_service
from app.common.filters import FilterParams

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserResponseSchema)
async def create_user(
    user: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    """
    Directly create a new user account.

    This endpoint is typically used for administrative purposes and returns
    a standardized success response with the newly created user data.
    """
    return await user_service.create_user(user)


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(
    params: FilterParams = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    """
    Retrieve a list of all users in the system with filtering.

    Only accessible by users with the SELLER role. Returns a standardized
    success response with the list of users.
    """
    return await user_service.get_all_users(params)


@router.get("/{email}", response_model=UserResponseSchema)
async def get_user_by_email(
    email: str, user_service: UserService = Depends(get_user_service)
):
    """
    Search for a specific user using their email address.

    Returns a standardized success response containing the user profile data.
    """
    return await user_service.get_user_by_email(email)
