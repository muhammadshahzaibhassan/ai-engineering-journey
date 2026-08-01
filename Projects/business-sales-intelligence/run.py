"""
Simple runner that sets up the environment and runs the pipeline
"""
import sys
import os
from pathlib import Path

# Add the project root and src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# Now import and run
from src.data_loader import load_raw_data
from src.cleaning import clean_data
from src.feature_engineering import build_customer_features
from src.train import train_models
from src.evaluate import evaluate_models

def run_pipeline():
    """Run the complete pipeline"""
    print("=" * 60)
    print("Business Sales Intelligence - Pipeline")
    print("=" * 60)
    
    # Create directories
    for folder in ['data/processed', 'models', 'outputs/metrics', 'outputs/plots', 'outputs/reports']:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created/verified")
    
    # 1. Load
    print("\n📂 Loading raw data...")
    df_raw = load_raw_data('data/raw/online_retail_II_synthetic.csv')
    print(f"   Loaded {len(df_raw):,} rows")
    
    # 2. Clean
    print("\n🧹 Cleaning data...")
    df_clean = clean_data(df_raw)
    df_clean.to_csv('data/processed/cleaned_data.csv', index=False)
    print(f"   Cleaned data saved: {len(df_clean):,} rows")
    
    # 3. Feature engineering
    print("\n🔧 Building customer features...")
    df_customers = build_customer_features(df_clean)
    df_customers.to_csv('data/processed/customer_features.csv', index=False)
    print(f"   Customer features saved: {len(df_customers):,} customers")
    
    # 4. Train
    print("\n🤖 Training models...")
    train_models('data/processed/customer_features.csv')
    
    # 5. Evaluate
    print("\n📊 Evaluating models...")
    evaluate_models()
    
    print("\n" + "=" * 60)
    print("✅ Pipeline complete!")
    print("   Launch dashboard: streamlit run app/Home.py")
    print("=" * 60)

if __name__ == '__main__':
    run_pipeline()