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
