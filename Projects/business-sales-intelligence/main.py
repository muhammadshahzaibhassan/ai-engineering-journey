"""
Main entry point to run the entire pipeline:
1. Load raw data
2. Clean
3. Feature engineering (customer-level)
4. Train models
5. Evaluate models
"""
from src.data_loader import load_raw_data
from src.cleaning import clean_data
from src.feature_engineering import build_customer_features
from src.train import train_models
from src.evaluate import evaluate_models
from pathlib import Path

def run_pipeline(raw_data_path='data/raw/online_retail_II.xlsx'):
    """
    Execute the full data and model pipeline.
    """
    # 1. Load
    print("Loading raw data...")
    df_raw = load_raw_data(raw_data_path)

    # 2. Clean
    print("Cleaning data...")
    df_clean = clean_data(df_raw)
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    df_clean.to_csv('data/processed/cleaned_data.csv', index=False)
    print("Cleaned data saved to data/processed/cleaned_data.csv")

    # 3. Feature engineering
    print("Building customer features...")
    df_customers = build_customer_features(df_clean)
    df_customers.to_csv('data/processed/customer_features.csv', index=False)
    print("Customer features saved to data/processed/customer_features.csv")

    # 4. Train models
    print("Training models...")
    train_models('data/processed/customer_features.csv')

    # 5. Evaluate models
    print("Evaluating models...")
    evaluate_models()

    print("Pipeline complete.")

if __name__ == '__main__':
    run_pipeline()