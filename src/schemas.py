from pydantic import BaseModel, EmailStr, Field

# Customer schemes

class Customer(BaseModel):
    name: str
    email: EmailStr

class CustomerResponse(Customer):
    customer_id: int

# Product schemes

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)

class ProductResponse(Product):
    product_id: int

# Order schemes

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class Order(BaseModel):
    customer_id: int
    items: list[OrderItem] = Field(min_length=1)

class OrderResponse(Order):
    order_id: int
    order_date: str

# Extract schemes 

class ExtractRequest(BaseModel):
    amount: int = Field(gt=0, le=100)

class ExtractResponse(BaseModel):
    message: str
    orders_created: int