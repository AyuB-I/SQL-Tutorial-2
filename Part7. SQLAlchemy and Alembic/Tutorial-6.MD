# SQLAlchemy and Alembic

## Creating tables with SQLAlchemy

### ORM

So you know how to create tables in SQL, now you can use SQLAlchemy to create them. If you are not familiar with _Object
oriented programming_ (OOP) at this point, you have to learn it first, since we will be using  _Object Relational
Mapping_ (ORM) to create tables.

ORM is extremely useful because you can create Python objects and then use them to interact with the database. After
that, you will have access to your database tables as to python objects, and to tables' columns as to attributes of
these objects.

### Creating a table

To start creating tables, you will need a specific SQLAlchemy base class to inherit from, so SQLAlchemy will understand
how to map the results of your queries to Python objects.

This class is called declarative base and is created like this:

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

Now you can start creating tables as Python classes.

Do you remember how we created the users table in SQL?

```postgresql
CREATE TABLE users
(
    telegram_id   BIGINT PRIMARY KEY,
    full_name     VARCHAR(255) NOT NULL,
    username      VARCHAR(255),
    language_code VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT NOW(),
    referrer_id   BIGINT,
    FOREIGN KEY (referrer_id)
        REFERENCES users (telegram_id)
        ON DELETE SET NULL
);
```

Let's create a class to represent this table:

1. To create a table in SQLAlchemy, you need to create a class that inherits from the declarative base.
2. In order to create columns in the table, you need to create new attributes and assign them the `Column` class.
3. To use SQL data types you have to import specific objects from the `sqlalchemy` module. They usually have the same
   names. Examples: `BIGINT`, `VARCHAR`, `TIMESTAMP`.
4. To create a primary key, you need to pass the `primary_key` argument to the column.
5. To create a not null constraint, you need to pass the `nullable` argument to the column.
6. To create a default value, you need to pass the `server_default` argument to the column.
7. To create a foreign key, you need to pass the `ForeignKey` argument to the column and fill its arguments.
8. To use SQL expressions from SQLAlchemy you can use `sqlalchemy.sql.expression` module. For example, you can use
   `null()` or `false()` to create a default values `NULL` or `FALSE` for a column.
9. To use functions from SQLAlchemy you can use `sqlalchemy.func` module. For example, you can use `func.now()`
   to create a default `NOW()` value for a column.
10. To give a name to a table you must use the `__tablename__` attribute.

#### Example:

```python
from sqlalchemy import Column, BIGINT, VARCHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(BIGINT, primary_key=True)
    full_name = Column(VARCHAR(255), nullable=False)
    username = Column(VARCHAR(255))
    language_code = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    referrer_id = Column(BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL'))
```

You can see how easy it is done with SQLAlchemy. Just look and that beauty again.

Let's now make some more tables from the previous tutorials.

> **Note:** You can use autoincrement argument to create a SERIAL type column.

```python
from sqlalchemy import Column, Integer, BIGINT, VARCHAR, TIMESTAMP, TEXT, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


# CREATE TABLE orders
# (
#     order_id   SERIAL PRIMARY KEY,
#     user_id    BIGINT NOT NULL,
#     created_at TIMESTAMP DEFAULT NOW(),
#     FOREIGN KEY (user_id)
#         REFERENCES users (telegram_id)
#         ON DELETE CASCADE
# );

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


# CREATE TABLE products
# (
#     product_id  SERIAL PRIMARY KEY,
#     title       VARCHAR(255) NOT NULL,
#     description TEXT,
#     created_at  TIMESTAMP DEFAULT NOW()
# );

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    description = Column(TEXT)
    created_at = Column(TIMESTAMP, server_default=func.now())


# CREATE TABLE order_products
# (
#     order_id   INTEGER NOT NULL,
#     product_id INTEGER NOT NULL,
#     quantity   INTEGER NOT NULL,
#     FOREIGN KEY (order_id)
#         REFERENCES orders (order_id)
#         ON DELETE CASCADE,
#     FOREIGN KEY (product_id)
#         REFERENCES products (product_id)
#         ON DELETE RESTRICT
# );

class OrderProduct(Base):
    __tablename__ = 'order_products'

    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='RESTRICT'), primary_key=True)
    quantity = Column(Integer, nullable=False)

```

### Creating a database

Now you can use SQLAlchemy to create a database.

**Although it is not recommended**, since you would like to track changes in the database, and tracking changes with
SQLAlchemy boils down to writing them as raw SQL statements, which is not convenient.

We will use Alembic to create tables a little later.

```python
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

URL = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using
    username='testuser',
    password='testpassword',
    host='localhost',
    database='testuser',
    port=5433
)
engine = create_engine(URL, echo=True, future=True)

...
# Tables classes
...

# Let's run that only if it is run directly.
if __name__ == '__main__':
    Base.metadata.create_all(engine)

```

Now you can run the code, and you will see that raw SQL executed by SQLAlchemy in the console is almost identical to the
SQL we wrote.

### Drop all tables

Now, before moving to the next step of the tutorial, let's drop all tables.

Run the following code:

```python
Base.metadata.drop_all(engine)
```

## Using Alembic to create migrations.

