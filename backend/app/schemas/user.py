from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        # Bcrypt has a 72 byte limit, check byte length
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError('Senha muito longa (máximo 72 bytes). Use uma senha mais curta.')
        return v
    
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

