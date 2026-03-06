from app.common.response import ResponseFactory
from app.repository import UserRepo
from app.schemas import (
    UserResponseSchema,
    UserCreateSchema,
    UserRegisterSchema,
    UserLoginSchema,
)
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.common import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from typing import cast
from app.core.redis import redis_client


class AuthService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def register(self, user: UserRegisterSchema) -> JSONResponse:
        """
        Register a new user, hash their password, and generate an access token.

        Args:
            user (UserRegisterSchema): The registration data provided by the user.

        Returns:
            JSONResponse: A standardized success response containing user data and access token.

        Raises:
            HTTPException: 400 if user exists or creation fails, 500 for server errors.
        """
        try:
            existing_user = await self.repo.get_user_by_email(user.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")

            # Create a copy of the user data and hash the password
            user_data = user.model_dump()
            user_data["password"] = get_password_hash(user_data["password"])

            # Map registration data to the creation schema
            user_create = UserCreateSchema(**user_data)

            result = await self.repo.create_user(user_create)
            if not result:
                raise HTTPException(status_code=400, detail="User not created")

            keys = await redis_client.keys("users:page:*")
            if keys:
                await redis_client.delete(*keys)

            # Token Generation
            token = create_access_token({"sub": str(result.id), "role": result.role})

            return ResponseFactory.success(
                data={
                    "user": UserResponseSchema.model_validate(result),
                    "access_token": token,
                },
                message="User registered successfully",
                status_code=201,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def login(self, user: UserLoginSchema) -> JSONResponse:
        """
        Authenticate a user and generate a new access token.

        Args:
            user (UserLoginSchema): The login credentials (email and password).

        Returns:
            JSONResponse: A standardized success response containing user data and access token.

        Raises:
            HTTPException: 400 for invalid credentials, 500 for server errors.
        """
        try:
            db_user = await self.repo.get_user_by_email(user.email)
            if not db_user:
                raise HTTPException(status_code=400, detail="Invalid email or password")

            # Verify the plain password against the stored hash
            if not verify_password(user.password, cast(str, db_user.password)):
                raise HTTPException(status_code=400, detail="Invalid password")

            token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
            # Return the user data (excluding password via schema)
            return ResponseFactory.success(
                data={
                    "user": UserResponseSchema.model_validate(db_user),
                    "access_token": token,
                },
                message="Login successful",
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
