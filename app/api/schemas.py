from typing import List, Union, Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import field_validator
from datetime import datetime, date


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class ShowUser(TunedModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: date
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: date


class CreateBankAccount(BaseModel):
    user_id: int
    balance: float


class ShowBankAccount(BaseModel):
    account_id: int
    user_id: int
    balance: float

    @field_validator('balance')
    @classmethod
    def check_balance(cls, value):
        if value is not None:
            if value < 0.0:
                raise ValueError("Баланс не может быть отрицательным числом.")
            return value
        return value


class InfoBankAccount(BaseModel):
    accounts: List[ShowBankAccount]
    update_account: ShowBankAccount
    updated_account: ShowBankAccount
    delete_account: ShowBankAccount
    last_accounts: List[ShowBankAccount]


class BankAccountRequest(TunedModel):
    accounts: List[CreateBankAccount]


class CreateProduct(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category_id: int


class ShowProduct(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category_id: int


class ShowProductOnOrder(BaseModel):
    product_id: int


class CreateOrder(BaseModel):
    customer_id: int
    total_amount: float
    products: List[ShowProductOnOrder]


class ShowOrder(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    products: List[ShowProduct]


class ShowCategory(BaseModel):
    id: int
    name: str
