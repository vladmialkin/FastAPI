from .base import Base
from sqlalchemy import Column, Integer, ForeignKey, Table

shop_category_association = Table(
    'shop_category_association', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', ForeignKey('shops.id'), nullable=False),
    Column('category_id', ForeignKey('categories.id'), nullable=False)
)
