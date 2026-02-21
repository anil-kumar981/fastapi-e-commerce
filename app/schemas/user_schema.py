from pydantic import BaseModel, ConfigDict
from app.models import Role


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    house_number: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    phone_number: str
    role: Role


class UserResponseSchema(UserCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
