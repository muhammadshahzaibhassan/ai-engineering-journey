"""
Business Sales Intelligence Dashboard — FastAPI backend.

Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Deploy: see README.md (built for Render, works on any Python host).
"""
from __future__ import annotations
import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

from app import store, schema_detection, cleaning, feature_engineering, analytics, ml

app = FastAPI(title="Business Sales Intelligence API", version="1.0")

# In production, replace "*" with your Vercel frontend URL for tighter security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get(session_id: str) -> store.Session:
    try:
        return store.get_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found or expired. Please re-upload your CSV.")


@app.get("/")
def health():
    return {"status": "ok", "service": "business-sales-intelligence-api"}


# ---------------------------------------------------------------------------
# 1. Upload
# ---------------------------------------------------------------------------
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".csv", ".txt")):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")

    raw_bytes = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw_bytes), encoding_errors="ignore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {e}")

    if df.empty or len(df.columns) < 2:
        raise HTTPException(status_code=400, detail="CSV appears to be empty or malformed.")

    session = store.create_session()
    session.filename = file.filename
    session.raw_df = df
    session.schema = schema_detection.detect_schema(df)
    session.warnings = schema_detection.validate_schema(session.schema)

    return {
        "session_id": session.id,
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "detected_schema": {k: v for k, v in session.schema.items() if not k.startswith("_")},
        "revenue_mode": session.schema.get("_revenue_mode"),
        "warnings": session.warnings,
        "preview": df.head(5).astype(str).to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# 2. Clean + Feature-engineer (runs both -- cheap enough to do together)
# ---------------------------------------------------------------------------
@app.post("/process/{session_id}")
def process(session_id: str):
    session = _get(session_id)
    if session.raw_df is None:
        raise HTTPException(status_code=400, detail="No data uploaded for this session.")

    cleaned, returns_df, log = cleaning.clean_data(session.raw_df, session.schema)
    cleaned = feature_engineering.add_transaction_features(cleaned, session.schema)
    cust_features = feature_engineering.build_customer_features(cleaned, session.schema)

    session.cleaned_df = cleaned
    session.returns_df = returns_df
    session.cleaning_log = log
    session.customer_features = cust_features

    return {
        "session_id": session.id,
        "cleaning_log": log,
        "cleaned_rows": len(cleaned),
        "returns_rows": len(returns_df),
        "customers_found": len(cust_features),
        "kpis": analytics.kpis(cleaned, session.schema, cust_features),
    }


# ---------------------------------------------------------------------------
# 3. EDA / Sales analytics
# ---------------------------------------------------------------------------
@app.get("/analytics/sales/{session_id}")
def sales_analytics(session_id: str):
    session = _get(session_id)
    _require_processed(session)
    df, schema = session.cleaned_df, session.schema
    return {
        "kpis": analytics.kpis(df, schema, session.customer_features),
        "monthly_trend": analytics.monthly_trend(df, schema),
        "revenue_by_country": analytics.revenue_by_country(df, schema),
        "top_products": analytics.top_products(df, schema),
        "revenue_distribution": analytics.revenue_distribution(df, schema),
    }


# ---------------------------------------------------------------------------
# 4. Customer analytics
# ---------------------------------------------------------------------------
@app.get("/analytics/customers/{session_id}")
def customer_analytics(session_id: str):
    session = _get(session_id)
    _require_processed(session)
    cf = session.customer_features
    if not len(cf):
        raise HTTPException(status_code=400, detail="No customer ID column was detected -- customer analytics unavailable for this file.")
    segment_breakdown = []
    if "CustomerSegment" in cf:
        vc = cf["CustomerSegment"].value_counts()
        segment_breakdown = [{"segment": str(k), "count": int(v)} for k, v in vc.items()]

    return {
        "top_customers": analytics.top_customers(cf),
        "rfm_segments": analytics.rfm_segments(cf),
        "segment_breakdown": segment_breakdown,
        "frequently_bought_together": analytics.frequently_bought_together(session.cleaned_df, session.schema),
    }


# ---------------------------------------------------------------------------
# 5. Train models
# ---------------------------------------------------------------------------
@app.post("/model/train/{session_id}")
def train_model(session_id: str):
    session = _get(session_id)
    _require_processed(session)
    if not len(session.customer_features):
        raise HTTPException(status_code=400, detail="No customer-level features available -- cannot train a repeat-purchase model.")

    result = ml.train_and_evaluate(session.customer_features)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    session.models = result["pipelines"]
    session.metrics = result["metrics"]
    session.feature_importance = result["feature_importance"]
    session.best_model_name = result["best_model_name"]
    session._numeric_cols = result["numeric_cols"]
    session._categorical_cols = result["categorical_cols"]

    return {
        "metrics": result["metrics"],
        "confusion_matrices": result["confusion_matrices"],
        "best_model_name": result["best_model_name"],
        "feature_importance": result["feature_importance"],
        "class_balance": result["class_balance"],
        "train_size": result["train_size"],
        "test_size": result["test_size"],
        "available_models": list(session.models.keys()),
        "input_fields": {
            "numeric": result["numeric_cols"],
            "categorical": result["categorical_cols"],
        },
    }


# ---------------------------------------------------------------------------
# 6. Predict
# ---------------------------------------------------------------------------
@app.post("/model/predict/{session_id}")
def predict(session_id: str, payload: dict = Body(...)):
    session = _get(session_id)
    if not session.models:
        raise HTTPException(status_code=400, detail="No trained model for this session yet. Call /model/train first.")

    model_name = payload.get("model_name") or session.best_model_name
    pipeline = session.models.get(model_name)
    if pipeline is None:
        raise HTTPException(status_code=400, detail=f"Unknown model '{model_name}'. Available: {list(session.models.keys())}")

    features = payload.get("features", {})
    result = ml.predict_one(pipeline, session._numeric_cols, session._categorical_cols, features)
    result["model_used"] = model_name
    return result


# ---------------------------------------------------------------------------
# 7. Report (single JSON summary the frontend can render or export)
# ---------------------------------------------------------------------------
@app.get("/report/{session_id}")
def report(session_id: str):
    session = _get(session_id)
    _require_processed(session)
    cf = session.customer_features
    return {
        "filename": session.filename,
        "kpis": analytics.kpis(session.cleaned_df, session.schema, cf),
        "monthly_trend": analytics.monthly_trend(session.cleaned_df, session.schema),
        "top_products": analytics.top_products(session.cleaned_df, session.schema, top_n=5),
        "top_customers": analytics.top_customers(cf, top_n=5) if len(cf) else [],
        "rfm_segments": analytics.rfm_segments(cf) if len(cf) else [],
        "model_metrics": session.metrics,
        "best_model": session.best_model_name,
        "cleaning_log": session.cleaning_log,
        "data_warnings": session.warnings,
    }


def _require_processed(session: store.Session):
    if session.cleaned_df is None:
        raise HTTPException(status_code=400, detail="Call POST /process/{session_id} first.")
