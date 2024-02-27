import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.handlers import user_router, bank_account_router, product_router, category_router
# from rabbitmq.producer import rabbitmq_router
import logging

# получение пользовательского логгера и установка уровня логирования
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
py_logger.addHandler(py_handler)

my_app = FastAPI(title="Мой проект")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user', tags=['user'])
main_api_router.include_router(bank_account_router, prefix='/bank_account', tags=['bank_account'])
# main_api_router.include_router(rabbitmq_router, prefix='/order', tags=['order'])
main_api_router.include_router(product_router, prefix='/product', tags=['product'])
main_api_router.include_router(category_router, prefix='/category', tags=['category'])
my_app.include_router(main_api_router)

if __name__ == '__main__':
    py_logger.info("Start app")
    uvicorn.run("main:my_app", host='127.0.0.2', port=8000, reload=True)