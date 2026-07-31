"""
Data cleaning module.
"""
import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw Online Retail dataset.

    Steps:
    1. Drop rows without CustomerID (cannot attribute revenue).
    2. Drop exact duplicates.
    3. Remove negative or zero UnitPrice.
    4. Separate negative Quantity as returns (drop from main, but could be stored; here we drop for simplicity).
    5. Convert InvoiceDate to datetime.
    6. Cap extreme outliers in Quantity and UnitPrice using IQR method (optional: flag instead of cap).
    7. Fill missing Description using StockCode mapping (fallback to 'Unknown').

    Args:
        df (pd.DataFrame): Raw dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    df = df.copy()

    # Drop rows without CustomerID
    df.dropna(subset=['CustomerID'], inplace=True)

    # Drop exact duplicates
    df.drop_duplicates(inplace=True)

    # Remove rows with negative or zero UnitPrice (likely errors)
    df = df[df['UnitPrice'] > 0]

    # Remove rows with negative Quantity (returns) for analysis; we could keep separately, but we drop for simplicity
    # In a production system, returns would be handled separately.
    df = df[df['Quantity'] > 0]

    # Convert InvoiceDate to datetime
    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Fill missing Description with most common description for that StockCode, else 'Unknown'
    if 'Description' in df.columns and 'StockCode' in df.columns:
        desc_map = df.groupby('StockCode')['Description'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
        df['Description'] = df.apply(
            lambda row: desc_map.get(row['StockCode'], 'Unknown') if pd.isna(row['Description']) else row['Description'],
            axis=1
        )

    # Outlier detection and capping using IQR for Quantity and UnitPrice (optional)
    for col in ['Quantity', 'UnitPrice']:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            # Cap extreme values
            df[col] = df[col].clip(lower=lower, upper=upper)

    return df