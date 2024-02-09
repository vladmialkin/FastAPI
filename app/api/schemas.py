from typing import List

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
