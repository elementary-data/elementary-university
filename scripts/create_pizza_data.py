# Cell 1: Imports
import csv
import random
import uuid
from datetime import datetime, timedelta

from faker import Faker

# Cell 2: Load base pizza data from CSV
pizza_data = []
with open("pizza_sales.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pizza_data.append({
            "pizza_name_id": row["pizza_name_id"],
            "pizza_size": row["pizza_size"],
            "unit_price": float(row["unit_price"]),
            "pizza_category": row["pizza_category"],
            "pizza_name": row["pizza_name"],
            "pizza_ingredients": row["pizza_ingredients"]
        })

# Remove duplicates
seen = set()
unique_pizzas = []
for p in pizza_data:
    key = (p["pizza_name_id"], p["pizza_size"], p["unit_price"], p["pizza_category"], p["pizza_name"])
    if key not in seen:
        seen.add(key)
        unique_pizzas.append(p)

# Cell 3: Extract unique ingredients
all_ingredients = set()
for p in unique_pizzas:
    ingredients = p["pizza_ingredients"].split(", ")
    all_ingredients.update(ingredients)

ingredient_list = sorted(all_ingredients)
ingredient_to_id = {name: idx + 1 for idx, name in enumerate(ingredient_list)}

# Save ingredient table to CSV
with open("ingredients.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "ingredient"])
    for name, idx in ingredient_to_id.items():
        writer.writerow([idx, name])

# Load existing customer ids from jaffle-data
customer_ids = []
with open("jaffle-data/raw_customers.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        customer_ids.append(row["id"])

# Cell 4: Generate synthetic pizza sales
fake = Faker()
start_date = datetime(2025, 1, 1)
end_date = datetime.today()
delta = end_date - start_date

order_id_counter = 1
pizza_id_counter = 1
output_rows = []

def generate_sales_for_day(day_index, num_orders=None):
    global pizza_id_counter, order_id_counter
    day = start_date + timedelta(days=day_index)
    num_orders = num_orders if num_orders is not None else random.randint(5, 20)

    for _ in range(num_orders):
        order_time = fake.time()
        num_items = random.randint(1, 5)
        if random.random() < 0.7:
            order_customer_id = random.choice(customer_ids)
        else:
            order_customer_id = str(uuid.uuid4())

        for _ in range(num_items):
            pizza = random.choice(unique_pizzas)
            quantity = random.randint(1, 3)
            unit_price = pizza["unit_price"]
            total_price = round(unit_price * quantity, 2)

            ingredient_names = pizza["pizza_ingredients"].split(", ")
            ingredient_ids = [ingredient_to_id[name] for name in ingredient_names]
            
            output_rows.append([
                pizza_id_counter,
                order_id_counter,
                order_customer_id,
                pizza["pizza_name_id"],
                quantity,
                day.strftime('%m/%d/%Y'),
                order_time,
                unit_price,
                total_price,
                pizza["pizza_size"],
                pizza["pizza_category"],
                pizza["pizza_name"],
                "|".join(ingredient_names),
                "|".join(map(str, ingredient_ids))
            ])
            pizza_id_counter += 1
        order_id_counter += 1

# Generate one batch per day from start_date to today
for i in range(delta.days + 1):
    generate_sales_for_day(i)

# Add extra synthetic data for yesterday
yesterday = datetime.now().date() - timedelta(days=1)
yesterday_index = (yesterday - start_date.date()).days

if 0 <= yesterday_index <= delta.days:
    extra_orders = random.randint(20,100)
    print(f"Adding {extra_orders} extra orders for {yesterday}")
    generate_sales_for_day(yesterday_index, num_orders=extra_orders)

# Cell 5: Write to synthetic_pizza_sales.csv
with open("raw_pizza_sales.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        "pizza_id",
        "order_id",
        "customer_id",
        "pizza_name_id",
        "quantity",
        "order_date",
        "order_time",
        "unit_price",
        "total_price",
        "pizza_size",
        "pizza_category",
        "pizza_name",
        "ingredient_names",
        "ingredient_ids",
    ])
    writer.writerows(output_rows)

print("Generated 'synthetic_pizza_sales.csv' and 'ingredients.csv'")
