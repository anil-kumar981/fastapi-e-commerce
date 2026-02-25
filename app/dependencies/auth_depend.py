from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.common import decode_access_token
from app.schemas import TokenData
from app.models import Role, User
from app.dependencies.user_depend import get_user_repo
from app.repository import UserRepo
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepo = Depends(get_user_repo),
) -> User:
    """
    FastAPI dependency to retrieve the current authenticated user from the JWT token.

    Args:
        token (str): The JWT bearer token provided in the Authorization header.
        user_repo (UserRepo): The user repository instance.

    Returns:
        User: The authenticated user object from the database.

    Raises:
        HTTPException: 401 Unauthorized if the token is invalid, expired, or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = str(user_id)
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    if token_data.id is None:
        raise credentials_exception

    user = await user_repo.get_user_by_id(int(token_data.id))
    if user is None:
        raise credentials_exception
    return user


class RoleChecker:
    """
    Dependency to check if the authenticated user has the required roles.
    """

    def __init__(self, allowed_roles: List[Role]):
        """
        Initialize the role checker with allowed roles.

        Args:
            allowed_roles (List[Role]): The list of roles permitted to access the resource.
        """
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        """
        Verify the user's role against the allowed roles.

        Args:
            user (User): The current authenticated user.

        Returns:
            User: The user if they have the required role.

        Raises:
            HTTPException: 403 Forbidden if the user's role is not authorized.
        """
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to access this resource",
            )
        return user
