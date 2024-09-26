from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    amount: int
    description: str
    
class ExpenseCreate(ExpenseBase):
    pass
    
    
class Expense(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
