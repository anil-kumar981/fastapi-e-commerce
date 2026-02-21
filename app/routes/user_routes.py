from fastapi import APIRouter, Depends
from typing import List
from app.schemas import UserCreateSchema, UserResponseSchema
from app.services import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserResponseSchema)
def create_user(
    user: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(user)


@router.get("/", response_model=List[UserResponseSchema])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users()


@router.get("/{email}", response_model=UserResponseSchema)
def get_user_by_email(
    email: str, user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user_by_email(email)
