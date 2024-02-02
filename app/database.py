from config import DB_USER, DB_NAME, DB_PORT, DB_HOST, DB_PASS
from databases import Database


DATABASE_URL = F"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
database = Database(DATABASE_URL)


