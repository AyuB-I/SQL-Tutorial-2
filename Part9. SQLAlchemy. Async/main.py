import asyncio

from sqlalchemy import select
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import User, Order


async def main():
    url = URL.create(
        drivername="postgresql+asyncpg",  # driver name = postgresql + the library we are using
        username='testuser',
        password='testpassword',
        host='localhost',
        database='testuser',
        port=5439
    )
    async_engine = create_async_engine(url, future=True, echo=True)
    session_pool = sessionmaker(bind=async_engine, class_=AsyncSession)

    async with session_pool() as session:
        user_orders = select(
            Order.order_id, User.full_name
        ).join(
            User
        )
        # We 'await' the execute method
        result = await session.execute(user_orders)

        # Now we can use `.first()` or `.all()` methods on the result.
        orders = result.all()
        await session.commit()

    for order in orders:
        print(order.full_name, order.order_id)


if __name__ == '__main__':
    asyncio.run(main())
