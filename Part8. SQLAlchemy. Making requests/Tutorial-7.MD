# SQLAlchemy. Making requests

## Translating raw SQL into SQLAlchemy queries

So you've learned how to create tables with SQLAlchemy, and now it is time to learn how to use them to build queries.

The syntax is very similar to SQL, so let's repeat the first example from the lesson about Relationships.

```postgresql
INSERT INTO users
    (telegram_id, full_name, username, language_code, created_at)
VALUES (1, 'John Doe', 'johnny', 'en', '2020-01-01');
```

Now magic is going to happen.

- In order to make the same query, we can use the `insert()` method from the SQLAlchemy.
- To pass the values, we can use the `values` method after the `insert` method, and pass each value as a keyword
  argument.

> **Note:**
>
> We've put our tables' declaration into the `models.py` file (a table can be also called a _'model'_)

```python
import datetime
from models import User, Product, OrderProduct, Order
from sqlalchemy import insert

stmt = insert(
    User
).values(
    telegram_id=1,
    full_name='John Doe',
    username='johnny',
    language_code='en',
    created_at=datetime.date(2020, 1, 1),
)
```

So every time we want to use an SQL command, we can import it by the same name from the `sqlalchemy` module:

[//]: # (- `SELECT` - `select&#40;&#41;`)

[//]: # (- `INSERT` - `insert&#40;&#41;`)

[//]: # (- `UPDATE` - `update&#40;&#41;`)

[//]: # (- `DELETE` - `delete&#40;&#41;`)

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT</code></td><td><code>select()</code></td></tr>
<tr><td><code>INSERT</code></td><td><code>insert()</code></td></tr>
<tr><td><code>UPDATE</code></td><td><code>update()</code></td></tr>
<tr><td><code>DELETE</code></td><td><code>delete()</code></td></tr>
</tbody>
</table>


To specify the table in the `FROM` clause, we use the `class` of the table as an argument to that method:
<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users</code></td><td><code>select(User)</code></td></tr>
<tr><td><code>INSERT INTO users ...</code></td><td><code>insert(User)</code></td></tr>
<tr><td><code>UPDATE users SET ...</code></td><td><code>update(User)</code></td></tr>
</tbody>
</table>

Whether we want to select specific columns, we can use the respective attribute from the table class:
<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT users.telegram_id ...</code></td><td><code>select(User.telegram_id)</code></td></tr>
<tr><td><code>SELECT users.full_name ...</code></td><td><code>select(User.full_name)</code></td></tr>
<tr><td><code>SELECT users.username, users.language_code ...</code></td><td><code>select(User.username, User.language_code)</code></td></tr>
</tbody>
</table>

To use additional SQL expressions we will use the method (with the similar name) from the resulting object:
<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users WHERE ... </code></td><td><code>select(User).where(...)</code></td></tr>
<tr><td><code>INSERT INTO users ... VALUES ...</code></td><td><code>insert(User).values(...)</code></td></tr>
<tr><td><code>UPDATE users SET ... WHERE ...</code></td><td><code>update(User).values(...).where(...)</code></td></tr>
<tr><td><code>DELETE FROM users WHERE ...</code></td><td><code>delete(User).where(...)</code></td></tr>
</tbody>
</table>

### Where

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users WHERE users.telegram_id = 1</code></td><td><code>select(User).where(User.telegram_id == 1)</code></td></tr>
<tr><td><code>SELECT ... FROM users WHERE users.full_name = 'John Doe'</code></td><td><code>select(User).where(User.full_name == 'John Doe')</code></td></tr>
<tr><td><code>SELECT ... FROM users WHERE users.created_at > '2020-01-01'</code></td><td><code>select(User).where(User.created_at > datetime.date(2020, 1, 1))</code></td></tr>
</tbody>
</table>

### Join

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users JOIN products ON users.id = products.user_id</code></td><td><code>select(User).join(Product, User.id == Product.user_id)</code></td></tr>
</tbody>
</table>

### Group by

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users GROUP BY users.language_code</code></td><td><code>select(User).group_by(User.language_code)</code></td></tr>
</tbody>
</table>

### Order by

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users ORDER BY users.telegram_id</code></td><td><code>select(User).order_by(User.telegram_id)</code></td></tr>
<tr><td><code>SELECT ... FROM users ORDER BY users.full_name DESC</code></td><td><code>select(User).order_by(User.full_name.desc())</code></td></tr>
<tr><td><code>SELECT ... FROM users ORDER BY users.created_at ASC</code></td><td><code>select(User).order_by(User.created_at.asc())</code></td></tr>
</tbody>
</table>

### Limit

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users LIMIT 10</code></td><td><code>select(User).limit(10)</code></td></tr>
</tbody>
</table>

### Offset

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users OFFSET 10</code></td><td><code>select(User).offset(10)</code></td></tr>
</tbody>
</table>

### Having

<table>
<thead>
<tr><th>Command</th><th>Method</th></tr>
</thead>
<tbody>
<tr><td><code>SELECT ... FROM users HAVING ... </code></td><td><code>select(User).having(...)</code></td></tr>
</tbody>
</table>

### Joining with multiple tables

```postgresql
SELECT *
FROM users
         JOIN orders ON orders.user_id = users.telegram_id
         JOIN order_products ON order_products.order_id = orders.order_id
         JOIN products ON products.product_id = order_products.product_id = products.product_id

```

Goes like this:

```python
select(
    User, Order, OrderProduct, Product
).join(
    Order,
    Order.user_id == User.telegram_id
).join(
    OrderProduct,
    OrderProduct.order_id == Order.order_id
).join(
    Product,
    Product.product_id == OrderProduct.product_id
)
```

### Multiple conditions:

```
SELECT ... 
FROM users 
WHERE users.telegram_id = 1 
AND users.language_code = 'en'
```

You just iterate through the conditions like this:

```python
select(
    User
).where(
    User.telegram_id == 1,
    User.language_code == 'en'
)
```

### Multiple conditions with OR:

```
SELECT ... 
FROM users 
WHERE users.telegram_id = 1 
OR users.language_code = 'en'
```

You need to use the `or_()` function from `sqlalchemy` module, and pass the conditions as arguments:

```python
select(
    User
).where(
    or_(
        User.telegram_id == 1,
        User.language_code == 'en'
    )
)
```

## Examples from previous lessons

Let's see how we can create other examples from the previous lessons:

### SQL (reiterate)

```postgresql
INSERT INTO users
    (telegram_id, full_name, username, language_code, created_at)
VALUES (1, 'John Doe', 'johnny', 'en', '2020-01-01');
-- 1. Insert a new user


INSERT INTO users
(telegram_id, full_name, username, language_code, created_at, referrer_id)
VALUES (2, 'Jane Doe', 'jane', 'en', '2020-01-02', 1);
-- 2. Insert a user with a referrer


SELECT users.full_name AS "user", ref.full_name AS referrer
FROM users
         JOIN users AS ref ON ref.telegram_id = users.referrer_id;
-- 3. Get full names of the user and the referrer

SELECT users.full_name AS "user", ref.full_name AS referrer
FROM users
         LEFT OUTER JOIN users AS ref ON ref.telegram_id = users.referrer_id;
-- 4. Get full names of all users and their referrer, but if the referrer is not set, use the value `NULL`

SELECT users.full_name AS "user", ref.full_name AS referrer
FROM users
         RIGHT JOIN users AS ref ON ref.telegram_id = users.referrer_id;
-- 5. Get full names of users and all referrers, but if the user is not set, use the value `NULL`

INSERT INTO orders (user_id)
VALUES (1)
RETURNING order_id;
-- 6. Insert an order for the user with id 1


SELECT orders.order_id, users.full_name
FROM orders
         JOIN users ON users.telegram_id = orders.user_id;
-- 7. Get the order id and the full name of the user for that order


INSERT INTO products (title, description)
VALUES ('Product 1', 'Description 1'),
       ('Product 2', 'Description 2'),
       ('Product 3', 'Description 3');
-- 8. Insert three products

INSERT INTO order_products (order_id, product_id, quantity)
VALUES (1, 1, 1),
       (1, 2, 2),
       (1, 3, 3);
-- 9. Insert three products for the order with id 1


SELECT orders.order_id, products.title as product_name, users.full_name
FROM order_products
         JOIN products ON products.product_id = order_products.product_id
         JOIN orders ON orders.order_id = order_products.order_id
         JOIN users ON users.telegram_id = orders.user_id;
-- 10. Get the order id, the product name and the full name of the user for each order
```

### Python

```python
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
```