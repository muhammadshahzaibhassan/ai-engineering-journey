"""
Module 3 & 5 — EDA + Customer Analytics.

Every function returns plain dicts/lists (JSON-serializable) sized for
direct consumption by the frontend's chart components -- no image files,
since the frontend renders its own charts (recharts).
"""
from __future__ import annotations
import pandas as pd
import numpy as np


def kpis(df: pd.DataFrame, schema: dict, customer_features: pd.DataFrame) -> dict:
    order_col = schema.get("order_id")
    cust_col = schema.get("customer_id")
    prod_col = schema.get("product_id") or schema.get("product_name")

    total_revenue = float(df["revenue"].sum()) if "revenue" in df else None
    total_orders = int(df[order_col].nunique()) if order_col else len(df)
    total_customers = int(df[cust_col].nunique()) if cust_col else None
    total_products = int(df[prod_col].nunique()) if prod_col else None
    aov = (total_revenue / total_orders) if (total_revenue and total_orders) else None
    repeat_rate = (
        float(customer_features["RepeatCustomer"].mean()) if len(customer_features) else None
    )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_products": total_products,
        "avg_order_value": aov,
        "repeat_customer_rate": repeat_rate,
        "rows_analyzed": len(df),
    }


def monthly_trend(df: pd.DataFrame, schema: dict) -> list[dict]:
    if "_month" not in df or "revenue" not in df:
        return []
    g = df.groupby("_month")["revenue"].sum().reset_index().sort_values("_month")
    return [{"month": r["_month"], "revenue": round(float(r["revenue"]), 2)} for _, r in g.iterrows()]


def revenue_by_country(df: pd.DataFrame, schema: dict, top_n: int = 10) -> list[dict]:
    country_col = schema.get("country")
    if not country_col or "revenue" not in df:
        return []
    g = df.groupby(country_col)["revenue"].sum().sort_values(ascending=False).head(top_n)
    return [{"country": str(k), "revenue": round(float(v), 2)} for k, v in g.items()]


def top_products(df: pd.DataFrame, schema: dict, top_n: int = 10) -> dict:
    prod_col = schema.get("product_name") or schema.get("product_id")
    qty_col = schema.get("quantity")
    if not prod_col:
        return {"by_revenue": [], "by_quantity": []}

    by_rev = []
    if "revenue" in df:
        g = df.groupby(prod_col)["revenue"].sum().sort_values(ascending=False).head(top_n)
        by_rev = [{"product": str(k), "revenue": round(float(v), 2)} for k, v in g.items()]

    by_qty = []
    if qty_col:
        g2 = df.groupby(prod_col)[qty_col].sum().sort_values(ascending=False).head(top_n)
        by_qty = [{"product": str(k), "quantity": float(v)} for k, v in g2.items()]

    return {"by_revenue": by_rev, "by_quantity": by_qty}


def revenue_distribution(df: pd.DataFrame, schema: dict, bins: int = 20) -> list[dict]:
    order_col = schema.get("order_id")
    if "revenue" not in df:
        return []
    series = df.groupby(order_col)["revenue"].sum() if order_col else df["revenue"]
    counts, edges = np.histogram(series.dropna(), bins=bins)
    return [
        {"bucket": f"{edges[i]:.0f}-{edges[i+1]:.0f}", "count": int(counts[i])}
        for i in range(len(counts))
    ]


def top_customers(customer_features: pd.DataFrame, top_n: int = 20) -> list[dict]:
    if not len(customer_features):
        return []
    cols = [c for c in ["CustomerID", "TotalSpent", "NumOrders", "Country", "CustomerSegment"] if c in customer_features]
    top = customer_features.sort_values("TotalSpent", ascending=False).head(top_n)[cols]
    return top.round(2).to_dict(orient="records")


def rfm_segments(customer_features: pd.DataFrame) -> list[dict]:
    """Score each customer 1-5 on R, F, M and combine into a business-readable segment."""
    if not len(customer_features):
        return []
    cf = customer_features.copy()

    def score(series, ascending):
        try:
            return pd.qcut(series.rank(method="first"), 5, labels=[1, 2, 3, 4, 5], duplicates="drop").astype(int)
        except ValueError:
            return pd.Series(3, index=series.index)

    r_score = score(cf["Recency"], ascending=True) if "Recency" in cf else 3
    r_score = 6 - r_score if isinstance(r_score, pd.Series) else r_score  # lower recency (days) = better = higher score
    f_score = score(cf["Frequency"], ascending=False) if "Frequency" in cf else 3
    m_score = score(cf["TotalSpent"], ascending=False) if "TotalSpent" in cf else 3

    cf["R"] = r_score
    cf["F"] = f_score
    cf["M"] = m_score
    rfm_sum = cf["R"].astype(int) + cf["F"].astype(int) + cf["M"].astype(int)

    def label(s):
        if s >= 13:
            return "Champions"
        if s >= 10:
            return "Loyal"
        if s >= 7:
            return "Potential Loyalist"
        if s >= 5:
            return "At Risk"
        return "Lost"

    cf["RFMSegment"] = rfm_sum.apply(label)
    counts = cf["RFMSegment"].value_counts().reset_index()
    counts.columns = ["segment", "count"]
    return counts.to_dict(orient="records")


def frequently_bought_together(df: pd.DataFrame, schema: dict, top_n_products: int = 20, top_pairs_per_product: int = 3) -> list[dict]:
    order_col = schema.get("order_id")
    prod_col = schema.get("product_name") or schema.get("product_id")
    if not order_col or not prod_col:
        return []

    # Restrict to top N products by frequency to keep this fast on large files
    top_products_list = df[prod_col].value_counts().head(top_n_products).index.tolist()
    sub = df[df[prod_col].isin(top_products_list)]

    baskets = sub.groupby(order_col)[prod_col].apply(lambda s: list(set(s)))
    from collections import Counter
    pair_counts = Counter()
    for items in baskets:
        items = sorted(items)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pair_counts[(items[i], items[j])] += 1

    product_pairs: dict[str, list] = {}
    for (a, b), cnt in pair_counts.items():
        product_pairs.setdefault(a, []).append((b, cnt))
        product_pairs.setdefault(b, []).append((a, cnt))

    results = []
    for prod in top_products_list:
        partners = sorted(product_pairs.get(prod, []), key=lambda x: -x[1])[:top_pairs_per_product]
        if partners:
            results.append({
                "product": str(prod),
                "frequently_bought_with": [{"product": str(p), "co_occurrences": c} for p, c in partners],
            })
    return results
