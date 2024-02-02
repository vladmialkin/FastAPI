from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .database import database
from .models import User, Students

app = FastAPI()

user_data = {'id': 1, 'first_name': 'Vlad', 'last_name': 'Mialkin', 'age': 20}
user = User(**user_data)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/issue")
def read_issue():
    return FileResponse('templates/main.html')


@app.post("/calculate")
async def get_sum(num1: int | float, num2: int | float) -> dict[str, int | float]:
    return {"result": num1 + num2}


@app.post("/create_user")
async def create_user(user: User):
    print(f"Пользователь {user.first_name} {user.last_name} успешно создан!")
    return user


@app.get("/users")
async def create_user():
    return user.check_adult()


@app.post("/students/", response_model=Students)
async def create_students(student: Students):
    query = """INSERT INTO students(first_name, last_name, date_of_birth, email, phone_number, enrollment_date, major)
                VALUES(:first_name, :last_name, :date_of_birth, :email, :phone_number, :enrollment_date, :major)
                RETURNING id, first_name, last_name
    """
    values = {"first_name": student.first_name,
              'last_name': student.last_name,
              "date_of_birth": student.date_of_birth,
              "email": student.email,
              "phone_number": student.phone_number,
              "enrollment_date": student.enrollment_date,
              "major": student.major}
    try:
        student_id = await database.execute(query=query, values=values)
        return {**student.dict(), "id": student_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create student")