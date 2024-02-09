from .base import Base
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Float, nullable=False)

    customer = relationship("User", back_populates='orders')
