# Fix 404: Sync ML Code to Your stock-api Repo

The Flutter app gets **404 – Not Found** because the deployed repo (`https://github.com/tradingRejin25/stock-api`) does not include the ML routes. The server is running an older version of the API without the ML module.

## What the stock-api repo must have

For ML to work, your **stock-api** repo (the one Render deploys) must contain:

| Path | Purpose |
|------|--------|
| `main.py` | Must include `from routes.ml_routes import router as ml_router` and `app.include_router(ml_router)` |
| `routes/ml_routes.py` | ML API routes (/api/ml/predict, /candles, /train, /insights, /health) |
| `ml/__init__.py` | ML package |
| `ml/features.py` | Feature building for candles |
| `ml/predictor.py` | Prediction + model loading |
| `ml/storage.py` | Candle storage and calibration |
| `ml/train.py` | Training from stored data |
| `requirements.txt` | Must include `scikit-learn>=1.5.0` |

## Option A: Push from your local machine

If your full API code (with ML) is in `stock_ai/stock_api_service/`:

1. **Clone the stock-api repo** (if you don’t have it yet):
   ```bash
   git clone https://github.com/tradingRejin25/stock-api.git
   cd stock-api
   ```

2. **Copy everything from stock_api_service into the clone** (overwrite):
   - From your `stock_ai` project folder, copy the **contents** of `stock_api_service` into the root of `stock-api` (so `main.py`, `routes/`, `ml/`, `requirements.txt`, etc. are at the **root** of stock-api).

   On Windows (PowerShell), from the folder that contains both `stock_ai` and `stock-api`:
   ```powershell
   Copy-Item -Path "stock_ai\stock_api_service\*" -Destination "stock-api\" -Recurse -Force
   ```

   Or copy the folders/files manually so that stock-api has:
   - `main.py`
   - `requirements.txt`
   - `routes/` (with `ml_routes.py`, `quality_stocks_routes.py`, etc.)
   - `ml/` (with `__init__.py`, `features.py`, `predictor.py`, `storage.py`, `train.py`)
   - `services/`, `data/`, etc. as in stock_api_service.

3. **Commit and push**:
   ```bash
   cd stock-api
   git add .
   git status
   git commit -m "Add ML module: predict, candles, train, insights, health"
   git push origin master
   ```

4. **Redeploy on Render** (auto-deploys on push, or trigger Manual Deploy).

5. **Verify**: Open `https://<your-render-url>/` in a browser. The JSON should list `ml_predict`, `ml_candles`, `ml_train`, `ml_insights`. Then try `https://<your-render-url>/api/ml/health` – it should return `{"status":"ok",...}`.

## Option B: Check what’s in stock-api now

1. Clone and inspect:
   ```bash
   git clone https://github.com/tradingRejin25/stock-api.git
   cd stock-api
   dir
   ```

2. Check if ML is present:
   - Is there a file `routes/ml_routes.py`?
   - Does `main.py` contain the line `app.include_router(ml_router)` or `from routes.ml_routes import router as ml_router`?
   - Is there an `ml/` folder with `predictor.py`, `features.py`, `storage.py`, `train.py`?

If any of these are missing, copy them from your local `stock_ai/stock_api_service/` into the stock-api repo root (as in Option A), then commit, push, and redeploy.

## After syncing

- Backend insight in the app should show **Backend OK** when you tap **Check backend**.
- **Status 404 – Not Found (ML route missing)** will go away once the new deploy is live.
