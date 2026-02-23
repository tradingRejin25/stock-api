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

## If /api/ml/* returns 404 on Render

Render is running whatever code is in the **repo and branch** you connected. Quality and trendlyne endpoints work because that code has those routers; ML returns 404 because that deployed code does **not** include the ML router or `ml/` package.

**Fix:** Deploy the version that includes ML.

- **If Render is connected to the stock_ai repo:**  
  Push the latest `stock_ai` (with `stock_api_service/main.py` that includes `ml_router`, and the `stock_api_service/ml/` folder and `routes/ml_routes.py`). Ensure `stock_api_service/requirements.txt` includes `scikit-learn` and `joblib`. Then trigger a new deploy on Render.

- **If Render is connected to a separate API repo (e.g. stock-api):**  
  Copy the **full** contents of `stock_ai/stock_api_service` into the root of that repo (overwrite `main.py`, `requirements.txt`, and add the `ml/` folder and `routes/ml_routes.py` if missing). Commit and push; Render will redeploy. The repo root must have `main.py`, `routes/` (including `ml_routes.py`), `ml/` (storage, features, predictor, train, `__init__.py`), and `requirements.txt` with `scikit-learn>=1.3.0` and `joblib>=1.3.0`.

---

## Rollback to a previous deploy (using commit hash)

When a deploy breaks the API, you can roll back using a **commit hash** from the repo Render uses.

### Option A — Render Dashboard (no git force-push)

1. Open [Render Dashboard](https://dashboard.render.com) → your **stock-api** (or API) service.
2. Go to **Manual Deploy** (top right).
3. Choose **Deploy specific commit** (or **Branch** and then you can paste a commit SHA if your UI has a commit field).
4. Enter the **commit hash** (e.g. `8364c69` or full SHA like `8364c691a1b2c3d4e5f6...`) and start the deploy.

Render will build and run that commit. Your GitHub branch is unchanged.

**Finding the commit hash:** On GitHub, open your **stock-api** repo → **Commits** and copy the hash of the last good deploy. Or in your **deploy repo** folder (the one you push to GitHub):  
`git log --oneline -15`

### Option B — Git reset in your deploy repo (then push)

Use this if you prefer to move the branch back so the “current” commit is the old one.

1. Open the repo you use for deploy (e.g. `stock-api`), **not** stock_ai:
   ```powershell
   cd c:\Work\Trading\stock-api
   ```
   (Use the path where your **stock-api** or **quality-stocks-api** clone lives.)

2. List recent commits and pick the hash to roll back **to**:
   ```powershell
   git log --oneline -15
   ```

3. Reset the branch to that commit (replace `COMMIT_HASH` with the hash, e.g. `8364c69`):
   ```powershell
   git reset --hard COMMIT_HASH
   ```

4. Force-push so Render deploys that commit:
   ```powershell
   git push --force origin main
   ```
   (Use `master` if your branch is `master`.)

Render will auto-deploy the branch; after a few minutes the service will be running the rolled-back code.

---

## More detail

- **Data and env:** [DEPLOY_DATA.md](DEPLOY_DATA.md)
- **ML routes and root directory:** [docs/DEPLOY_ML.md](../docs/DEPLOY_ML.md)
- **Syncing stock_ai → stock-api repo:** [SYNC_TO_STOCK_API_REPO.md](SYNC_TO_STOCK_API_REPO.md)
