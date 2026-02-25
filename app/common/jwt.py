from jose import jwt
from app.core.config import settings
from datetime import datetime, timedelta


def create_access_token(data: dict) -> str:
    """
    Create a new JWT access token with an expiration time.

    Args:
        data (dict): The payload to include in the token (e.g., user_id, roles).

    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=settings.JWT_TOKEN_EXPIRE_IN_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload if the token is valid.

    Raises:
        JWTError: If the token is invalid or has expired.
    """
    return jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
