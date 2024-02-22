import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.handlers import user_router, bank_account_router, product_router, category_router
from app.rabbitmq.consumer import rabbitmq_router

#  Создание экземпляра приложения

app = FastAPI(title="Мой проект")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user', tags=['user'])
main_api_router.include_router(bank_account_router, prefix='/bank_account', tags=['bank_account'])
main_api_router.include_router(rabbitmq_router, prefix='/order', tags=['order'])
main_api_router.include_router(product_router, prefix='/product', tags=['product'])
main_api_router.include_router(category_router, prefix='/category', tags=['category'])
app.include_router(main_api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.2', port=8000, reload=True)