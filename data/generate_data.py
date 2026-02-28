"""
Generate a realistic 3-year retail/e-commerce sales dataset.
Run this once to create sales_data.csv
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ── Config ───────────────────────────────────────────────
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2024, 12, 31)
N_ORDERS   = 5000

CATEGORIES = {
    "Electronics":   {"products": ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch"], "price_range": (150, 1200)},
    "Clothing":      {"products": ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes"],               "price_range": (20, 200)},
    "Home & Living": {"products": ["Sofa", "Lamp", "Bedsheet", "Curtains", "Cookware"],            "price_range": (30, 800)},
    "Books":         {"products": ["Fiction", "Non-Fiction", "Textbook", "Comic", "Biography"],    "price_range": (10, 80)},
    "Sports":        {"products": ["Yoga Mat", "Dumbbells", "Cycle", "Tennis Racket", "Shoes"],    "price_range": (25, 500)},
    "Beauty":        {"products": ["Perfume", "Skincare Kit", "Lipstick", "Hair Dryer", "Serum"],  "price_range": (15, 250)},
}

REGIONS    = ["North", "South", "East", "West", "Central"]
CITIES     = {
    "North":   ["Delhi", "Chandigarh", "Amritsar"],
    "South":   ["Bangalore", "Chennai", "Hyderabad"],
    "East":    ["Kolkata", "Bhubaneswar", "Patna"],
    "West":    ["Mumbai", "Pune", "Ahmedabad"],
    "Central": ["Bhopal", "Indore", "Nagpur"],
}
CHANNELS   = ["Website", "Mobile App", "Marketplace", "Direct"]
PAYMENT    = ["Credit Card", "Debit Card", "UPI", "Net Banking", "COD"]

# ── Generate Dates (with seasonality) ───────────────────
total_days = (END_DATE - START_DATE).days
dates = []
for _ in range(N_ORDERS):
    d = START_DATE + timedelta(days=np.random.randint(0, total_days))
    # Boost sales in Oct-Dec (festival season)
    if d.month in [10, 11, 12] and np.random.rand() < 0.3:
        d = START_DATE + timedelta(days=np.random.randint(0, total_days))
    dates.append(d)
dates.sort()

# ── Generate Records ─────────────────────────────────────
records = []
for i, date in enumerate(dates):
    category = np.random.choice(list(CATEGORIES.keys()),
                                 p=[0.25, 0.20, 0.15, 0.10, 0.15, 0.15])
    cat_info = CATEGORIES[category]
    product  = np.random.choice(cat_info["products"])
    lo, hi   = cat_info["price_range"]
    price    = round(np.random.uniform(lo, hi), 2)
    qty      = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.4, 0.2, 0.1, 0.15, 0.1, 0.05])
    discount = np.random.choice([0, 5, 10, 15, 20, 25], p=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05])
    revenue  = round(price * qty * (1 - discount/100), 2)
    profit   = round(revenue * np.random.uniform(0.15, 0.40), 2)
    region   = np.random.choice(REGIONS)
    city     = np.random.choice(CITIES[region])
    channel  = np.random.choice(CHANNELS, p=[0.35, 0.30, 0.25, 0.10])
    payment  = np.random.choice(PAYMENT,  p=[0.25, 0.20, 0.30, 0.10, 0.15])
    rating   = round(np.random.choice([3.0, 3.5, 4.0, 4.5, 5.0],
                                       p=[0.05, 0.10, 0.30, 0.35, 0.20]), 1)
    returned = np.random.choice([0, 1], p=[0.92, 0.08])

    records.append({
        "OrderID":       f"ORD-{10000 + i}",
        "Date":          date.strftime("%Y-%m-%d"),
        "Month":         date.strftime("%b %Y"),
        "Quarter":       f"Q{(date.month-1)//3 + 1} {date.year}",
        "Year":          date.year,
        "Category":      category,
        "Product":       product,
        "UnitPrice":     price,
        "Quantity":      qty,
        "Discount":      discount,
        "Revenue":       revenue,
        "Profit":        profit,
        "Region":        region,
        "City":          city,
        "Channel":       channel,
        "PaymentMethod": payment,
        "Rating":        rating,
        "Returned":      returned,
    })

df = pd.DataFrame(records)
df.to_csv("sales_data.csv", index=False)
print(f"✅ Dataset saved: {len(df)} orders")
print(f"   Total Revenue: ₹{df['Revenue'].sum():,.0f}")
print(f"   Total Profit:  ₹{df['Profit'].sum():,.0f}")
print(f"   Date Range:    {df['Date'].min()} to {df['Date'].max()}")
print(f"   Categories:    {df['Category'].nunique()}")
print(f"   Cities:        {df['City'].nunique()}")
