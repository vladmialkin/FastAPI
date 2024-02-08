from .base import Base
from sqlalchemy import Column, Integer, ForeignKey


class ShopCategoryAssociation(Base):
    __tablename__ = 'shop_category_association'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('shops.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
