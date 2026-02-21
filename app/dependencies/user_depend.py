from fastapi import Depends
from sqlalchemy.orm import Session
from app.repository import UserRepo
from app.dependencies.db_depend import get_db
from app.services.user_service import UserService


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepo(db)


def get_user_service(user_repo: UserRepo = Depends(get_user_repo)):
    return UserService(user_repo)
