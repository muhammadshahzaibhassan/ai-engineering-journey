"""
Streamlit page - Model Performance.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Model Evaluation", layout="wide")
st.title("📊 Model Performance")

# Load comparison table
try:
    df_comp = pd.read_csv('outputs/metrics/model_comparison.csv')
except FileNotFoundError:
    st.error("Model comparison not found. Please run evaluation first.")
    st.stop()

st.subheader("Model Comparison")
st.dataframe(df_comp.style.format({
    'Accuracy': '{:.2%}',
    'Precision': '{:.2%}',
    'Recall': '{:.2%}',
    'F1': '{:.2%}',
    'ROC_AUC': '{:.2%}'
}))

# Confusion matrices
img_path = Path('outputs/plots/confusion_matrices.png')
if img_path.exists():
    st.subheader("Confusion Matrices")
    img = Image.open(img_path)
    st.image(img, use_column_width=True)
else:
    st.warning("Confusion matrix plot not found. Run evaluation to generate.")

# Feature importances
img_path2 = Path('outputs/plots/feature_importance.png')
if img_path2.exists():
    st.subheader("Feature Importances (Random Forest)")
    img2 = Image.open(img_path2)
    st.image(img2, use_column_width=True)
else:
    st.info("Feature importance plot not available (only for Random Forest).")