from .base import Base
from .shop_category_association import ShopCategoryAssociation
from sqlalchemy import Column, Boolean, String, Integer, DateTime, func, Text, Float
from sqlalchemy.orm import relationship


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())

    categories = relationship('Category', secondary=ShopCategoryAssociation, back_populates="shops")