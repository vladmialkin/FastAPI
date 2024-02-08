from envparse import Env
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

env = Env()


REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)  # подключение к БД (асинхронное)
