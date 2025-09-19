from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Schema para login de usuário"""
    username: str
    password: str

class Token(BaseModel):
    """Schema para token de acesso"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema para dados do token"""
    username: Optional[str] = None
