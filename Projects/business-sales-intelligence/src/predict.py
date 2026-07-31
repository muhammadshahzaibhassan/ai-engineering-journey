"""
Prediction module for loading model and making predictions on new input.
"""
import joblib
import pandas as pd
from pathlib import Path

def load_model(model_name='RandomForest', model_dir='models/'):
    """
    Load a saved model pipeline.

    Args:
        model_name (str): Name of the model (e.g., 'RandomForest').
        model_dir (str): Directory containing model .pkl files.

    Returns:
        Pipeline: Loaded scikit-learn pipeline.
    """
    model_path = Path(model_dir) / f"{model_name}.pkl"
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    return joblib.load(model_path)

def predict_repeat(pipeline, input_data: dict) -> dict:
    """
    Predict repeat purchase probability for a single customer.

    Args:
        pipeline: Trained pipeline with preprocessor and classifier.
        input_data (dict): Dictionary containing features:
            - Recency (int)
            - Frequency (float)
            - TotalSpent (float)
            - AvgBasketSize (float)
            - Country (str)
            - CustomerSegment (str)

    Returns:
        dict: {'probability': float, 'prediction': int}
    """
    # Convert to DataFrame
    df = pd.DataFrame([input_data])
    # Ensure columns order matches training
    expected_cols = ['Recency', 'Frequency', 'TotalSpent', 'AvgBasketSize', 'Country', 'CustomerSegment']
    df = df[expected_cols]
    proba = pipeline.predict_proba(df)[0, 1]
    pred = (proba >= 0.5).astype(int)
    return {'probability': proba, 'prediction': pred}