import pandas as pd
import random
from faker import Faker

fake = Faker()

products = [
    "Laptop",
    "Phone",
    "Tablet",
    "Monitor",
    "Keyboard"
]

regions = [
    "North",
    "South",
    "East",
    "West"
]

sales_reps = [
    "Rahul",
    "Priya",
    "Amit",
    "Sneha",
    None
]

data = []

for i in range(500):
    quantity = random.randint(-2, 10)

    price = random.randint(5000, 50000)

    row = {
        "order_id": random.randint(1000, 1100),
        "product": random.choice(products),
        "region": random.choice(regions),
        "sales_rep": random.choice(sales_reps),
        "quantity": quantity,
        "price": price,
        "order_date": fake.date_this_year()
    }

    data.append(row)

df = pd.DataFrame(data)

df.to_csv("data/raw_sales.csv", index=False)

print("Raw sales data generated successfully!")