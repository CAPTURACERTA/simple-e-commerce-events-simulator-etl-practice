from ..schemas import Order, OrderResponse, OrderItem
from ..db import get_db_connection
from fastapi import APIRouter, HTTPException, Depends, status


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: Order, db_conn=Depends(get_db_connection)):
    with db_conn.cursor() as cursor:
        # Insert order and get order_id
        cursor.execute(
            "INSERT INTO orders (customer_id) VALUES (%s) RETURNING *",
            (order.customer_id,),
        )
        order_row = cursor.fetchone()
        order_row['order_date'] = str(order_row['order_date'])

        # Insert order items
        for item in order.items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                (order_row['order_id'], item.product_id, item.quantity),
            )
        db_conn.commit()
        return OrderResponse(**order_row, items=order.items)
    
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db_conn=Depends(get_db_connection)):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "SELECT order_id, customer_id, order_date FROM orders WHERE order_id = %s",
            (order_id,),
        )
        order_row = cursor.fetchone()
        if not order_row:
            raise HTTPException(status_code=404, detail="Order not found")
        order_row['order_date'] = str(order_row['order_date'])
        
        cursor.execute(
            "SELECT product_id, quantity FROM order_items WHERE order_id = %s",
            (order_id,),
        )
        items = [OrderItem(product_id=row["product_id"], quantity=row["quantity"]) for row in cursor.fetchall()]
        
        return OrderResponse(**order_row, items=items)