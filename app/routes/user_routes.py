from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas import UserCreateSchema, UserResponseSchema
from app.services import UserService
from app.dependencies import get_user_service, RoleChecker
from app.models import Role, User
from app.common import ResponseFactory

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
    result = await user_service.create_user(user)
    return ResponseFactory.success(
        data=result,
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
    current_seller: User = Depends(RoleChecker([Role.SELLER])),
):
    """
    Retrieve a list of all users in the system.

    Only accessible by users with the SELLER role. Returns a standardized
    success response with the list of users.
    """
    result = await user_service.get_all_users()
    return ResponseFactory.success(data=result)


@router.get("/{email}", response_model=UserResponseSchema)
async def get_user_by_email(
    email: str, user_service: UserService = Depends(get_user_service)
):
    """
    Search for a specific user using their email address.

    Returns a standardized success response containing the user profile data.
    """
    result = await user_service.get_user_by_email(email)
    return ResponseFactory.success(data=result)
