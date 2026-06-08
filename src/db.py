import atexit
import os
from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

load_dotenv()


def _get_int_env(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value else default


DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": _get_int_env("DB_PORT", 5432),
    "database": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "cursor_factory": RealDictCursor,
}

connection_pool = SimpleConnectionPool(
    minconn=_get_int_env("DB_POOL_MIN", 1),
    maxconn=_get_int_env("DB_POOL_MAX", 10),
    **DB_CONFIG,
)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)


@contextmanager
def get_db_connection():
    conn = get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)


def create_tables():
    statements = (
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price NUMERIC(10, 2)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(customer_id),
            order_date TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INT REFERENCES orders(order_id),
            product_id INT REFERENCES products(product_id),
            quantity INT
        );
        """,
    )

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        conn.commit()


def close_connection_pool():
    connection_pool.closeall()


atexit.register(close_connection_pool)
create_tables()
