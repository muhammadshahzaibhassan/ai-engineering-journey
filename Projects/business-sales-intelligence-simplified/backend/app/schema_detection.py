"""
Auto-detects the semantic role of each column in an arbitrary sales/retail CSV.

Instead of hard-coding "InvoiceNo", "CustomerID", etc. (as the original
Online Retail II build did), we score every column against a set of
name + dtype heuristics and pick the best candidate for each role.
The result is a `schema` dict that every downstream module (cleaning,
features, analytics, ml) reads from -- so nothing else in the codebase
needs to know real column names.
"""
from __future__ import annotations
import re
import pandas as pd
from typing import Optional

ROLES = [
    "order_id", "customer_id", "date", "quantity",
    "unit_price", "revenue", "product_id", "product_name", "country",
]

# name patterns, ordered by how strongly they indicate the role
NAME_PATTERNS: dict[str, list[str]] = {
    "order_id":     [r"invoice", r"order[_ ]?id", r"order[_ ]?no", r"transaction[_ ]?id", r"receipt"],
    "customer_id":  [r"customer[_ ]?id", r"cust[_ ]?id", r"client[_ ]?id", r"user[_ ]?id", r"customer"],
    "date":         [r"invoice[_ ]?date", r"order[_ ]?date", r"transaction[_ ]?date", r"date", r"timestamp"],
    "quantity":     [r"quantity", r"qty", r"units", r"count"],
    "unit_price":   [r"unit[_ ]?price", r"price", r"cost"],
    "revenue":      [r"revenue", r"total[_ ]?amount", r"sales", r"amount", r"line[_ ]?total"],
    "product_id":   [r"stock[_ ]?code", r"product[_ ]?id", r"sku", r"item[_ ]?code"],
    "product_name": [r"description", r"product[_ ]?name", r"item[_ ]?name", r"product"],
    "country":      [r"country", r"region", r"market"],
}


def _clean_name(c: str) -> str:
    return re.sub(r"[^a-z0-9_ ]", "", c.strip().lower())


def _score_column(col: str, series: pd.Series, role: str) -> float:
    name = _clean_name(col)
    score = 0.0
    for i, pattern in enumerate(NAME_PATTERNS[role]):
        if re.search(pattern, name):
            score += (len(NAME_PATTERNS[role]) - i) * 10  # earlier pattern = stronger match
            break
    else:
        return 0.0  # no name match at all -> not a candidate

    # dtype sanity checks per role
    sample = series.dropna()
    if role == "date":
        if pd.api.types.is_datetime64_any_dtype(series):
            score += 15
        else:
            try:
                parsed = pd.to_datetime(sample.head(50), errors="coerce")
                if parsed.notna().mean() > 0.7:
                    score += 10
                else:
                    return 0.0
            except Exception:
                return 0.0
    elif role in ("quantity", "unit_price", "revenue"):
        if pd.api.types.is_numeric_dtype(series):
            score += 10
        else:
            numeric = pd.to_numeric(sample.head(50), errors="coerce")
            if numeric.notna().mean() > 0.7:
                score += 5
            else:
                return 0.0
    elif role in ("order_id", "customer_id", "product_id"):
        # ids should have reasonably repeated / bounded cardinality relative to row count
        score += 3
    return score


def detect_schema(df: pd.DataFrame) -> dict[str, Optional[str]]:
    """Return {role: column_name_or_None} for the best-guess mapping."""
    schema: dict[str, Optional[str]] = {role: None for role in ROLES}
    used_cols: set[str] = set()

    for role in ROLES:
        best_col, best_score = None, 0.0
        for col in df.columns:
            if col in used_cols:
                continue
            s = _score_column(col, df[col], role)
            if s > best_score:
                best_col, best_score = col, s
        if best_col is not None and best_score > 0:
            schema[role] = best_col
            used_cols.add(best_col)

    # If there's no explicit revenue column but we do have quantity + unit_price,
    # that's fine -- revenue will be *computed* downstream. Flag which mode we're in.
    schema["_revenue_mode"] = (
        "explicit" if schema["revenue"] else
        "computed" if (schema["quantity"] and schema["unit_price"]) else
        "unavailable"
    )
    return schema


def validate_schema(schema: dict) -> list[str]:
    """Return a list of human-readable warnings about what's missing."""
    warnings = []
    if not schema.get("customer_id"):
        warnings.append("No customer ID column detected -- customer-level analytics (RFM, segments, prediction) will be unavailable.")
    if not schema.get("date"):
        warnings.append("No date column detected -- time-trend charts will be unavailable.")
    if schema.get("_revenue_mode") == "unavailable":
        warnings.append("No revenue, or quantity+price pair, detected -- revenue-based analytics will be unavailable.")
    if not schema.get("order_id"):
        warnings.append("No order/invoice ID column detected -- order-count metrics will use row count as a fallback.")
    return warnings
