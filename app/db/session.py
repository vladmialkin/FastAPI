from typing import Generator, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ..settings import REAL_DATABASE_URL

# Подключение к БД

engine = create_async_engine(REAL_DATABASE_URL, future=True, echo=True)

async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session_maker()
        yield session
    finally:
        await session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
