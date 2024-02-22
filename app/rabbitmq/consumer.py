import json
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .connecting import channel, connection
from pydantic import BaseModel
from app.api.schemas import ShowProductOnOrder, ShowProduct
from app.db.models import Order
from ..db.session import get_db

rabbitmq_router = APIRouter()


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class CreateOrder(BaseModel):
    customer_id: int
    total_amount: float
    products: List[ShowProductOnOrder]


class ShowOrder(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    products: List[ShowProduct]


async def _get_orders(db: AsyncSession):
    try:
        query = select(Order)
        res = await db.execute(query)
        return res.fetchall()

    except Exception as e:
        print(e)


@rabbitmq_router.post('/', response_model=CreateOrder)
async def create_order(body: CreateOrder):
    channel.basic_publish(exchange='', routing_key='new_orders_queue', body=json.dumps(body))
    return {"message": "Заказ создан"}


@rabbitmq_router.get('/')
async def create_order(db: AsyncSession = Depends(get_db)):
    return await _get_orders(db)
