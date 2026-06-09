import random
from datetime import datetime, timedelta


def generate_random_orders(
        amount: int,
        customer_ids: list[int],
        product_ids: list[int]
) -> list[dict]:
    orders = []
    for _ in range(amount):
        order = {
            "customer_id": random.choice(customer_ids),
            "order_date": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            "items": [
                {
                    "product_id": random.choice(product_ids),
                    "quantity": random.randint(1, 5)
                }
                for _ in range(random.randint(1, 3))
            ]
        }
        orders.append(order)
    return orders