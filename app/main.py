import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.handlers import user_router
from api.handlers import bank_account_router

#  Создание экземпляра приложения

app = FastAPI(title="Мой проект")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user', tags=['user'])
main_api_router.include_router(bank_account_router, prefix='/bank_account', tags=['bank_account'])
app.include_router(main_api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.2', port=8000, reload=True)