"""
Module 4 — Feature Engineering (generic, schema-driven).

Adds a `revenue` column to the transaction-level df (computed or copied
from the detected revenue column), plus date parts. Then aggregates to
one row per customer with RFM-style features used by both the customer
analytics module and the ML module.
"""
from __future__ import annotations
import pandas as pd
import numpy as np


def add_transaction_features(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    df = df.copy()
    qty_col = schema.get("quantity")
    price_col = schema.get("unit_price")
    rev_col = schema.get("revenue")
    date_col = schema.get("date")

    if schema.get("_revenue_mode") == "computed":
        df["revenue"] = df[qty_col] * df[price_col]
    elif schema.get("_revenue_mode") == "explicit":
        df["revenue"] = df[rev_col]
    else:
        df["revenue"] = np.nan

    if date_col:
        df["_month"] = df[date_col].dt.to_period("M").astype(str)
        df["_year"] = df[date_col].dt.year
        df["_quarter"] = df[date_col].dt.quarter
        df["_weekday"] = df[date_col].dt.day_name()
        df["_is_weekend"] = df[date_col].dt.dayofweek >= 5

    return df


def build_customer_features(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """One row per customer. Returns empty df if no customer_id detected."""
    cust_col = schema.get("customer_id")
    order_col = schema.get("order_id")
    date_col = schema.get("date")

    if not cust_col:
        return pd.DataFrame()

    df = df.copy()
    analysis_date = df[date_col].max() + pd.Timedelta(days=1) if date_col else None

    agg = {"revenue": "sum"}
    if order_col:
        agg[order_col] = "nunique"

    grouped = df.groupby(cust_col).agg(agg).rename(columns={
        "revenue": "TotalSpent",
        order_col: "NumOrders",
    } if order_col else {"revenue": "TotalSpent"})

    if not order_col:
        grouped["NumOrders"] = df.groupby(cust_col).size()

    # Average basket size = avg revenue-bearing rows per order
    if order_col:
        rows_per_order = df.groupby([cust_col, order_col]).size().groupby(cust_col).mean()
        grouped["AvgBasketSize"] = rows_per_order
    else:
        grouped["AvgBasketSize"] = df.groupby(cust_col).size() / grouped["NumOrders"].replace(0, 1)

    if date_col:
        last_purchase = df.groupby(cust_col)[date_col].max()
        first_purchase = df.groupby(cust_col)[date_col].min()
        grouped["Recency"] = (analysis_date - last_purchase).dt.days
        tenure_months = ((analysis_date - first_purchase).dt.days / 30.44).clip(lower=1)
        grouped["Frequency"] = grouped["NumOrders"] / tenure_months
    else:
        grouped["Recency"] = np.nan
        grouped["Frequency"] = np.nan

    country_col = schema.get("country")
    if country_col:
        top_country = df.groupby(cust_col)[country_col].agg(lambda s: s.mode().iat[0] if not s.mode().empty else None)
        grouped["Country"] = top_country

    grouped = grouped.reset_index().rename(columns={cust_col: "CustomerID"})

    # Derived labels
    if grouped["TotalSpent"].notna().any():
        q75 = grouped["TotalSpent"].quantile(0.75)
        grouped["HighValueCustomer"] = (grouped["TotalSpent"] >= q75).astype(int)
        try:
            grouped["CustomerSegment"] = pd.qcut(
                grouped["TotalSpent"], q=3, labels=["Bronze", "Silver", "Gold"], duplicates="drop"
            ).astype(str)
        except ValueError:
            grouped["CustomerSegment"] = "Silver"
    else:
        grouped["HighValueCustomer"] = 0
        grouped["CustomerSegment"] = "Unknown"

    grouped["RepeatCustomer"] = (grouped["NumOrders"] > 1).astype(int)

    return grouped
