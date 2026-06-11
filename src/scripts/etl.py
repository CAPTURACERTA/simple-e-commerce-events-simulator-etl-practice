from ..db import db_connection_context
from .fake_data import generate_random_orders


def get_customers_ids():
    with db_connection_context() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT customer_id FROM customers")
            return [row["customer_id"] for row in cursor.fetchall()]

def get_products_ids():
    with db_connection_context() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT product_id FROM products")
            return [row["product_id"] for row in cursor.fetchall()]

def insert_orders(amount: int) -> int:
    customer_ids = get_customers_ids()
    product_ids = get_products_ids()

    if not customer_ids:
        raise ValueError("No customers available. Create customers before extracting orders.")
    if not product_ids:
        raise ValueError("No products available. Create products before extracting orders.")

    orders = generate_random_orders(amount, customer_ids, product_ids)

    with db_connection_context() as db_conn:
        with db_conn.cursor() as cursor:
            for order in orders:
                cursor.execute(
                    "INSERT INTO orders (customer_id, order_date) VALUES (%s, %s) RETURNING order_id",
                    (order["customer_id"], order["order_date"])
                )
                order_id = cursor.fetchone()["order_id"]
                for item in order["items"]:
                    cursor.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                        (order_id, item["product_id"], item["quantity"])
                    )
        db_conn.commit()
    return len(orders)
