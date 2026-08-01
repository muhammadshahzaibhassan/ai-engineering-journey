"""
Utility functions for the project.
"""
import pandas as pd
from pathlib import Path

def load_cleaned_data(path='data/processed/cleaned_data.csv'):
    """Load the cleaned transaction data."""
    df = pd.read_csv(path)
    # Ensure Revenue column exists (fallback)
    if 'Revenue' not in df.columns:
        print("⚠️  Revenue column not found. Creating from Quantity * UnitPrice...")
        df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

def load_customer_features(path='data/processed/customer_features.csv'):
    """Load the customer features table."""
    return pd.read_csv(path)

def compute_kpis(df_transactions, df_customers):
    """
    Compute overall KPIs from cleaned transaction data and customer features.
    """
    # Ensure Revenue column exists
    if 'Revenue' not in df_transactions.columns:
        df_transactions['Revenue'] = df_transactions['Quantity'] * df_transactions['UnitPrice']
    
    total_revenue = df_transactions['Revenue'].sum()
    total_orders = df_transactions['InvoiceNo'].nunique()
    total_customers = df_customers['CustomerID'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'avg_order_value': avg_order_value
    }

def generate_report(output_path='outputs/reports/business_report.md'):
    """Generate a business report."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("# Business Sales Intelligence Report\n\n")
        f.write("## KPIs\n\n")
        f.write("(Generated from data)\n")
        f.write("## Charts\n\n")
        f.write("See outputs/plots/ for visualizations.\n")
    print(f"Report generated at {output_path}")