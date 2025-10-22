from sqlalchemy import Column, Integer, String, Enum, Boolean,DateTime
from app.database.base import Base 
from sqlalchemy.orm import Session,relationship
from app.database.enum import RoleEnum
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role=Column(Enum(RoleEnum), default=RoleEnum.user)
    join_date=Column(DateTime, default=datetime.utcnow, nullable=False)
   

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    jti = Column(String, primary_key=True)
    revoked_at = Column(DateTime, default=datetime.utcnow)


