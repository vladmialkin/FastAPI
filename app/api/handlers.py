from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import BankAccount, User
from app.db.session import get_db
from .schemas import CreateUser, ShowUser, InfoBankAccount, BankAccountRequest, CreateBankAccount, ShowBankAccount

user_router = APIRouter()  # создание router для User
bank_account_router = APIRouter()


async def _create_new_user(body: CreateUser, db: AsyncSession) -> ShowUser:
    try:
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="Ошибка создания пользователя")


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


async def _transaction_bank_account(body: BankAccountRequest, db: AsyncSession) -> InfoBankAccount:
    try:
        async with db.begin():
            #  Создание 2 аккаунтов
            for account in body.accounts:
                create_new_account = BankAccount(user_id=account.user_id, balance=account.balance)
                db.add(create_new_account)
            await db.flush()
            #  Вывод всех аккаунтов
            query = select(BankAccount)
            res = await db.execute(query)
            res_row = res.fetchall()
            accounts = [
                ShowBankAccount(account_id=value[0].id, user_id=value[0].user_id, balance=value[0].balance) for
                value in res_row]
            update_account = accounts[0]
            delete_account = accounts[1]
            # Изменение balance аккаунта
            query = update(BankAccount).where(BankAccount.id == update_account.account_id).values(
                balance=1000).returning(BankAccount)
            res = await db.execute(query)
            row_res = res.fetchone()[0]
            updated_account = ShowBankAccount(account_id=row_res.id, user_id=row_res.user_id, balance=row_res.balance)
            # Удаление аккаунта
            query = delete(BankAccount).where(BankAccount.id == delete_account.account_id)
            await db.execute(query)
            #  Вывод всех оставшихся аккаунтов
            query = select(BankAccount)
            res = await db.execute(query)
            last_accounts = [
                ShowBankAccount(account_id=value[0].id, user_id=value[0].user_id, balance=value[0].balance) for
                value in res.fetchall()]
            return InfoBankAccount(accounts=accounts, update_account=update_account, updated_account=updated_account,
                                   delete_account=delete_account,
                                   last_accounts=last_accounts)
    except Exception as error:
        print(error)


@user_router.post('/', response_model=CreateUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.get('/', response_model=ShowUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _get_user(user_id, db)


@bank_account_router.post('/', response_model=InfoBankAccount)
async def transaction_bank_account(body: BankAccountRequest, db: AsyncSession = Depends(get_db)) -> InfoBankAccount:
    return await _transaction_bank_account(body, db)
