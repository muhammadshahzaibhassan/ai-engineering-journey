"""
Preprocessing pipeline construction for machine learning.
"""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

def build_preprocessor(numeric_features, categorical_features):
    """
    Build a ColumnTransformer with scaling for numeric features and one-hot encoding for categorical.

    Args:
        numeric_features (list): List of numeric column names.
        categorical_features (list): List of categorical column names.

    Returns:
        ColumnTransformer: Preprocessor object.
    """
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    return preprocessor