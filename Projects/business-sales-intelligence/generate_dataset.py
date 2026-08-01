"""
Generate synthetic e-commerce dataset for Business Sales Intelligence project.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
num_invoices = 22000
num_customers = 4500
num_products = 2700

def generate_products(n):
    """Generate product catalog with descriptions and prices."""
    product_data = []
    descriptions = [
        'WHITE HANGING HEART T-LIGHT HOLDER', 'METAL LANTERN', 'PACK OF 12 PINK PARASOL',
        'WOODEN STAR DECORATION', 'SET OF 3 FAIRY LIGHTS', 'KNITTED CHRISTMAS STOCKING',
        'CANDLE HOLDER GLASS', 'DECORATIVE MIRROR', 'SET OF 6 GLASSES', 'CERAMIC VASE',
        'RUSTIC WOODEN FRAME', 'GOLD METAL CANDLE STAND', 'PACK OF 5 STORAGE BOXES',
        'PLANT POT WITH STAND', 'PACK OF 4 MUGS', 'CHRISTMAS TREE ORNAMENT SET',
        'JUTE BAG WITH PRINT', 'BEADED NAPKIN RINGS', 'STAINLESS STEEL WATER BOTTLE',
        'WOODEN CUTTING BOARD', 'MARBLE COASTERS', 'VELVET CUSHION', 'BAMBOO COOKIE CUTTERS',
        'GLASS TERRARIUM', 'PACK OF 3 SCENTED CANDLES', 'METAL WALL ART', 'LEATHER PHOTO FRAME',
        'CERAMIC BIRD FIGURINE', 'SET OF 2 SALT AND PEPPER POTS', 'PORCELAIN TEAPOT',
        'GARDEN GNOME', 'WIND CHIME', 'BAMBOO PLANT STAND', 'MACRAME PLANT HANGER',
        'BOOKEND SET', 'PAPER LANTERN', 'MOSAIC CANDLE HOLDER', 'OAK CHEESE BOARD',
        'SET OF 4 COFFEE MUGS', 'GLASS BOTTLE WITH STOPPER', 'ROPE BASKET', 'CERAMIC PLATE SET'
    ]
    
    for i in range(n):
        desc = random.choice(descriptions)
        stock = f"{random.randint(10000, 99999)}{random.choice(['A', 'B', 'C', ''])}"
        price = round(random.uniform(0.50, 50.00), 2)
        
        if random.random() < 0.1:  # 10% luxury items
            price = round(random.uniform(50.00, 100.00), 2)
        elif random.random() < 0.3:  # 30% mid-range
            price = round(random.uniform(5.01, 15.00), 2)
        else:  # 60% low-range
            price = round(random.uniform(0.50, 5.00), 2)
            
        product_data.append({'StockCode': stock, 'Description': desc, 'UnitPrice': price})
    
    return pd.DataFrame(product_data)

def generate_invoice_data():
    """Generate invoice transactions."""
    products_df = generate_products(num_products)
    customer_ids = list(range(12345, 12345 + num_customers))
    
    country_list = ['United Kingdom'] * 8500 + ['Germany'] * 300 + ['France'] * 300 + ['USA'] * 200 + \
                   ['Spain'] * 200 + ['Netherlands'] * 150 + ['Belgium'] * 100 + ['Switzerland'] * 100 + \
                   ['Portugal'] * 50 + ['Ireland'] * 50 + ['Australia'] * 25 + ['Canada'] * 25
    
    invoices = []
    current_invoice_num = 536365
    
    customer_weights = [random.random() for _ in customer_ids]
    total_weight = sum(customer_weights)
    customer_weights = [w/total_weight for w in customer_weights]
    
    start_date = datetime(2009, 12, 1)
    end_date = datetime(2011, 12, 9)
    date_range = (end_date - start_date).days
    
    for inv_idx in range(num_invoices):
        invoice_no = str(current_invoice_num + inv_idx)
        
        # 5% chance of cancellation
        is_cancellation = random.random() < 0.05
        if is_cancellation:
            invoice_no = 'C' + invoice_no
        
        # 20% chance of missing CustomerID
        if random.random() < 0.2:
            cust_id = np.nan
        else:
            cust_id = np.random.choice(customer_ids, p=customer_weights)
        
        if pd.isna(cust_id):
            country = random.choice(['United Kingdom', 'Germany', 'France'])
        else:
            country = random.choice(country_list)
        
        days_offset = random.randint(0, date_range)
        invoice_date = start_date + timedelta(days=days_offset)
        
        # Seasonality: more items in Nov-Dec
        if invoice_date.month in [11, 12]:
            num_items = random.randint(5, 20)
        else:
            num_items = random.randint(2, 15)
        
        selected_products = products_df.sample(n=num_items, replace=True)
        for _, product in selected_products.iterrows():
            quantity = random.randint(1, 10)
            
            if random.random() < 0.05:  # Bulk orders
                quantity = random.randint(50, 200)
            
            if is_cancellation:
                quantity = -quantity
            
            invoices.append({
                'InvoiceNo': invoice_no,
                'StockCode': product['StockCode'],
                'Description': product['Description'],
                'Quantity': quantity,
                'InvoiceDate': invoice_date.strftime('%m/%d/%Y %H:%M'),
                'UnitPrice': product['UnitPrice'],
                'CustomerID': cust_id,
                'Country': country
            })
    
    return pd.DataFrame(invoices)

def main():
    """Generate and save the dataset."""
    print("=" * 60)
    print("Generating Synthetic Online Retail Dataset")
    print("=" * 60)
    
    print("\n📦 Generating invoices...")
    df = generate_invoice_data()
    
    # Shuffle rows
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Create directories
    from pathlib import Path
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    
    # Save
    output_path = 'data/raw/online_retail_II_synthetic.csv'
    df.to_csv(output_path, index=False, float_format='%.2f')
    
    print(f"\n✅ Dataset generated successfully!")
    print(f"   Rows: {len(df):,}")
    print(f"   Unique invoices: {df['InvoiceNo'].nunique():,}")
    print(f"   Unique customers: {df['CustomerID'].nunique():,}")
    print(f"   Cancellations: {df[df['InvoiceNo'].str.startswith('C')].shape[0]:,} rows")
    print(f"\n   Saved to: {output_path}")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()