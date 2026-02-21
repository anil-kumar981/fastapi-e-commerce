from app.db.base import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime
from enum import Enum as pyEnum
from datetime import datetime


class Role(pyEnum):
    CONSUMER = "Consumer"
    SELLER = "Seller"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    house_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(Enum(Role, name="role_enum"), default=Role.CONSUMER, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
