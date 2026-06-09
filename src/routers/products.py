from ..schemas import Product, ProductResponse
from ..db import get_db_connection
from fastapi import APIRouter, HTTPException, Depends, status


router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: Product, db_conn=Depends(get_db_connection)):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING product_id",
            (product.name, product.price),
        )
        product_id = cursor.fetchone()["product_id"]
        db_conn.commit()
        return ProductResponse(product_id=product_id, **product.model_dump())
    
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db_conn=Depends(get_db_connection)):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "SELECT product_id, name, price FROM products WHERE product_id = %s",
            (product_id,),
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse(**result)