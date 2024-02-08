from base import Base
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship


class Discount(Base):
    __tablename__ = 'discount'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product')
    discount_percentage = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)


