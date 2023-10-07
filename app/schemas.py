from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class AccountsBase(BaseModel):
    cash: float
    bank: float


class AccountOut(BaseModel):
    pass


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    currency: str
    city: str
    phone_no: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TransactionBase(BaseModel):
    transaction_type: str
    account_type: str
    amount: float
    category: str
    timestamp: datetime


class InvestableBase(BaseModel):
    investable_percent: int


# for user bata aune token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
