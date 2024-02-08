from .base import Base
from .shop_category_association import shop_category_association
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    products = relationship("Product", back_populates='category')
    shops = relationship("Shop", secondary=shop_category_association, back_populates='categories')

