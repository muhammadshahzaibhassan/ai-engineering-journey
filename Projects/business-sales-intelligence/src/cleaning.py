"""
Data cleaning module.
"""
import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw Online Retail dataset.
    """
    df = df.copy()

    # Drop rows without CustomerID
    df.dropna(subset=['CustomerID'], inplace=True)

    # Drop exact duplicates
    df.drop_duplicates(inplace=True)

    # Remove rows with negative or zero UnitPrice
    df = df[df['UnitPrice'] > 0]

    # Remove rows with negative Quantity (returns)
    df = df[df['Quantity'] > 0]

    # Convert InvoiceDate to datetime
    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Fill missing Description
    if 'Description' in df.columns and 'StockCode' in df.columns:
        desc_map = df.groupby('StockCode')['Description'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
        df['Description'] = df.apply(
            lambda row: desc_map.get(row['StockCode'], 'Unknown') if pd.isna(row['Description']) else row['Description'],
            axis=1
        )

    # Outlier capping
    for col in ['Quantity', 'UnitPrice']:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df[col] = df[col].clip(lower=lower, upper=upper)

    # ========== ADD REVENUE COLUMN ==========
    df['Revenue'] = df['Quantity'] * df['UnitPrice']

    return df