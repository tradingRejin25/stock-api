# How to deploy the Stock API (Render)

Deploy the FastAPI app so the Flutter app and other clients can call your Render URL (e.g. `https://stock-api-sdvy.onrender.com`).

---

## Deploy only API + ML (no stock_ai, no Flutter) — recommended

Use a **separate GitHub repo** that contains **only** the API service and ML code. You never push the full stock_ai project.

### 1. Create or use an “API only” repo

- Create a new repo on GitHub (e.g. `quality-stocks-api` or `stock-api`) **or** use an existing one.
- Clone it on your machine:

```powershell
cd c:\Work\Trading
git clone https://github.com/YOUR_USERNAME/quality-stocks-api.git
cd quality-stocks-api
```

(Replace with your repo URL and name.)

### 2. Copy only the API service into the repo

Copy the **contents** of `stock_api_service` into the **root** of the clone (so `main.py`, `routes/`, `ml/`, `requirements.txt`, etc. are at the **root** of the repo, not inside a subfolder).

**PowerShell** (from the folder that contains `stock_ai` and your clone):

```powershell
Copy-Item -Path "stock_ai\stock_api_service\*" -Destination "quality-stocks-api\" -Recurse -Force
cd quality-stocks-api
```

Or copy manually so the repo root has: `main.py`, `requirements.txt`, `routes/`, `ml/`, `services/`, `data/`, `render.yaml`, etc.

### 3. Commit and push (only API + ML code)

```powershell
git add -A
git status
git commit -m "Update API and ML service"
git push origin main
```

Only this repo is on GitHub; stock_ai stays local.

### 4. Connect Render to this repo

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Web Service**.
2. Select the **API-only** repo (e.g. `quality-stocks-api`).
3. **Root Directory:** leave **empty** (the repo root is already the service).
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Create the service.

### 5. Update the API after changes

Whenever you change the API or ML code in `stock_ai\stock_api_service`:

```powershell
Copy-Item -Path "c:\Work\Trading\stock_ai\stock_api_service\*" -Destination "c:\Work\Trading\quality-stocks-api\" -Recurse -Force
cd c:\Work\Trading\quality-stocks-api
git add -A
git commit -m "Update API/ML"
git push origin main
```

Render will redeploy automatically (or use Manual Deploy).

---

## Deploy from stock_ai repo with GitHub

Use the **stock_ai** repo as the source. A **render.yaml** at the repo root tells Render to use the `stock_api_service` folder.

### 1. Push your code to GitHub

From your **stock_ai** project folder:

```bash
cd c:\Work\Trading\stock_ai
git add -A
git status
git commit -m "Add Render blueprint for stock_api_service"
git push origin main
```

Ensure **render.yaml** at the **root** of stock_ai is committed (it sets `rootDir: stock_api_service`).

### 2. Connect the repo to Render

1. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Web Service**.
2. Connect your **GitHub** account if needed.
3. Select the **stock_ai** repository (the one that contains `stock_api_service` and the root `render.yaml`).
4. Render should detect the **Blueprint** from `render.yaml` and show:
   - **Root Directory:** `stock_api_service`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Choose a **name** (e.g. `quality-stocks-api`) and **region**.
6. Click **Create Web Service**.

If you already have a service and only need to switch it to the stock_ai repo:

- In the service → **Settings** → **Build & Deploy**:
  - **Repository** → change to **stock_ai** (or reconnect).
  - **Root Directory** → set to **`stock_api_service`**.
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Save; then trigger **Manual Deploy** or push to the connected branch.

### 3. (Optional) Quality stocks data

If you want `/api/quality-stocks/*` to return stocks (not just `count: 0`), add the Trendlyne Excel file. See **DEPLOY_DATA.md**.

- Put **`data/trendlyne_data.xlsx`** inside **stock_api_service** and commit, so the repo has `stock_ai/stock_api_service/data/trendlyne_data.xlsx`, **or**
- Use a Render persistent disk and set **`QUALITY_STOCKS_EXCEL_PATH`** in the service Environment to the file’s full path.

### 4. Verify

After the first deploy (or a redeploy):

- **Health:** `https://<your-service>.onrender.com/health` → `{"status":"healthy"}`.
- **Root:** `https://<your-service>.onrender.com/` → JSON with endpoints.
- **Quality stocks:** `https://<your-service>.onrender.com/api/quality-stocks/debug/info` → `excel_file_exists`, `total_stocks_loaded`.

---

## Alternative: Deploy from stock-api repo (copy from stock_ai)

If you prefer to keep using a **separate** repo (e.g. `stock-api`) for the API:

1. Clone the stock-api repo, then copy the **contents** of `stock_api_service` into the **root** of stock-api (so `main.py`, `routes/`, `requirements.txt` are at repo root).
2. In Render, point the service to the **stock-api** repo and leave **Root Directory** empty.
3. Build: `pip install -r requirements.txt`, Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`.

See the rest of this file for data and verification.

---

## Render service settings (reference)

| Setting | Value |
|--------|--------|
| **Root Directory** | `stock_api_service` when repo is stock_ai; empty when repo is stock-api with `main.py` at root. |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Python** | 3.11.7 (env var `PYTHON_VERSION=3.11.7` is set by root `render.yaml` for stock_ai). |

---

## Data file so quality-stocks return results

The health check can be OK while `/api/quality-stocks/durability-valuation/best` returns `count: 0` if the **Trendlyne Excel file** is missing. See **DEPLOY_DATA.md** for detail.

**Short version:**

- Add **`data/trendlyne_data.xlsx`** to the repo (in the same place as `main.py`, e.g. `stock-api/data/trendlyne_data.xlsx`), **or**
- Upload the file to a Render **persistent disk** and set env var **`QUALITY_STOCKS_EXCEL_PATH`** to the full path of the file (e.g. `/opt/render/project/data/trendlyne_data.xlsx`).

Without this file, quality-stocks endpoints respond with `count: 0` and an optional `message` explaining the missing data.

---

## Redeploy and verify

Push to the branch connected to Render (or use **Manual Deploy**). Then check health, root, and `/api/quality-stocks/debug/info` as in step 4 above.

---

## More detail

- **Data and env:** [DEPLOY_DATA.md](DEPLOY_DATA.md)
- **ML routes and root directory:** [docs/DEPLOY_ML.md](../docs/DEPLOY_ML.md)
- **Syncing stock_ai → stock-api repo:** [SYNC_TO_STOCK_API_REPO.md](SYNC_TO_STOCK_API_REPO.md)
