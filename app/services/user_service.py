from app.repository import UserRepo
from app.schemas import UserCreateSchema, UserResponseSchema
from typing import List


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def create_user(self, user: UserCreateSchema) -> UserResponseSchema:
        return self.repo.create_user(user)

    def get_user_by_email(self, email: str) -> UserResponseSchema:
        data = self.repo.get_user_by_email(email)
        return UserResponseSchema.model_validate(data)

    def get_all_users(self) -> List[UserResponseSchema]:
        users = self.repo.get_all_users()
        users_response = [UserResponseSchema.model_validate(u) for u in users]
        return users_response
