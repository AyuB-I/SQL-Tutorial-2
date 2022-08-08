import datetime

from sqlalchemy import create_engine, bindparam
from sqlalchemy import insert, select
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, aliased, join

from models import User, Order, Product, OrderProduct


# Let's create a function that will insert a user into the database
def create_user(session, telegram_id, full_name, username, language_code, created_at, referrer_id=None):
    stmt = insert(User).values(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username,
        language_code=language_code,
        created_at=created_at,
        referrer_id=referrer_id,
    )
    session.execute(stmt)


def select_users_with_referrer(session):
    # Simple INNER JOIN

    # We need a new alias for the referrer table
    Referrer = aliased(User)
    stmt = select(
        User.full_name.label('user'),  # We can use 'label' to give an alias to the column
        Referrer.full_name.label('referrer'),
    ).join(
        Referrer,
        Referrer.telegram_id == User.referrer_id
    )
    return session.execute(stmt)


def select_all_users_and_some_referrers(session):
    # Left JOIN

    Referrer = aliased(User)
    stmt = select(
        User.full_name.label('user'),  # We can use 'label' to give an alias to the column
        Referrer.full_name.label('referrer'),
    ).join(
        Referrer,  # right join side
        Referrer.telegram_id == User.referrer_id,  # on clause
        isouter=True,  # outer join
    )
    return session.execute(stmt)


def select_some_users_and_all_referrers(session):
    # Right JOIN is a LEFT join, with tables swapped

    Referrer = aliased(User)
    stmt = select(
        User.full_name.label('user'),  # We can use 'label' to give an alias to the column
        Referrer.full_name.label('referrer'),
    ).select_from(
        join(
            Referrer,  # Making referrer the left join side for LEFT JOIN.
            User,
            onclause=Referrer.telegram_id == User.referrer_id,
            isouter=True,  # outer join
        )
    )
    return session.execute(stmt)


def create_new_order_for_user(session, user_id):
    new_order = insert(
        Order
    ).values(
        user_id=user_id,
    ).returning(Order.order_id)
    result = session.execute(new_order)
    return result.scalar()


def show_users_orders(session):
    user_orders = select(
        Order.order_id, User.full_name
    ).join(
        User  # We can skip on clause here, let SQLAlchemy figure it out
    )
    result = session.execute(user_orders)
    return result.all()


def create_new_products(session, products_info):
    new_products = insert(
        Product
    ).values(
        products_info
    ).returning(
        Product.product_id
    )
    result = session.execute(new_products)
    return result.scalars()


def add_products_to_order(session, order_id, product_data):
    stmt = insert(
        OrderProduct
    ).values(
        order_id=order_id,
        product_id=bindparam('product_id'),
        quantity=bindparam('quantity'),
    )
    session.execute(stmt, product_data)


def show_all_users_products(session):
    stmt = select(
        Order.order_id, Product.title, User.full_name
    ).select_from(
        OrderProduct
    ).join(
        Product, Product.product_id == OrderProduct.product_id
    ).join(
        Order, Order.order_id == OrderProduct.order_id,
    ).join(
        User, User.telegram_id == Order.user_id
    )
    result = session.execute(stmt)
    return result.all()


def main():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username='testuser',
        password='testpassword',
        host='localhost',
        database='testuser',
        port=5433)

    engine = create_engine(url, future=True)
    session_pool = sessionmaker(bind=engine)
    with session_pool() as session:
        # 1. Insert a new user
        create_user(session, 1, 'John Doe', 'johnny', 'en', datetime.date(2020, 1, 1))

        # 2. Insert a new user with a referrer
        create_user(session, 2, 'Jane Doe', 'jane', 'en', datetime.date(2020, 1, 2), 1)

        # 3. Get full names of the user and the referrer
        result = select_users_with_referrer(session)
        users_with_referrer = result.all()
        print('Users with referrer:')
        for row in users_with_referrer:
            print(f'User: {row.user=}, Referrer: {row.referrer=}')
        print()

        # 4. Get full names of all users and their referrer, but if the referrer is not set, use the value `NULL`
        result = select_all_users_and_some_referrers(session)
        all_users_and_referrers = result.all()
        print('All users and their referrers:')
        for row in all_users_and_referrers:
            print(f'User: {row.user=}, Referrer: {row.referrer=}')

        # 5. Get full names of users and all referrers, but if the user is not set, use the value `NULL`
        result = select_some_users_and_all_referrers(session)
        some_users_and_all_referrers = result.all()
        print()
        print('Some users and all their referrers:')
        for row in some_users_and_all_referrers:
            print(f'User: {row.user=}, Referrer: {row.referrer=}')

        print()

        # 6. Create a new order for user 1
        order_id = create_new_order_for_user(session, user_id=1)

        # 7. Get the order id and the full name of the user for that order
        users_orders = show_users_orders(session)
        print('Users orders:')
        for row in users_orders:
            print(f'Order ID: {row.order_id}, User: {row.full_name}')
        print()

        # 8. Insert three products
        product_ids = create_new_products(
            session,
            [
                {'title': 'Product 1', 'description': 'Description 1'},
                {'title': 'Product 2', 'description': 'Description 2'},
                {'title': 'Product 3', 'description': 'Description 3'},
            ]
        )
        product_ids = list(product_ids)
        print(f'Product ids: {product_ids}')
        print()

        # 9. Insert three products for the order with that order_id (now we don't know the order_id in advance)
        add_products_to_order(
            session,
            order_id=order_id,
            product_data=[
                dict(product_id=product_id, quantity=1)
                for product_id in product_ids
            ]
        )

        # 10. Get the order id, the product name and the full name of the user for each order
        users_products = show_all_users_products(session)
        print('Users products:')
        for row in users_products:
            print(f'Order ID: {row.order_id}, Title: {row.title}, User: {row.full_name}')


main()
