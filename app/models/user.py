from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func  # func nos da funciones SQL como now()
from app.database import Base  # Importamos la Base que definimos antes
from enum import Enum as Enum_base


class UserRole(str, Enum_base):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    avatar = Column(String(200), default="https://via.placeholder.com/150")
    password_hash = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
