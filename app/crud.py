from sqlalchemy.orm import Session
import schemas

import models


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.Student):
    db_student = models.Student(first_name=student.first_name,
                                last_name=student.last_name,
                                date_of_birth=student.date_of_birth,
                                email=student.email,
                                phone_number=student.phone_number,
                                enrollment_date=student.enrollment_date,
                                major=student.major)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
