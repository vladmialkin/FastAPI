import sqlalchemy
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.users import User
from app.db.session import get_db
from .schemas import CreateUser, ShowUser, GetUserResponse

user_router = APIRouter()  # создание router для User


async def _create_new_user(body: CreateUser, db: AsyncSession) -> ShowUser:
    async with db.begin():
        new_user = User(first_name=body.first_name,
                        last_name=body.last_name,
                        email=body.email,
                        date_of_birth=body.date_of_birth)
        db.add(new_user)
        await db.flush()
        return ShowUser(
            user_id=new_user.id,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            date_of_birth=new_user.date_of_birth,
            is_active=new_user.is_active,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at
        )


async def _get_user(user_id: int, db: AsyncSession) -> ShowUser:
    try:
        async with db.begin():
            query = select(User).where(User.id == user_id)
            res = await db.execute(query)
            user_row = res.fetchone()
            if user_row is not None:
                user = user_row[0]
                return ShowUser(
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    date_of_birth=user.date_of_birth,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
            else:
                raise HTTPException(status_code=404, detail=f"Пользователя с id {user_id} не существует.")
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))


@user_router.post('/', response_model=CreateUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.get('/', response_model=ShowUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _get_user(user_id, db)
