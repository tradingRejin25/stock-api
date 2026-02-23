# Routes in stock_api_service – checklist

All of these routes **exist** in `stock_ai/stock_api_service/` and are registered in `main.py`.

---

## main.py

- **Routers included:**  
  `quality_stocks_router`, `trendlyne_quality_router`, `ml_router`, `nifty_stocks_router`
- **Root:** `GET /`, `GET /health`

---

## 1. Quality stocks (`routes/quality_stocks_routes.py`)

| Method | Path | Status |
|--------|------|--------|
| GET | `/api/quality-stocks/great` | ✅ |
| GET | `/api/quality-stocks/durability-valuation/best` | ✅ |
| GET | `/api/quality-stocks/durability-valuation/excellent` | ✅ |
| GET | `/api/quality-stocks/aggressive` | ✅ |
| GET | `/api/quality-stocks/good` | ✅ |
| GET | `/api/quality-stocks/all` | ✅ |
| GET | `/api/quality-stocks/stock/{nse_code}` | ✅ |
| GET | `/api/quality-stocks/search?query=` | ✅ |
| GET | `/api/quality-stocks/debug/info` | ✅ |

---

## 2. Trendlyne quality (`routes/trendlyne_quality_routes.py`)

| Method | Path | Status |
|--------|------|--------|
| GET | `/api/trendlyne-quality/great` | ✅ |

---

## 3. Nifty stocks (`routes/nifty_stocks_routes.py`)

| Method | Path | Status |
|--------|------|--------|
| GET | `/api/nifty-stocks` (optional `?nseCode=`, `?search=`, `?isin=`) | ✅ |

---

## 4. ML (`routes/ml_routes.py`)

| Method | Path | Status |
|--------|------|--------|
| GET | `/api/ml/health` | ✅ |
| POST | `/api/ml/predict` | ✅ |
| POST | `/api/ml/candles` | ✅ |
| POST | `/api/ml/train` | ✅ |
| GET | `/api/ml/insights` | ✅ |

---

## 5. ML package (used by `ml_routes`)

| Path | Status |
|------|--------|
| `ml/__init__.py` | ✅ |
| `ml/predictor.py` | ✅ |
| `ml/features.py` | ✅ |
| `ml/storage.py` | ✅ |
| `ml/train.py` | ✅ |

---

## Summary

- **Quality stocks:** 9 routes (including durability-valuation/best, durability-valuation/excellent).
- **Trendlyne quality:** 1 route (trendlyne-quality/great).
- **Nifty stocks:** 1 route (nifty-stocks).
- **ML:** 5 routes (health, predict, candles, train, insights).

All of these are present under `stock_ai/stock_api_service/`. If Render still returns 404 for some of them, the deployed repo (stock-api) is not in sync with this folder—push the **contents** of `stock_api_service` to the **root** of the stock-api repo and redeploy.
