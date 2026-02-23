# Push API + ML from this folder (no clone)

Use **this directory** (`stock_api_service`) as the Git repo. You work and push from here; no separate clone.

---

## One-time setup

Open a terminal and go into this folder:

```powershell
cd c:\Work\Trading\stock_ai\stock_api_service
```

### 1. Make this folder a Git repo (if it isn’t already)

```powershell
git status
```

- If you see `fatal: not a git repository`: run:

```powershell
git init
git branch -M main
```

- If you already see branch/status: skip to step 2.

### 2. Add the GitHub remote

Create a **new empty repo** on GitHub (e.g. `quality-stocks-api`). Then:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/quality-stocks-api.git
```

(Replace `YOUR_USERNAME` and `quality-stocks-api` with your repo.)

If `origin` already exists and you want to change it:

```powershell
git remote set-url origin https://github.com/YOUR_USERNAME/quality-stocks-api.git
```

### 3. First push

```powershell
git add -A
git status
git commit -m "API and ML service"
git push -u origin main
```

If GitHub repo has a README/license and you get “unrelated histories”:

```powershell
git pull origin main --allow-unrelated-histories
# resolve any conflicts, then:
git push -u origin main
```

---

## Daily workflow: push after you change code

Whenever you update API or ML code **in this folder**:

```powershell
cd c:\Work\Trading\stock_ai\stock_api_service
git add -A
git status
git commit -m "Your message"
git push origin main
```

Render will redeploy from this repo if it’s connected.

---

## Render

- **New Web Service** → connect the repo you pushed to (e.g. `quality-stocks-api`).
- **Root Directory:** leave **empty** (this folder is the repo root).
- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## If the parent project (stock_ai) uses Git

After you run `git init` inside `stock_api_service`, the parent repo (stock_ai) will see this folder as a nested repo. To avoid tracking the same files in both:

- In **stock_ai**’s root, add to `.gitignore`:

```
stock_api_service/
```

Then `stock_ai` won’t push the API code; only pushes from inside `stock_api_service` will update the API repo.
