# Business Sales Intelligence Dashboard

Upload any retail/sales CSV → get revenue trends, customer segmentation
(RFM), cross-sell analysis, and a repeat-purchase prediction model, in a
live web dashboard.

This is a two-service app:

```
business-sales-intelligence/
├── backend/     FastAPI — CSV parsing, cleaning, features, EDA, RFM, ML
└── frontend/    Next.js — upload UI + dashboard (deploys to Vercel)
```

Why two services instead of one: Vercel doesn't run pandas/scikit-learn
workloads well (serverless size/timeout limits), so the split is
frontend-on-Vercel + backend-on-Render — both free, both one click from
GitHub. See each folder's README for exact deploy steps.

## Quick start (local)

**Terminal 1 — backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 — frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open `http://localhost:3000`, drop in a CSV, and go.

## What it does with your CSV

1. **Auto-detects columns** — order ID, customer ID, date, quantity, unit
   price, revenue, product ID/name, country — by name and dtype heuristics.
   Works with column names like `InvoiceNo`/`Order ID`/`transaction_id`,
   `CustomerID`/`customer_id`, etc. No fixed schema required.
2. **Cleans the data** — drops duplicates and rows with no customer ID,
   fills missing product descriptions from matching product IDs, parses
   dates, separates returns/cancellations rather than deleting them, flags
   (not silently drops) extreme quantity outliers. Every decision is logged
   and shown in the UI.
3. **Engineers customer features** — TotalSpent, NumOrders, AvgBasketSize,
   Recency, Frequency, HighValueCustomer, Gold/Silver/Bronze segment.
4. **Analytics** — monthly revenue trend, revenue by country, top products
   by revenue and quantity, RFM segmentation (Champions/Loyal/At
   Risk/Lost), top customers, frequently-bought-together pairs.
5. **ML** — trains Logistic Regression, Decision Tree, and Random Forest
   to predict whether a customer will purchase again; reports accuracy,
   precision, recall, F1, ROC AUC, and Random Forest feature importance;
   picks the best model by F1.
6. **Prediction UI** — fill in a customer profile (recency, frequency,
   spend, basket size, country, segment) and get a live probability from
   the trained model.

## Deploying it publicly

1. Push this whole folder to a GitHub repo.
2. Deploy `backend/` to [Render](https://render.com) (see `backend/README.md`).
3. Deploy `frontend/` to [Vercel](https://vercel.com) (see `frontend/README.md`),
   pointing `NEXT_PUBLIC_API_URL` at your Render URL.
4. Share the Vercel URL — anyone can drop in their own CSV and use it.

## Notes on scope

The original project roadmap this was built from (`business-sales-intelligence-roadmap.md`)
specified Streamlit and the fixed "Online Retail II" schema. This build
instead:
- generalizes column detection so **any** sales CSV works, not just that
  one dataset, and
- replaces Streamlit with a Next.js + FastAPI split, since that's what
  deploys cleanly and for free on Vercel.

Data is processed **in-memory per session** (no database) — simple,
free-tier-friendly, and enough for a portfolio/demo tool. If you want
persistence across restarts or multiple concurrent heavy users, swap
`backend/app/store.py` for Redis/Postgres.
