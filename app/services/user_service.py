from fastapi.responses import JSONResponse
from app.common.response import ResponseFactory
from app.repository import UserRepo
from app.schemas import UserCreateSchema, UserResponseSchema
from app.common.filters import FilterParams
from fastapi import HTTPException
from app.core.redis import redis_client
import json


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

            # Invalidate user list cache
            keys = await redis_client.keys("users:page:*")
            if keys:
                await redis_client.delete(*keys)

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

    async def get_all_users(self, params: FilterParams) -> JSONResponse:
        """
        Retrieve users registered in the system with filtering.

        Args:
            params (FilterParams): Filtering, sorting and pagination parameters.

        Returns:
            JSONResponse: A standardized success response with a list of users.

        Raises:
            HTTPException: 500 for server errors.
        """
        try:
            cache_key = f"users:page:{params.page}:size:{params.size}:search:{params.search}:sort_by:{params.sort_by}:order:{params.order}"
            cached_users = await redis_client.get(cache_key)

            if cached_users:
                # Deserialize the list of dicts from JSON
                users_data = json.loads(cached_users)
                return ResponseFactory.success(
                    data=users_data,
                    message="Users found successfully (from cache)",
                    status_code=200,
                )

            # Fetch from database
            users = await self.repo.get_all_users(params)

            # Prepare response data and cache it
            users_response = [
                UserResponseSchema.model_validate(u).model_dump(mode="json")
                for u in users
            ]
            await redis_client.set(cache_key, json.dumps(users_response), ex=3600)

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
