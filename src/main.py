from fastapi import FastAPI
from .routers import analytics, customers, orders, products

app = FastAPI()

# app.include_router(analytics.router)
app.include_router (customers.router)
app.include_router(orders.router)
app.include_router(products.router)