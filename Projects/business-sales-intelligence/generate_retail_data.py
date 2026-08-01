"""
Synthetic E-Commerce Retail Dataset Generator
Mimics the structure/distributions of the UCI Online Retail II dataset.

Run:  python3 generate_retail_data.py
Output: online_retail_synthetic.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

# =========================================================================
# 1. PRODUCT CATALOG  (~2,800 unique products across realistic categories)
# =========================================================================

CATEGORIES = {
    "decor": {
        "adjectives": ["WHITE HANGING", "VINTAGE", "RUSTIC", "FLORAL", "STRIPED",
                       "PAINTED", "ANTIQUE", "PASTEL", "GLASS", "WOODEN", "METAL",
                       "CERAMIC", "RETRO", "SHABBY CHIC", "CHRISTMAS"],
        "nouns": ["HEART T-LIGHT HOLDER", "WALL CLOCK", "PHOTO FRAME", "CANDLE HOLDER",
                  "WOODEN SIGN", "MIRROR", "WALL ART", "DOOR MAT", "CUSHION COVER",
                  "LAMP SHADE", "HANGING DECORATION", "STAR DECORATION", "BUNTING",
                  "STORAGE BOX", "TRINKET BOX", "GARLAND"],
        "price_tier_bias": [0.6, 0.3, 0.08, 0.02],
    },
    "kitchen": {
        "adjectives": ["RETRO", "SET OF 3", "SET OF 6", "ENAMEL", "SPOTTY", "STRIPED",
                       "REGENCY", "VINTAGE", "PARTY", "TRAVEL", "CHARLOTTE", "PINK"],
        "nouns": ["MUG", "CAKE STAND", "STORAGE JAR", "BAKING TIN", "TEA TOWEL",
                  "SPATULA SET", "CHOPPING BOARD", "EGG CUP", "TEAPOT", "LUNCH BOX",
                  "CAKE TIN", "COASTER SET", "TRAY", "BISCUIT TIN", "APRON"],
        "price_tier_bias": [0.55, 0.32, 0.1, 0.03],
    },
    "gifts": {
        "adjectives": ["SMALL", "LARGE", "MINI", "GLASS", "PAPER", "FELT", "KNITTED",
                       "PERSONALISED", "NOVELTY", "TRADITIONAL", "GLITTER"],
        "nouns": ["GIFT BAG", "GREETING CARD", "JEWELLERY BOX", "KEYRING", "MAGNET",
                  "NOTEBOOK", "PENCIL CASE", "PHOTO ALBUM", "GIFT TAG SET",
                  "WRAPPING PAPER", "TRINKET TRAY", "MONEY BOX"],
        "price_tier_bias": [0.65, 0.28, 0.06, 0.01],
    },
    "decorations_seasonal": {
        "adjectives": ["CHRISTMAS", "EASTER", "HALLOWEEN", "PARTY", "BIRTHDAY",
                       "WEDDING", "VINTAGE", "GLITTER", "PAPER"],
        "nouns": ["BAUBLE SET", "TREE DECORATION", "BUNTING", "PARTY BAG",
                  "BALLOON PACK", "CAKE TOPPER", "GARLAND", "CRACKERS SET",
                  "CANDLE SET", "LIGHT STRING"],
        "price_tier_bias": [0.55, 0.35, 0.08, 0.02],
    },
    "bags_textiles": {
        "adjectives": ["JUMBO", "SMALL", "RETRO", "SPOTTY", "STRIPED", "VINTAGE",
                       "CANVAS", "RECYCLED", "FOLDING"],
        "nouns": ["SHOPPER BAG", "TOTE BAG", "WASH BAG", "LUNCH BAG", "STORAGE BAG",
                  "APRON", "TEA COSY", "OVEN GLOVE", "DOORSTOP", "CUSHION"],
        "price_tier_bias": [0.6, 0.3, 0.08, 0.02],
    },
    "garden": {
        "adjectives": ["METAL", "WOODEN", "SOLAR", "HANGING", "CERAMIC", "VINTAGE STYLE"],
        "nouns": ["PLANT POT", "BIRD FEEDER", "GARDEN SIGN", "WIND CHIME",
                  "WATERING CAN", "GARDEN LANTERN", "PLANT MARKER SET"],
        "price_tier_bias": [0.45, 0.35, 0.15, 0.05],
    },
    "toys_stationery": {
        "adjectives": ["MINI", "COLOURING", "WOODEN", "RETRO", "SPACEBOY", "DOLLY GIRL"],
        "nouns": ["PLAYING CARDS", "COLOURING SET", "BUILDING BLOCKS", "NOTEBOOK",
                  "PENCIL SET", "STICKER SHEET", "PUZZLE", "SPINNING TOP"],
        "price_tier_bias": [0.7, 0.25, 0.04, 0.01],
    },
    "luxury": {
        "adjectives": ["DESIGNER", "LIMITED EDITION", "HANDCRAFTED", "PREMIUM",
                       "ARTISAN", "SIGNATURE"],
        "nouns": ["JEWELLERY SET", "SCARF", "CANDLE COLLECTION", "TABLE LAMP",
                  "DECORATIVE VASE", "WALL HANGING", "GIFT HAMPER"],
        "price_tier_bias": [0.05, 0.25, 0.4, 0.3],
    },
}

PRICE_TIERS = [(0.50, 5.00), (5.01, 15.00), (15.01, 50.00), (50.01, 100.00)]

def build_product_catalog(n_target=2800):
    products = []
    seen_desc = set()
    seen_codes = set()
    cat_names = list(CATEGORIES.keys())

    while len(products) < n_target:
        cat = cat_names[rng.integers(0, len(cat_names))]
        spec = CATEGORIES[cat]
        adj = spec["adjectives"][rng.integers(0, len(spec["adjectives"]))]
        noun = spec["nouns"][rng.integers(0, len(spec["nouns"]))]
        desc = f"{adj} {noun}"
        # add a colour/variant sometimes to create more unique combos
        if rng.random() < 0.5:
            variant = ["RED", "BLUE", "PINK", "GREEN", "IVORY", "NATURAL", "GREY",
                       "YELLOW", "PURPLE", "TURQUOISE"][rng.integers(0, 10)]
            desc = f"{variant} {desc}"
        if desc in seen_desc:
            continue
        seen_desc.add(desc)

        # stock code: 5 digits, optional letter suffix
        while True:
            code = str(rng.integers(10000, 99999))
            if rng.random() < 0.35:
                code += chr(65 + rng.integers(0, 26))
            if code not in seen_codes:
                seen_codes.add(code)
                break

        tier_idx = rng.choice(4, p=spec["price_tier_bias"])
        lo, hi = PRICE_TIERS[tier_idx]
        base_price = round(rng.uniform(lo, hi), 2)

        products.append({
            "StockCode": code,
            "Description": desc,
            "Category": cat,
            "BasePrice": base_price,
        })

    return pd.DataFrame(products)

print("Building product catalog...")
catalog = build_product_catalog(2800)
print(f"  {len(catalog)} unique products created")

# =========================================================================
# 2. CUSTOMERS & COUNTRIES
# =========================================================================

COUNTRIES = ["United Kingdom", "Germany", "France", "USA", "Spain", "Netherlands",
             "Belgium", "Switzerland", "Portugal", "Ireland", "Other"]
COUNTRY_P = [0.85, 0.03, 0.03, 0.02, 0.02, 0.015, 0.01, 0.01, 0.005, 0.005, 0.005]
OTHER_COUNTRIES = ["Italy", "Sweden", "Norway", "Denmark", "Poland", "Austria",
                    "Finland", "Australia", "Japan", "Canada"]

N_CUSTOMERS = 4500
customer_ids = rng.choice(np.arange(12345, 20000), size=N_CUSTOMERS, replace=False)
customer_country = rng.choice(COUNTRIES, size=N_CUSTOMERS, p=COUNTRY_P)
customer_country_map = dict(zip(customer_ids, customer_country))

print(f"Created {N_CUSTOMERS} unique customers")

# =========================================================================
# 3. TIME / SEASONALITY WEIGHTING
# =========================================================================

START_DATE = datetime(2009, 12, 1)
END_DATE = datetime(2011, 12, 9)
TOTAL_DAYS = (END_DATE - START_DATE).days

def day_weight(d: datetime) -> float:
    """Seasonal + gradual-growth weighting for a given date."""
    month = d.month
    # seasonality by month: holiday peak Nov-Dec, trough Jan-Feb
    month_factor = {
        1: 0.6, 2: 0.65, 3: 0.8, 4: 0.85, 5: 0.9, 6: 0.95,
        7: 0.9, 8: 0.85, 9: 1.0, 10: 1.15, 11: 1.6, 12: 1.75,
    }[month]
    # gradual growth across the whole 2-year window
    progress = (d - START_DATE).days / TOTAL_DAYS
    growth_factor = 0.75 + 0.5 * progress
    return month_factor * growth_factor

# precompute daily weights
all_days = [START_DATE + timedelta(days=i) for i in range(TOTAL_DAYS + 1)]
weights = np.array([day_weight(d) for d in all_days])
weights = weights / weights.sum()

# =========================================================================
# 4. INVOICE GENERATION
# =========================================================================

N_INVOICES = 62000          # scaled up from the 20-25K spec to hit ~500K total rows
CANCEL_RATE = 0.04          # 4% of invoices are cancellations
NULL_CUSTOMER_RATE = 0.20

print(f"Generating {N_INVOICES} invoices...")

# sample invoice dates according to seasonal weights
day_idx = rng.choice(len(all_days), size=N_INVOICES, p=weights)
invoice_dates = [all_days[i] + timedelta(hours=int(rng.integers(8, 20)),
                                          minutes=int(rng.integers(0, 60)))
                  for i in day_idx]
invoice_dates.sort()  # chronological order looks more realistic

# items per invoice: mean ~8, range 2-20
items_per_invoice = np.clip(rng.poisson(6, size=N_INVOICES) + 2, 2, 20)

# assign customer (or null) per invoice
is_guest = rng.random(N_INVOICES) < NULL_CUSTOMER_RATE
invoice_customers = rng.choice(customer_ids, size=N_INVOICES)
invoice_customers = invoice_customers.astype(object)
invoice_customers[is_guest] = None

# country: matches the customer's home country when known, else sampled fresh
invoice_country = np.empty(N_INVOICES, dtype=object)
for i in range(N_INVOICES):
    if invoice_customers[i] is not None:
        invoice_country[i] = customer_country_map[invoice_customers[i]]
    else:
        invoice_country[i] = rng.choice(COUNTRIES, p=COUNTRY_P)
# expand "Other" into a real country name
other_mask = invoice_country == "Other"
invoice_country[other_mask] = rng.choice(OTHER_COUNTRIES, size=other_mask.sum())

# which invoices are cancellations
is_cancel = rng.random(N_INVOICES) < CANCEL_RATE

# invoice numbers
base_no = 536365
normal_counter = base_no
cancel_counter = base_no + 5  # offset so sequences interleave a bit differently
invoice_numbers = []
for i in range(N_INVOICES):
    if is_cancel[i]:
        invoice_numbers.append(f"C{cancel_counter}")
        cancel_counter += rng.integers(1, 4)
    else:
        invoice_numbers.append(str(normal_counter))
        normal_counter += rng.integers(1, 4)

# category-weighted product pools, precomputed for fast sampling
cat_groups = {cat: catalog[catalog.Category == cat].reset_index(drop=True)
              for cat in CATEGORIES}
cat_names_list = list(CATEGORIES.keys())

rows = []
for i in range(N_INVOICES):
    n_items = int(items_per_invoice[i])
    inv_no = invoice_numbers[i]
    cust = invoice_customers[i]
    cust_val = int(cust) if cust is not None else np.nan
    country = invoice_country[i]
    inv_date = invoice_dates[i]

    # realistic co-occurrence: pull most items from 1-2 categories, a couple from elsewhere
    primary_cats = rng.choice(cat_names_list, size=min(2, len(cat_names_list)), replace=False)

    chosen_products = []
    for j in range(n_items):
        if rng.random() < 0.8:
            cat = primary_cats[rng.integers(0, len(primary_cats))]
        else:
            cat = cat_names_list[rng.integers(0, len(cat_names_list))]
        pool = cat_groups[cat]
        prod = pool.iloc[rng.integers(0, len(pool))]
        chosen_products.append(prod)

    for prod in chosen_products:
        if is_cancel[i]:
            qty = -int(rng.integers(1, 51))
        else:
            r = rng.random()
            if r < 0.94:
                qty = int(rng.integers(1, 101))
            elif r < 0.995:
                qty = int(rng.integers(100, 501))
            else:
                qty = int(rng.integers(500, 1001))

        price = round(prod["BasePrice"] * rng.uniform(0.95, 1.05), 2)
        price = max(price, 0.01)

        rows.append((
            inv_no,
            prod["StockCode"],
            prod["Description"],
            qty,
            inv_date,
            price,
            cust_val,
            country,
        ))

print(f"Generated {len(rows)} line items")

df = pd.DataFrame(rows, columns=[
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
])

# format date as MM/DD/YYYY HH:MM
df["InvoiceDate"] = df["InvoiceDate"].dt.strftime("%m/%d/%Y %H:%M")

print(f"\nFinal dataset shape: {df.shape}")

# =========================================================================
# 5. SANITY CHECKS
# =========================================================================

print("\n--- Sanity Checks ---")
print("All UnitPrice > 0:", (df["UnitPrice"] > 0).all())
print("Quantity has negatives (returns) and positives (sales):",
      (df["Quantity"] < 0).any() and (df["Quantity"] > 0).any())
c_invoices = df["InvoiceNo"].str.startswith("C")
print("All C-invoices have negative Quantity:",
      (df.loc[c_invoices, "Quantity"] < 0).all())
pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M")  # raises if invalid
print("InvoiceDate parses as valid datetime: True")
pct_customer_populated = df["CustomerID"].notna().mean()
print(f"CustomerID populated: {pct_customer_populated:.1%} (target >=80%)")
print("Description never empty:", (df["Description"].str.len() > 0).all())
print("Unique invoices:", df["InvoiceNo"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Unique customers:", df["CustomerID"].dropna().nunique())
print("Cancellation invoice %:", round(c_invoices.mean() * 100, 2), "%")
print("Date range:", df["InvoiceDate"].min(), "to", df["InvoiceDate"].max())
print("\nCountry distribution:")
print((df["Country"].value_counts(normalize=True) * 100).round(2).head(11))

# =========================================================================
# 6. EXPORT
# =========================================================================

import csv
out_path = "/mnt/user-data/outputs/online_retail_synthetic.csv"
# QUOTE_NONNUMERIC -> all text fields (InvoiceNo, StockCode, Description, Country)
# get double-quoted; numeric fields (Quantity, UnitPrice, CustomerID) stay bare.
df.to_csv(out_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"\nSaved to {out_path}")
