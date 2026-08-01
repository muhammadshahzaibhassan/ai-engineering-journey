"""
Module 2 — Data Cleaning (generic, schema-driven).

Takes the raw dataframe + detected schema and returns:
  - cleaned_df: analysis-ready rows
  - returns_df: rows identified as refunds/cancellations (negative quantity),
                kept separately rather than discarded
  - log: list of human-readable strings describing every decision made,
         so the frontend can show "what we did to your data"
"""
from __future__ import annotations
import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame, schema: dict) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    log: list[str] = []
    df = df.copy()
    start_rows = len(df)

    order_col = schema.get("order_id")
    cust_col = schema.get("customer_id")
    date_col = schema.get("date")
    qty_col = schema.get("quantity")
    price_col = schema.get("unit_price")
    rev_col = schema.get("revenue")

    # 1. Drop exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    if before - len(df):
        log.append(f"Dropped {before - len(df)} exact duplicate rows.")

    # 2. Drop rows with no customer id (can't attribute revenue to an unknown customer)
    if cust_col:
        before = len(df)
        df = df[df[cust_col].notna()]
        if before - len(df):
            log.append(f"Dropped {before - len(df)} rows missing {cust_col} (customer ID).")

    # 3. Fill missing product descriptions from other rows with the same product id
    prod_name_col = schema.get("product_name")
    prod_id_col = schema.get("product_id")
    if prod_name_col and prod_id_col:
        n_missing = df[prod_name_col].isna().sum()
        if n_missing:
            lookup = (
                df.dropna(subset=[prod_name_col])
                  .drop_duplicates(subset=[prod_id_col])
                  .set_index(prod_id_col)[prod_name_col]
            )
            df[prod_name_col] = df[prod_name_col].fillna(df[prod_id_col].map(lookup))
            filled = n_missing - df[prod_name_col].isna().sum()
            log.append(f"Filled {filled} missing {prod_name_col} values from matching {prod_id_col}.")

    # 4. Type conversion: date
    if date_col:
        before_na = df[date_col].isna().sum()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        new_na = df[date_col].isna().sum() - before_na
        if new_na > 0:
            log.append(f"{new_na} rows had an unparseable date and were set to NaT.")
        before = len(df)
        df = df[df[date_col].notna()]
        if before - len(df):
            log.append(f"Dropped {before - len(df)} rows with an invalid/missing date.")

    # 5. Coerce quantity/price/revenue to numeric
    for col in [qty_col, price_col, rev_col]:
        if col:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. Separate returns (negative quantity) from sales
    returns_df = pd.DataFrame()
    if qty_col:
        is_return = df[qty_col] < 0
        if order_col:
            is_return = is_return | df[order_col].astype(str).str.upper().str.startswith("C")
        returns_df = df[is_return].copy()
        df = df[~is_return].copy()
        if len(returns_df):
            log.append(f"Separated {len(returns_df)} rows identified as returns/cancellations (negative quantity or 'C'-prefixed order ID) into a returns table.")

    # 7. Drop non-positive price / revenue rows (data errors)
    for col, label in [(price_col, "unit price"), (rev_col, "revenue")]:
        if col:
            before = len(df)
            df = df[df[col] > 0]
            if before - len(df):
                log.append(f"Dropped {before - len(df)} rows with zero/negative {label} (data errors).")

    # 8. Outlier flagging on quantity via IQR (flag, don't silently drop)
    if qty_col and len(df) > 20:
        q1, q3 = df[qty_col].quantile([0.25, 0.75])
        iqr = q3 - q1
        upper = q3 + 3 * iqr  # generous multiplier -- flag extreme, not merely "unusual"
        n_outliers = int((df[qty_col] > upper).sum())
        if n_outliers:
            df["_qty_outlier_flag"] = df[qty_col] > upper
            log.append(f"Flagged {n_outliers} rows with unusually high {qty_col} (> {upper:.0f}, IQR method) via _qty_outlier_flag rather than removing them.")

    log.insert(0, f"Started with {start_rows:,} rows, {len(df):,} remain after cleaning ({len(returns_df):,} moved to returns).")
    return df.reset_index(drop=True), returns_df.reset_index(drop=True), log
