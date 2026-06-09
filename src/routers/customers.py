from ..schemas import Customer, CustomerResponse
from ..db import get_db_connection
from fastapi import APIRouter, HTTPException, Depends, status


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: Customer, db_conn=Depends(get_db_connection)):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING customer_id",
            (customer.name, customer.email),
        )
        customer_id = cursor.fetchone()["customer_id"]
        db_conn.commit()
        return CustomerResponse(customer_id=customer_id, **customer.model_dump())
    

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db_conn=Depends(get_db_connection)):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "SELECT customer_id, name, email FROM customers WHERE customer_id = %s",
            (customer_id,),
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return CustomerResponse(**result)
