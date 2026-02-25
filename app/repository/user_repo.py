from app.repository.base_repo import BaseRepo
from app.models.user_model import User
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepo(BaseRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create_user(self, user: UserCreateSchema) -> User:
        """
        Create a new user record in the database.

        Args:
            user (UserCreateSchema): The schema containing the user creation data.

        Returns:
            User: The newly created User model instance.
        """
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(self, user_id: int, user: UserUpdateSchema) -> Optional[User]:
        """
        Update an existing user record.

        Args:
            user_id (int): The ID of the user to update.
            user (UserUpdateSchema): The schema containing the fields to update.

        Returns:
            Optional[User]: The updated User instance if found, otherwise None.
        """
        # Fetch the existing user
        result = await self.db.execute(select(User).filter(User.id == user_id))
        db_user = result.scalars().first()

        if not db_user:
            return None

        # Dynamically update only the fields that were set in the schema
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user record from the database by its email address.

        Args:
            email (str): The email address to look up.

        Returns:
            Optional[User]: The User instance if found, otherwise None.
        """
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_all_users(self) -> List[User]:
        """
        Retrieve all user records from the database.

        Returns:
            List[User]: A list of all User model instances.
        """
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user record from the database by its unique identifier.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            Optional[User]: The User instance if found, otherwise None.
        """
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
