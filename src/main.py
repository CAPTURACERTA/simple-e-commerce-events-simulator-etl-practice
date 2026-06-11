from fastapi import FastAPI
from .routers import analytics, customers, orders, products, extract

app = FastAPI()

app.include_router(analytics.router)
app.include_router (customers.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(extract.router)