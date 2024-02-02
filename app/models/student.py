from core import *


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime(timezone=True))
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    enrollment_date = Column(DateTime(timezone=True))
    major = Column(String)
