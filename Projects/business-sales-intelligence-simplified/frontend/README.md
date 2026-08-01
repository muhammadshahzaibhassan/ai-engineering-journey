# Frontend — Signal/Desk

Next.js app (App Router, plain JS, Tailwind, recharts). Upload a sales CSV,
browse revenue/customer/product analytics, train a repeat-purchase model,
and score customers — all against the FastAPI backend in `../backend`.

## Run locally

```bash
cd frontend
npm install
cp .env.local.example .env.local   # then edit if your backend isn't on :8000
npm run dev
```

Open `http://localhost:3000`. Make sure the backend is running on
`http://localhost:8000` (see `../backend/README.md`) — or update
`NEXT_PUBLIC_API_URL` in `.env.local` to point wherever it's running.

## Deploy to Vercel

1. Deploy the backend first (see `../backend/README.md` — Render is the
   easy path) and copy its live URL.
2. Push this repo to GitHub.
3. Go to [vercel.com](https://vercel.com) → New Project → import your repo.
4. Set:
   - **Root directory:** `frontend`
   - **Framework preset:** Next.js (auto-detected)
5. Add an environment variable:
   - `NEXT_PUBLIC_API_URL` = your Render backend URL (e.g. `https://your-app.onrender.com`)
6. Deploy. Vercel gives you a public URL — that's what you share.

Every time you push to your repo's default branch, Vercel redeploys
automatically.

## Project structure

```
frontend/
├── app/
│   ├── layout.js          # root layout, wraps app in SessionProvider + Nav
│   ├── page.js             # Home — upload + KPI snapshot
│   ├── sales/page.js       # Revenue trend, country/product rankings
│   ├── customers/page.js   # RFM segments, top customers, cross-sell
│   ├── prediction/page.js  # Train models, score a customer profile
│   └── model/page.js       # Confusion matrices, feature importance, report
├── components/
│   ├── Nav.js, Panel.js, KpiTicker.js, UploadPanel.js, NoDataState.js, Shared.js
│   └── charts/              # TrendLine, RankedBar, SegmentDonut (recharts)
└── lib/
    ├── api.js               # thin fetch wrapper around the backend
    └── SessionContext.js    # shared state, persisted to localStorage
```
