from envparse import Env
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, TEST_DB_HOST, TEST_DB_USER, TEST_DB_PASS, TEST_DB_PORT, \
    TEST_DB_NAME

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)  # подключение к БД (асинхронное)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f'postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
)  # подключение к БД (асинхронное)
