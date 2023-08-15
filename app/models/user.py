from sqlalchemy import Column, Table, Integer, VARCHAR, ForeignKey, Boolean
from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(VARCHAR(100), nullable=False, unique=True)
    full_name = Column(VARCHAR(100))
    email = Column(VARCHAR, nullable=False)
    disabled = Column(Boolean, default=False)


class UserPassword(BaseModel):
    __tablename__ = 'user_passwords'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    password_hash = Column(VARCHAR(100), nullable=False)


