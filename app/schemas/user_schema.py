from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from app.models import Role
from app.common import validate_password


class UserBase(BaseModel):
    """
    Base schema for user fields shared between creation and updates.
    """

    house_number: str | None = Field(None, min_length=3, max_length=50)
    street: str | None = Field(None, min_length=3, max_length=50)
    city: str | None = Field(None, min_length=3, max_length=50)
    state: str | None = Field(None, min_length=3, max_length=50)
    postal_code: str | None = Field(None, min_length=3, max_length=50)
    country: str | None = Field(None, min_length=3, max_length=50)
    phone_number: str | None = Field(
        None, min_length=10, max_length=15, pattern=r"^[0-9]{10}$"
    )
    role: Role = Field(default=Role.CONSUMER)


class UserCreateSchema(UserBase):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserUpdateSchema(UserBase):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=72)


class UserResponseSchema(UserBase):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