As we discussed earlier, we will need to use [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to create
tables and track changes in the database.

> **Note:**
> This history of changes is called **migrations**.

In order to use Alembic, you need to install it. Make sure you are using the virtual environment.

```bash
source venv/bin/activate
pip install alembic
```

Now you have to init Alembic directory. We will call the directory `alembic` as well.

```bash
alembic init alembic
```

Now there were generated many files in the `alembic` directory. Please
read [their tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to understand how they work.

In order for the alembic to connect to our database we need to add the following to the `env.py` file.

```python
from sqlalchemy.engine.url import URL

url = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using
    username='testuser',
    password='testpassword',
    host='localhost',
    database='testuser',
    port=5433
)
config.set_main_option('sqlalchemy.url', str(url))
```

What we are actually doing here, is replacing the `sqlalchemy.url` from the `alembic.ini` file with the `URL` we created
earlier.

You can also write your `sqlalchemy.url` string in the `alembic.ini` file if you want.

> **Note:**
>
> You can also store your database connection information (login, password, port, ...) in environment variables and
> get them from there in the `env.py` file.

Now, for alembic to see our tables, we need to assign `target_metadata` to the metadata from the `Base` class, imported
from our main file to the `env.py` file.

```python
from main import Base

# target_metadata = None REPLACE WITH:
target_metadata = Base.metadata
```

However, what we are going to do, is to generate a first migration from our code, it will generate more python code in
the `alembic/versions` directory.

```bash
alembic revision --autogenerate -m "initial migration"
```

Great! Let's see what was generated.

```
INFO  [alembic.autogenerate.compare] Detected added table 'products'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'orders'
INFO  [alembic.autogenerate.compare] Detected added table 'order_products'
Generating SQL-Tutorial-2\Part7. SQLAlchemy and Alembic\alembic\versions\804682fdc9c4_initial_migration.py ...  done
```

#### 804682fdc9c4_initial_migration.py

```python
"""initial migration

Revision ID: 804682fdc9c4
Revises: 
Create Date: 2022-07-14 10:29:18.479014

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '804682fdc9c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
                    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
                    sa.Column('description', sa.TEXT(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('product_id')
                    )
    op.create_table('users',
                    sa.Column('telegram_id', sa.BIGINT(), nullable=False),
                    sa.Column('full_name', sa.VARCHAR(length=255), nullable=False),
                    sa.Column('username', sa.VARCHAR(length=255), nullable=True),
                    sa.Column('language_code', sa.VARCHAR(length=255), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('referrer_id', sa.BIGINT(), nullable=True),
                    sa.ForeignKeyConstraint(['referrer_id'], ['users.telegram_id'], ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('telegram_id')
                    )
    op.create_table('orders',
                    sa.Column('order_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.BIGINT(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.telegram_id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('order_id')
                    )
    op.create_table('order_products',
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ondelete='RESTRICT'),
                    sa.PrimaryKeyConstraint('order_id', 'product_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_products')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('products')
    # ### end Alembic commands ###
```

You can see here 2 functions:

- upgrade - which will create the tables, and add the columns, constraints, etc.
- downgrade - which will drop the tables, and remove the columns, constraints, etc., that are applied in the `upgrade`
  function.

So, whenever you want to upgrade your database, you can just run the `alembic upgrade head` command.

### Updating and downgrading

You can also update and downgrade your database by relative to current migration scripts (`+N` or `-N` migrations):

```bash
# upgrade
alembic upgrade +1
# or downgrade
alembic downgrade -1
```

Let's apply our changes to the database.

```bash
alembic upgrade head
```

Now you can make sure that tables were created with SQLAlchemy. Let's run our 2nd example from the previous tutorial:

```python
def example_2():
    session_pool = sessionmaker(bind=engine)
    query = text("SELECT * FROM users")
    with session_pool() as session:
        result = session.execute(query)
        all_rows = result.all()
        print(f'{all_rows=}')

```

##### Response:

```
INFO sqlalchemy.engine.Engine BEGIN (implicit)
INFO sqlalchemy.engine.Engine SELECT * FROM users
INFO sqlalchemy.engine.Engine [generated in 0.00011s] {}
all_rows=[]
INFO sqlalchemy.engine.Engine ROLLBACK
```

It got none rows because we haven't created any user in our database. However, it works!

### Changes in the database

Whenever you like to change your tables, you can do it by editing your python code of table classes, or otherwise you
can create a new migration script with `alembic revision --autogenerate -m "new migration"` and add the changes
manually.

This is because not always the alembic will understand what you are trying to do. Let's compare two examples.

#### Changing columns data type

- What if we need to change language_code data type to VARCHAR with a new length? 255 is more than enough, so let's
  change to 10 characters.
- What if we need to restrict the length of the product description from TEXT with unfixed max length to fixed max
  length of 3000 characters?

We will edit that in our classes:

```python
...


class User(Base):
    # language_code = Column(VARCHAR(255), nullable=False)
    language_code = Column(VARCHAR(10), nullable=False)


...


class Product(Base):
    # description = Column(TEXT)
    description = Column(VARCHAR(3000), nullable=True)


...
```

Now let's create a new migration script:

```bash
alembic revision --autogenerate -m "changed language_code and product description"
```

You will see that no changes were found by alembic:
```python
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
```

So in that case we need to edit the code manually:

```python
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'language_code', type_=sa.VARCHAR(10), nullable=False)
    op.alter_column('products', 'description', type_=sa.VARCHAR(3000), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'description', type_=sa.TEXT, nullable=True)
    op.alter_column('users', 'language_code', type_=sa.VARCHAR(255), nullable=False)
    # ### end Alembic commands ###
```

Now we have our newly created migration script, and we need to upgrade our database.

```bash
alembic upgrade +1
```

#### Adding a new column

What if we need to add a new column to our table?

Let's add a new column to our table:

```python
class Users(Base):
    ...
    phone_number = Column(VARCHAR(50))
```

Let's create a new migration script:

```bash
alembic revision --autogenerate -m "added user phone number"
```

Hurray! This change was detected by alembic, and we can upgrade our database.

```python
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
```

Let's apply our changes to the database.

```bash
alembic upgrade +1
```

Brilliant! You have learnt how to create tables with Alembic and SQLAlchemy, and how to upgrade and downgrade your
database.