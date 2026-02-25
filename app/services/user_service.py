from fastapi.responses import JSONResponse
from app.common.response import ResponseFactory
from app.repository import UserRepo
from app.schemas import UserCreateSchema, UserResponseSchema
from fastapi import HTTPException


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def create_user(self, user: UserCreateSchema) -> JSONResponse:
        """
        Create a new user in the system.

        Args:
            user (UserCreateSchema): The user data to create.

        Returns:
            JSONResponse: A standardized success response with the created user data.

        Raises:
            HTTPException: 500 for server errors.
        """
        try:
            result = await self.repo.create_user(user)
            return ResponseFactory.success(
                data=UserResponseSchema.model_validate(result),
                message="User created successfully",
                status_code=201,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_by_email(self, email: str) -> JSONResponse:
        """
        Retrieve a user from the system by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            JSONResponse: A standardized success response with the user data.

        Raises:
            HTTPException: 500 for server errors.
        """
        try:
            data = await self.repo.get_user_by_email(email)
            return ResponseFactory.success(
                data=UserResponseSchema.model_validate(data),
                message="User found successfully",
                status_code=200,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_users(self) -> JSONResponse:
        """
        Retrieve all users registered in the system.

        Returns:
            JSONResponse: A standardized success response with a list of all users.

        Raises:
            HTTPException: 500 for server errors.
        """
        try:
            users = await self.repo.get_all_users()
            users_response = [UserResponseSchema.model_validate(u) for u in users]
            return ResponseFactory.success(
                data=users_response,
                message="Users found successfully",
                status_code=200,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_by_id(self, user_id: int) -> JSONResponse:
        """
        Retrieve a single user by their unique identifier.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            JSONResponse: A standardized success response with the user data.

        Raises:
            HTTPException: 404 if user not found, 500 for server errors.
        """
        try:
            user = await self.repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return ResponseFactory.success(
                data=UserResponseSchema.model_validate(user),
                message="User found successfully",
                status_code=200,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
