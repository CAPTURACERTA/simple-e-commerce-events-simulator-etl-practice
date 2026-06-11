from ..db import get_db_connection
from fastapi import APIRouter, Depends, Path


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/top-customers-count/{limit}")
def top_customers_count(
    limit: int = Path(gt=0, le=100),
    db_conn=Depends(get_db_connection),
):
    with db_conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.customer_id, c.name, c.email, COUNT(o.order_id) AS order_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            ORDER BY order_count DESC
            LIMIT %s
            """,
            (limit,),
        )
        results = cursor.fetchall()
        return [
            {
                "customer_id": row["customer_id"],
                "name": row["name"],
                "email": row["email"],
                "order_count": row["order_count"],
            }
            for row in results
        ]

@router.get("/top-customers-value/{limit}")
def top_customers_value(
    limit: int = Path(gt=0, le=100),
    db_conn=Depends(get_db_connection),
):
    with db_conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.customer_id, c.name, c.email, SUM(oi.quantity * p.price) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY c.customer_id
            ORDER BY total_spent DESC
            LIMIT %s
            """,
            (limit,),
        )
        results = cursor.fetchall()
        return [
            {
                "customer_id": row["customer_id"],
                "name": row["name"],
                "email": row["email"],
                "total_spent": float(row["total_spent"]),
            }
            for row in results
        ]

@router.get("/top-products/{limit}")
def top_products(
    limit: int = Path(gt=0, le=100),
    db_conn=Depends(get_db_connection),
):
    with db_conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.product_id, p.name, p.price, SUM(oi.quantity) AS total_sold
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.product_id
            ORDER BY total_sold DESC
            LIMIT %s
            """,
            (limit,),
        )
        results = cursor.fetchall()
        return [
            {
                "product_id": row["product_id"],
                "name": row["name"],
                "price": float(row["price"]),
                "total_sold": row["total_sold"],
            }
            for row in results
        ]
