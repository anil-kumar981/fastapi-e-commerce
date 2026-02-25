from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import UserRepo
from app.dependencies.db_depend import get_db
from app.services.user_service import UserService


async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepo(db)


async def get_user_service(user_repo: UserRepo = Depends(get_user_repo)):
    return UserService(user_repo)
