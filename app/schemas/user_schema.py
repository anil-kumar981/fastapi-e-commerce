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
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str) -> str:
        return validate_password(v)


class UserUpdateSchema(UserBase):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_password(v)
        return v


class UserResponseSchema(UserCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
