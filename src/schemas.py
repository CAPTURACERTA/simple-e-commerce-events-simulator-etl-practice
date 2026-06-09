from pydantic import BaseModel, EmailStr

# Customer schemes

class Customer(BaseModel):
    name: str
    email: EmailStr

class CustomerResponse(Customer):
    customer_id: int

# Product schemes

class Product(BaseModel):
    name: str
    price: float

class ProductResponse(Product):
    product_id: int

# Order schemes

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    customer_id: int
    items: list[OrderItem]  

class OrderResponse(Order):
    order_id: int
    order_date: str