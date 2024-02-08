from base import Base
from shop_category_association import ShopCategoryAssociation
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    shops = relationship('Shop', secondary=ShopCategoryAssociation, back_populates="categories")
