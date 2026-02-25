from app.db.base import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime
from enum import Enum as pyEnum
from datetime import datetime


class Role(pyEnum):
    """
    Enumeration of user roles within the system.
    """

    CONSUMER = "Consumer"
    SELLER = "Seller"


class User(Base):
    """
    SQLAlchemy model representing a User in the database.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    role = Column(Enum(Role, name="role_enum"), default=Role.CONSUMER, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
