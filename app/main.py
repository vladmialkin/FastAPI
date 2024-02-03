from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Base
Base.metadata.create_all(bind=engine)

import crud
import schemas

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=schemas.Student)
def create_students(student: schemas.Student, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)
