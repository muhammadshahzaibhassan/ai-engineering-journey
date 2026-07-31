"""
Streamlit page - Predict Repeat Purchase.
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.predict import load_model, predict_repeat
from src.utils import load_customer_features

st.set_page_config(page_title="Prediction", layout="wide")
st.title("🔮 Predict Repeat Purchase")

# Load model (default: RandomForest)
model_name = st.selectbox("Select Model", ['RandomForest', 'LogisticRegression', 'DecisionTree'])
try:
    pipeline = load_model(model_name)
except FileNotFoundError:
    st.error(f"Model {model_name} not found. Please train models first.")
    st.stop()

# Input form
st.sidebar.header("Customer Features")
recency = st.sidebar.number_input("Recency (days since last purchase)", min_value=0, value=30)
frequency = st.sidebar.number_input("Frequency (orders per month)", min_value=0.0, value=0.5, step=0.1)
total_spent = st.sidebar.number_input("Total Spent ($)", min_value=0.0, value=500.0)
avg_basket = st.sidebar.number_input("Avg Basket Size (items per order)", min_value=0.0, value=10.0)
country = st.sidebar.selectbox("Country", ['United Kingdom', 'Germany', 'France', 'USA', 'Other'])
segment = st.sidebar.selectbox("Customer Segment", ['Gold', 'Silver', 'Bronze'])

# When user clicks predict
if st.sidebar.button("Predict"):
    input_data = {
        'Recency': recency,
        'Frequency': frequency,
        'TotalSpent': total_spent,
        'AvgBasketSize': avg_basket,
        'Country': country,
        'CustomerSegment': segment
    }
    result = predict_repeat(pipeline, input_data)
    prob = result['probability']
    pred = result['prediction']

    col1, col2 = st.columns(2)
    col1.metric("Probability of Repeat Purchase", f"{prob:.2%}")
    col2.metric("Prediction", "Yes" if pred == 1 else "No")

    # Simple gauge or progress bar
    st.progress(prob)

    st.info("Note: This prediction is based on the trained model and the input features. It is for demonstration purposes only.")