from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

from app.db.models import BankAccount, User, Order, Product, Category, ProductsOnOrder
from app.db.session import get_db, get_async_session
from .schemas import CreateUser, ShowUser, InfoBankAccount, BankAccountRequest, CreateBankAccount, ShowBankAccount, \
    CreateOrder, ShowOrder, CreateProduct, ShowProduct, ShowCategory

user_router = APIRouter()  # создание router для User
bank_account_router = APIRouter()
order_router = APIRouter()
product_router = APIRouter()
category_router = APIRouter()


async def _create_new_user(body: CreateUser, db: AsyncSession) -> ShowUser:
    """
    Функиция создает нового пользлвателя и возвращает его.
    body: данные пользователя
    db: сессия дб
    """
    try:
        async with db.begin():
            new_user = User(first_name=body.first_name,
                            last_name=body.last_name,
                            email=body.email,
                            date_of_birth=body.date_of_birth)
            # добавить пользователя в бд
            db.add(new_user)
            # подтвердить добавление
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
    """
    Функция ищет пользователя по его id.
    """
    try:
        async with db.begin():
            # запрос на получение пользователя
            query = select(User).where(User.id == user_id)
            # выполнение запроса в бд
            res = await db.execute(query)
            # получение результата
            user_row = res.fetchone()
            if user_row is not None:
                # вывод данных, если результат запроса не пустой
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
                # вывод ошибки, если пользователя с введенным id не существует
                raise HTTPException(status_code=404, detail=f"Пользователя с id {user_id} не существует.")
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))


async def _transaction_bank_account(body: BankAccountRequest, db: AsyncSession) -> InfoBankAccount:
    """
    Функция работы с банковскими аккаунтами
    """
    try:
        async with db.begin():
            #  Создание 2 аккаунтов
            for account in body.accounts:
                create_new_account = BankAccount(user_id=account.user_id, balance=account.balance)
                db.add(create_new_account)

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
            # подтверждение действий в бд
            await db.flush()
            return InfoBankAccount(accounts=accounts, update_account=update_account, updated_account=updated_account,
                                   delete_account=delete_account,
                                   last_accounts=last_accounts)
    except exc.IntegrityError:
        # ошибка при создании аккаунта пользователю, у которого уже существует аккаунт
        raise HTTPException(status_code=422, detail='Один из пользователей уже имеет банковский счёт.')


async def _create_order(body: CreateOrder, db: AsyncSession) -> ShowOrder:
    """
    Функция создания заказа
    """

    try:
        async with db.begin():
            # создание заказа
            new_order = Order(customer_id=body.customer_id,
                              total_amount=body.total_amount)
            db.add(new_order)

            await db.flush()
            products = []
            # получение данных по каждому продукту, созданного заказа
            for product in body.products:
                product_on_order = ProductsOnOrder(order_id=new_order.id, product_id=product.product_id)
                query = select(Product).where(Product.id == product.product_id)
                res = await db.execute(query)
                product = res.fetchone()[0]
                products.append(ShowProduct(name=product.name,
                                            description=product.description,
                                            price=product.price,
                                            category_id=product.category_id))
                db.add(product_on_order)
                await db.flush()
            return ShowOrder(id=new_order.id,
                             customer_id=new_order.customer_id,
                             total_amount=new_order.total_amount,
                             created_at=new_order.created_at,
                             updated_at=new_order.updated_at,
                             closed_at=new_order.closed_at,
                             products=products
                             )
    except Exception as e:
        # вывод ошибок
        print(e)


async def _create_product(body: CreateProduct, db: AsyncSession) -> ShowProduct:
    """
    Функция создания продукта
    """
    try:
        async with db.begin():
            new_product = Product(name=body.name,
                                  description=body.description,
                                  price=body.price,
                                  category_id=body.category_id
                                  )
            db.add(new_product)
            await db.flush()
            return ShowProduct(name=new_product.name,
                               description=new_product.description,
                               price=new_product.price,
                               category_id=new_product.category_id
                               )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail=str(e))


async def _show_products(db: AsyncSession):
    """
    Функция получения всех продуктов
    """

    try:
        async with db.begin():
            query = select(Product)
            res = await db.execute(query)
            products = []
            for val in res.fetchall():
                val = val[0]
                products.append(ShowProduct(name=val.name, description=val.description, price=val.price,
                                            category_id=val.category_id))
            return products

    except Exception as e:
        print(e)


async def _create_category(name: str, db: AsyncSession) -> ShowCategory:
    """
    Функция создания категории
    """
    try:
        async with db.begin():
            new_category = Category(name=name)
            db.add(new_category)
            await db.flush()
            return ShowCategory(id=new_category.id, name=new_category.name)
    except Exception as e:
        print(e)


async def _show_categories(db: AsyncSession):
    """
    Функция просмотра всех категорий
    """
    try:
        async with db.begin():
            query = select(Category)
            res = await db.execute(query)
            categories = []
            for val in res.fetchall():
                val = val[0]
                categories.append(ShowCategory(id=val.id, name=val.name))
            return categories
    except Exception as e:
        print(e)


@user_router.post('/', response_model=CreateUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_async_session)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.get('/', response_model=ShowUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)) -> ShowUser:
    return await _get_user(user_id, db)


@bank_account_router.post('/', response_model=InfoBankAccount)
async def transaction_bank_account(body: BankAccountRequest,
                                   db: AsyncSession = Depends(get_async_session)) -> InfoBankAccount:
    return await _transaction_bank_account(body, db)


@order_router.post('/', response_model=ShowOrder)
async def create_order(body: CreateOrder, db: AsyncSession = Depends(get_async_session)) -> ShowOrder:
    return await _create_order(body, db)


@product_router.post('/', response_model=ShowProduct)
async def create_product(body: CreateProduct, db: AsyncSession = Depends(get_async_session)) -> ShowProduct:
    return await _create_product(body, db)


@product_router.get('/')
async def show_products(db: AsyncSession = Depends(get_async_session)):
    return await _show_products(db)


@category_router.post('/', response_model=ShowCategory)
async def create_category(name: str, db: AsyncSession = Depends(get_async_session)) -> ShowCategory:
    return await _create_category(name, db)


@category_router.get('/')
async def show_categories(db: AsyncSession = Depends(get_async_session)):
    return await _show_categories(db)
