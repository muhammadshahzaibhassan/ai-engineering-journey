"""
Data loader module for loading raw dataset.
"""
import pandas as pd
from pathlib import Path

def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Load raw dataset from CSV or Excel file.

    Args:
        file_path (str): Path to the raw data file.

    Returns:
        pd.DataFrame: Loaded dataframe.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file extension is not supported.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    ext = file_path.suffix.lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .csv, .xls, or .xlsx.")
    return df