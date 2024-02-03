from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, INT, DateTime
from database import Base

metadata = MetaData()


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


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def check_adult(self):
        adult = {self.age >= 18}
        return {'first_name': self.first_name, 'last_name': self.last_name, 'age': self.age, 'adult': adult}
