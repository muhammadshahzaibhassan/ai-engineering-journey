"""
Streamlit app - Home page with KPIs.
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root and src to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from src.utils import load_cleaned_data, load_customer_features, compute_kpis

st.set_page_config(page_title="Sales Intelligence Dashboard", layout="wide")
st.title("📊 Business Sales Intelligence Dashboard")

# Load data
try:
    df_trans = load_cleaned_data()
    df_cust = load_customer_features()
    kpis = compute_kpis(df_trans, df_cust)
except FileNotFoundError:
    st.error("Processed data not found. Please run the data pipeline first (python main.py).")
    st.stop()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"${kpis['total_revenue']:,.0f}")
col2.metric("📦 Total Orders", f"{kpis['total_orders']:,}")
col3.metric("👥 Total Customers", f"{kpis['total_customers']:,}")
col4.metric("📈 Average Order Value", f"${kpis['avg_order_value']:,.2f}")

st.markdown("---")
st.markdown("""
### Welcome to the Sales Intelligence Platform

This dashboard provides insights into your sales data, customer behavior, and predictive analytics.
Use the sidebar to navigate through different sections:

- **Sales** – View sales trends by month and country.
- **Customers** – Explore customer segmentation and top spenders.
- **Prediction** – Predict if a customer will purchase again.
- **Model** – See model performance and feature importance.

All data is based on the Online Retail II dataset.
""")