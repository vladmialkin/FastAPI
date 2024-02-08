from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.users import User
from app.db.session import get_db
from .schemas import CreateUser, ShowUser

user_router = APIRouter()  # создание router для User


async def create_new_user(body: CreateUser, db: AsyncSession) -> ShowUser:
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


@user_router.post('/', response_model=CreateUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await create_new_user(body, db)
