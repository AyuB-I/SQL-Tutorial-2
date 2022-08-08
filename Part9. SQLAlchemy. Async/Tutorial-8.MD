# SQLAlchemy. Async

## Asnyc Engine

To allow asyncronous execution of queries, we need to use async engine, and asyncrounous library (`asyncpg`).
We have installed it earlier in previous tutorials.

Let's look again at how we create our sync engine.

```python
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

url = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using
    username='testuser',
    password='testpassword',
    host='localhost',
    database='testuser',
    port=5433
)
engine = create_engine(url, future=True)
```

Now, we just replace the regular `create_engine` with `create_async_engine` from `sqlalchemy.ext.asyncio`.

Also, we changed the library from `psycopg2` to `asyncpg` in the URL `drivername`.

```python
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.engine.url import URL

url = URL.create(
    drivername="postgresql+asyncpg",  # driver name = postgresql + the library we are using
    username='testuser',
    password='testpassword',
    host='localhost',
    database='testuser',
    port=5433
)
async_engine = create_async_engine(url, future=True)
```

Cool! Now an instance of `AsyncEngine` will be used as an engine.

## Async Session

That's not all. We also need to use async session instead of a regular session.

We have created our sessions in place by calling sessionmaker instance, that provided us with a session (context
manager).

```python
from sqlalchemy.orm import Session

session_pool = sessionmaker(bind=engine)
with session_pool() as session:
    session: Session  # It is a Session instance
    ...
    # run come code
# exit session
```

To make session async, we have to pass a class `AsyncSession` to the session maker function (parameter `class_`. It will
use it as a base class for the session, instead of `Session`.

> **Note:** To use async context manager while acquiring session, we **must** use `async with` statement.

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


session_pool = sessionmaker(bind=async_engine, class_=AsyncSession)

# Note async with
async with session_pool() as session:
    session: AsyncSession  # It is now an AsyncSession instance
    ...
    # run come code
```

## Async Query

Now, when we have async session, we have to `await` all queries.

> **Note:** The `await` is needed to obtain result, and only **after that** we can use `.first()` or `.all()` methods 
> on resulting objects.

Let's see how we can implement it in our previous example. We will adapt our `show_users_orders` function to use async.
#### Example
```python
# We use async context manager
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

    for order in orders:
        print(order.full_name, order.order_id)
```

#### Result

```
Test User 1
Test User 2 2
Test User 3 3
Test User 4 4
Test User 6 5
Test User 8 6
Test User 7
```

That's pretty much it.