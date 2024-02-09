from .base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class ProductsOnOrder(Base):
    __tablename__ = 'products_on_order'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    order = relationship("Order", back_populates='products_on_order')
    product = relationship("Product", back_populates='products_on_order')
