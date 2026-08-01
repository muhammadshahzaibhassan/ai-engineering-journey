# Backend — Business Sales Intelligence API

FastAPI service that does all the heavy lifting: CSV schema auto-detection,
cleaning, feature engineering, EDA, RFM segmentation, market-basket analysis,
and repeat-purchase ML (Logistic Regression / Decision Tree / Random Forest).

Nothing about it is tied to one dataset's column names — it inspects whatever
CSV you upload and works out what each column means.

## Run locally

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive Swagger docs of every endpoint.

## API summary

| Method | Path | Purpose |
|---|---|---|
| POST | `/upload` | Upload a CSV, get back the detected schema + preview |
| POST | `/process/{session_id}` | Clean data + build customer features |
| GET | `/analytics/sales/{session_id}` | KPIs, monthly trend, country/product rankings |
| GET | `/analytics/customers/{session_id}` | Top customers, RFM segments, cross-sell pairs |
| POST | `/model/train/{session_id}` | Train & evaluate 3 classifiers |
| POST | `/model/predict/{session_id}` | Score a customer profile |
| GET | `/report/{session_id}` | Single JSON summary of everything above |

Sessions are **in-memory** (a Python dict, TTL 6 hours) — there's no database.
That's a deliberate simplicity trade-off for a demo/portfolio project; if you
outgrow it, swap `app/store.py` for Redis or Postgres without touching any
other module.

## Deploy to Render (free tier, easiest path)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → New → Web Service → connect your repo.
3. Set:
   - **Root directory:** `backend`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy. Render gives you a URL like `https://your-app.onrender.com`.
5. Copy that URL into the frontend's `NEXT_PUBLIC_API_URL` env var (see
   `../frontend/README.md`).

Free-tier Render services sleep after inactivity — the first request after
a while will be slow (~30s cold start). Fine for a demo; upgrade the plan
if you need it always-warm.

### CORS

`main.py` currently allows all origins (`allow_origins=["*"]`) so the demo
works immediately. Once you know your Vercel URL, tighten this in
`main.py`'s `CORSMiddleware` to just that origin.
