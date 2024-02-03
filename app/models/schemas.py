from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    age: int


class Student(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    date_of_birth: datetime | None
    email: str
    phone_number: str
    enrollment_date: datetime | None
    major: str

