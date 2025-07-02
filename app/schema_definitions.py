from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRole(str, Enum):
    OPS = "OPS"
    CLIENT = "CLIENT"
    
print("in schema file")

# 🧾 Request model for user signup
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

# 🧾 Login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ Response model for showing user
class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True

# 🔐 Token response (after login)
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
