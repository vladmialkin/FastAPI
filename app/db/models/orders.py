from .base import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)
    closed_at = Column(DateTime, onupdate=func.current_timestamp(), nullable=True)

    products_on_order = relationship("ProductsOnOrder", back_populates='order')
    customer = relationship("User", back_populates='orders')
