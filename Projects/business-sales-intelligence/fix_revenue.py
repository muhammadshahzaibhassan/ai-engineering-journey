"""
One-time script to add Revenue column to cleaned data.
"""
import pandas as pd
from pathlib import Path

def fix_cleaned_data():
    """Add Revenue column to cleaned_data.csv if it doesn't exist."""
    
    # Load the cleaned data
    cleaned_path = 'data/processed/cleaned_data.csv'
    
    if not Path(cleaned_path).exists():
        print(f"❌ {cleaned_path} not found. Run main.py first.")
        return
    
    df = pd.read_csv(cleaned_path)
    
    # Check if Revenue column exists
    if 'Revenue' in df.columns:
        print("✅ Revenue column already exists.")
        return
    
    # Add Revenue column
    print("Adding Revenue column...")
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    # Save back
    df.to_csv(cleaned_path, index=False)
    print(f"✅ Revenue column added to {cleaned_path}")
    print(f"   Total Revenue: ${df['Revenue'].sum():,.2f}")
    
    # Also check customer_features
    customer_path = 'data/processed/customer_features.csv'
    if Path(customer_path).exists():
        print(f"\n📊 Rebuilding customer features to include Revenue...")
        # We need to rebuild customer features with the Revenue column
        # But feature_engineering.py already creates Revenue internally
        # So we just need to notify the user
        print("   Run 'python main.py' again to rebuild customer features with Revenue data.")

if __name__ == '__main__':
    fix_cleaned_data()