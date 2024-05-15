# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    transactions: List["Transaction"] = []

    class Config:
        from_attributes = True  # Обновлено

class TransactionBase(BaseModel):
    amount: float
    category: str
    date: datetime

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Обновлено
