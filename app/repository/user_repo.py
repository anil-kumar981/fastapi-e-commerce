from app.repository.base_repo import BaseRepo
from app.models.user_model import User
from app.schemas.user_schema import UserCreateSchema
from typing import List


class UserRepo(BaseRepo):
    def create_user(self, user: UserCreateSchema) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            house_number=user.house_number,
            street=user.street,
            city=user.city,
            state=user.state,
            postal_code=user.postal_code,
            country=user.country,
            phone_number=user.phone_number,
            role=user.role,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()
