"""
Streamlit page - Sales trends.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils import load_cleaned_data

st.set_page_config(page_title="Sales Analysis", layout="wide")
st.title("📈 Sales Trends")

# Load cleaned data
try:
    df = load_cleaned_data()
    # Ensure InvoiceDate is datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    # Create Revenue column if not present (should be)
    if 'Revenue' not in df.columns:
        df['Revenue'] = df['Quantity'] * df['UnitPrice']
except FileNotFoundError:
    st.error("Processed data not found. Please run the data pipeline.")
    st.stop()

# Monthly revenue trend
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
monthly_revenue = df.groupby('YearMonth')['Revenue'].sum().reset_index()
fig1 = px.line(monthly_revenue, x='YearMonth', y='Revenue', title='Monthly Revenue Trend')
st.plotly_chart(fig1, use_container_width=True)

# Daily trend (optional)
df['Date'] = df['InvoiceDate'].dt.date
daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()
fig2 = px.line(daily_revenue, x='Date', y='Revenue', title='Daily Revenue Trend')
st.plotly_chart(fig2, use_container_width=True)

# Country-wise sales
country_revenue = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).reset_index()
fig3 = px.bar(country_revenue.head(15), x='Country', y='Revenue', title='Top 15 Countries by Revenue')
st.plotly_chart(fig3, use_container_width=True)

# Additional: top products by revenue
product_revenue = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).reset_index().head(10)
fig4 = px.bar(product_revenue, x='Description', y='Revenue', title='Top 10 Products by Revenue')
st.plotly_chart(fig4, use_container_width=True)