"""
Streamlit page - Customer Analytics.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add project root and src to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from utils import load_customer_features, load_cleaned_data

st.set_page_config(page_title="Customer Analytics", layout="wide")
st.title("👥 Customer Insights")

# Load data
try:
    df_cust = load_customer_features()
    df_trans = load_cleaned_data()
except FileNotFoundError:
    st.error("Processed data not found. Please run the data pipeline.")
    st.stop()

# Repeat customer rate
repeat_rate = (df_cust['NumOrders'] > 1).mean() * 100
st.metric("Repeat Customer Rate", f"{repeat_rate:.1f}%")

# Top 20 customers
top_customers = df_cust.nlargest(20, 'TotalSpent')[['CustomerID', 'TotalSpent', 'NumOrders', 'Recency']]
st.subheader("🏆 Top 20 Customers by Spend")
st.dataframe(top_customers.style.format({'TotalSpent': '${:,.2f}'}))

# Customer Segment distribution
seg_counts = df_cust['CustomerSegment'].value_counts().reset_index()
seg_counts.columns = ['Segment', 'Count']
fig1 = px.pie(seg_counts, values='Count', names='Segment', title='Customer Segment Distribution')
st.plotly_chart(fig1, use_container_width=True)

# Recency distribution
fig2 = px.histogram(df_cust, x='Recency', nbins=30, title='Recency Distribution (days since last purchase)')
st.plotly_chart(fig2, use_container_width=True)

# Monetary distribution
fig3 = px.histogram(df_cust, x='TotalSpent', nbins=30, title='Total Spend Distribution')
st.plotly_chart(fig3, use_container_width=True)