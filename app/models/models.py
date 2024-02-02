from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, INT, DateTime

# from datetime import datetime
# from typing import List, Union

metadata = MetaData()


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int

    def check_adult(self):
        adult = {self.age >= 18}
        return {'first_name': self.first_name, 'last_name': self.last_name, 'age': self.age, 'adult': adult}


students = Table(
    "students",
    metadata,
    Column("student_id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("date_of_birth", DateTime(timezone=True)),

    Column("email", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("enrollment_date", DateTime(timezone=True)),
    Column("major", String),

)
