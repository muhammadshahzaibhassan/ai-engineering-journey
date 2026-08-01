"""
Module 6 & 7 — Machine Learning: train, evaluate, predict.

Target: RepeatCustomer (1 if a customer has more than one order, else 0).
Trains Logistic Regression, Decision Tree, and Random Forest inside a
Pipeline (ColumnTransformer -> model) so raw feature dicts can be fed
straight to `.predict_proba()` at inference time.
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix,
)

NUMERIC_FEATURES = ["Recency", "Frequency", "TotalSpent", "AvgBasketSize"]
CATEGORICAL_FEATURES_OPTIONAL = ["Country", "CustomerSegment"]
TARGET = "RepeatCustomer"


def _build_pipeline(model, numeric_cols, categorical_cols):
    transformers = []
    if numeric_cols:
        transformers.append(("num", StandardScaler(), numeric_cols))
    if categorical_cols:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols))
    pre = ColumnTransformer(transformers)
    return Pipeline([("preprocess", pre), ("model", model)])


def train_and_evaluate(customer_features: pd.DataFrame) -> dict:
    df = customer_features.copy()
    numeric_cols = [c for c in NUMERIC_FEATURES if c in df.columns]
    categorical_cols = [c for c in CATEGORICAL_FEATURES_OPTIONAL if c in df.columns]

    df = df.dropna(subset=numeric_cols + [TARGET])
    if len(df) < 20 or df[TARGET].nunique() < 2:
        return {
            "error": "Not enough data (or only one class present) to train a repeat-purchase model. "
                     "Need at least 20 customers with a mix of one-time and repeat buyers."
        }

    X = df[numeric_cols + categorical_cols]
    y = df[TARGET]

    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )

    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42),
    }

    pipelines, metrics, confusions = {}, [], {}
    for name, model in candidates.items():
        pipe = _build_pipeline(model, numeric_cols, categorical_cols)
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        try:
            probs = pipe.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, probs) if y_test.nunique() > 1 else None
        except Exception:
            auc = None

        metrics.append({
            "model": name,
            "accuracy": round(float(accuracy_score(y_test, preds)), 4),
            "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, preds, zero_division=0)), 4),
            "roc_auc": round(float(auc), 4) if auc is not None else None,
        })
        cm = confusion_matrix(y_test, preds, labels=[0, 1]).tolist()
        confusions[name] = cm
        pipelines[name] = pipe

    # Pick best model by F1 (balances precision/recall; reasonable default when
    # the relative cost of false negatives vs false positives isn't specified)
    best = max(metrics, key=lambda m: m["f1"])["model"]

    feature_importance = None
    rf_pipe = pipelines.get("Random Forest")
    if rf_pipe is not None:
        try:
            pre = rf_pipe.named_steps["preprocess"]
            names = pre.get_feature_names_out()
            importances = rf_pipe.named_steps["model"].feature_importances_
            fi = sorted(zip(names, importances), key=lambda x: -x[1])[:15]
            feature_importance = [{"feature": n, "importance": round(float(v), 4)} for n, v in fi]
        except Exception:
            feature_importance = None

    return {
        "pipelines": pipelines,
        "metrics": metrics,
        "confusion_matrices": confusions,
        "best_model_name": best,
        "feature_importance": feature_importance,
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "class_balance": {str(k): int(v) for k, v in y.value_counts().items()},
        "train_size": len(X_train),
        "test_size": len(X_test),
    }


def predict_one(pipeline, numeric_cols, categorical_cols, payload: dict) -> dict:
    row = {}
    for c in numeric_cols:
        row[c] = float(payload.get(c, 0) or 0)
    for c in categorical_cols:
        row[c] = payload.get(c, "Unknown")
    X = pd.DataFrame([row])
    pred = int(pipeline.predict(X)[0])
    try:
        prob = float(pipeline.predict_proba(X)[0, 1])
    except Exception:
        prob = None
    return {"repeat_customer_prediction": bool(pred), "probability": prob}
