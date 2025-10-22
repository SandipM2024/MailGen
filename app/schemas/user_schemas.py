from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional,List
 
class UserBase(BaseModel):
    name: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str
    confirm_password: str
    

class UserResponse(UserBase):
    id: int
    join_date: datetime
    class Config:
        from_attributes = True  # Ensures automatic conversion
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Convert datetime to string
        }
class LoginRequest(BaseModel):
    email: str
    password: str

# Response schema for login
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role:str
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str


