from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


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

