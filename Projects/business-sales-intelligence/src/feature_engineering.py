"""
Feature engineering module for customer-level aggregations and derived features.
"""
import pandas as pd
import numpy as np

def build_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build customer-level feature table from cleaned transaction data.

    Args:
        df (pd.DataFrame): Cleaned transaction data with columns:
            InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country, etc.

    Returns:
        pd.DataFrame: Customer-level dataframe with features:
            - CustomerID
            - TotalSpent
            - AvgBasketSize (average quantity per invoice)
            - NumOrders
            - Recency (days since last purchase)
            - Frequency (orders per month)
            - Monetary (same as TotalSpent)
            - Country (most frequent country for that customer)
            - HighValueCustomer (binary, top quartile by TotalSpent)
            - CustomerSegment (Gold/Silver/Bronze based on tertiles)
    """
    df = df.copy()

    # Create Revenue per transaction line
    df['Revenue'] = df['Quantity'] * df['UnitPrice']

    # Extract date features for aggregations
    # We'll compute Recency relative to the last date in dataset + 1 day
    max_date = df['InvoiceDate'].max()
    analysis_date = max_date + pd.Timedelta(days=1)

    # Group by CustomerID
    customer_group = df.groupby('CustomerID')

    # Basic aggregations
    customer_features = customer_group.agg(
        TotalSpent=('Revenue', 'sum'),
        NumOrders=('InvoiceNo', 'nunique'),
        AvgBasketSize=('Quantity', 'mean'),  # average items per transaction line? Better: per invoice.
        LastPurchaseDate=('InvoiceDate', 'max'),
        Country=('Country', lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    ).reset_index()

    # Recency: days since last purchase
    customer_features['Recency'] = (analysis_date - customer_features['LastPurchaseDate']).dt.days

    # Frequency: orders per month (tenure in months)
    # Tenure: from first purchase to last purchase, in months
    first_purchase = customer_group['InvoiceDate'].min().rename('FirstPurchaseDate')
    customer_features = customer_features.merge(first_purchase, on='CustomerID')
    tenure_days = (customer_features['LastPurchaseDate'] - customer_features['FirstPurchaseDate']).dt.days
    # Avoid division by zero for customers with only one purchase (tenure = 0)
    tenure_months = np.maximum(tenure_days / 30.44, 1.0)  # approximate months
    customer_features['Frequency'] = customer_features['NumOrders'] / tenure_months

    # Monetary is already TotalSpent
    customer_features['Monetary'] = customer_features['TotalSpent']

    # Segment labels: HighValueCustomer (top quartile)
    quartile_threshold = customer_features['TotalSpent'].quantile(0.75)
    customer_features['HighValueCustomer'] = (customer_features['TotalSpent'] >= quartile_threshold).astype(int)

    # CustomerSegment: based on tertiles of TotalSpent
    tertiles = customer_features['TotalSpent'].quantile([0.33, 0.67]).values
    def segment_label(spent):
        if spent >= tertiles[1]:
            return 'Gold'
        elif spent >= tertiles[0]:
            return 'Silver'
        else:
            return 'Bronze'
    customer_features['CustomerSegment'] = customer_features['TotalSpent'].apply(segment_label)

    # Drop temporary columns
    customer_features.drop(['LastPurchaseDate', 'FirstPurchaseDate'], axis=1, inplace=True)

    return customer_features