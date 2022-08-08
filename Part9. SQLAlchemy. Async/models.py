from sqlalchemy import Column, Integer, BIGINT, VARCHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(BIGINT, primary_key=True)
    full_name = Column(VARCHAR(255), nullable=False)
    username = Column(VARCHAR(255))
    language_code = Column(VARCHAR(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    referrer_id = Column(BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL'))

    # phone_number = Column(VARCHAR(50))


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(3000), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class OrderProduct(Base):
    __tablename__ = 'order_products'

    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='RESTRICT'), primary_key=True)
    quantity = Column(Integer, nullable=False)

