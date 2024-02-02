from core import *

Students = Table(
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