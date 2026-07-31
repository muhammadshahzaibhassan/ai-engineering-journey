"""
Model training module.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

from .preprocessing import build_preprocessor
from .feature_engineering import build_customer_features  # for reference

def train_models(customer_features_path: str, model_dir: str = 'models/'):
    """
    Load customer features, define target, split, build pipelines, train, and save models.

    Args:
        customer_features_path (str): Path to customer_features.csv.
        model_dir (str): Directory to save models.
    """
    # Load data
    df = pd.read_csv(customer_features_path)
    # Define target: RepeatCustomer = 1 if NumOrders > 1 (or could define based on time cutoff)
    # Here we use a simple definition: repeat customer if more than one order.
    df['RepeatCustomer'] = (df['NumOrders'] > 1).astype(int)

    # Features: Recency, Frequency, Revenue (TotalSpent), AvgBasketSize, Country, CustomerSegment
    # We'll use TotalSpent as Monetary, but we can also use Monetary directly.
    features = ['Recency', 'Frequency', 'TotalSpent', 'AvgBasketSize', 'Country', 'CustomerSegment']
    X = df[features]
    y = df['RepeatCustomer']

    # Split stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Define numeric and categorical columns
    numeric_cols = ['Recency', 'Frequency', 'TotalSpent', 'AvgBasketSize']
    categorical_cols = ['Country', 'CustomerSegment']

    # Build preprocessor
    preprocessor = build_preprocessor(numeric_cols, categorical_cols)

    # Models
    models = {
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(random_state=42, n_estimators=100)
    }

    # Create directory if not exists
    Path(model_dir).mkdir(parents=True, exist_ok=True)

    for name, model in models.items():
        # Build full pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        # Train
        pipeline.fit(X_train, y_train)
        # Save
        joblib.dump(pipeline, f"{model_dir}/{name}.pkl")
        print(f"Trained and saved {name}")

    # Also save the test set for evaluation later
    X_test.to_csv('outputs/metrics/X_test.csv', index=False)
    y_test.to_csv('outputs/metrics/y_test.csv', index=False)

if __name__ == '__main__':
    # Example execution
    train_models('data/processed/customer_features.csv')