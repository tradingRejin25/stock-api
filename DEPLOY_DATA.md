# Data requirements for deployed API (e.g. Render)

The health check (`/health` or `/`) can return OK while **quality-stocks** routes return `count: 0` and `stocks: []`. That happens when the **data file** the service reads from is missing in the deployed environment.

## Quality stocks (Trendlyne)

- **Used by:** `/api/quality-stocks/*` (e.g. `/great`, `/durability-valuation/best`, `/aggressive`, `/good`, `/all`, search, etc.)
- **Required file:** `data/trendlyne_data.xlsx` (Trendlyne export with columns such as Stock, NSE Code, ROE Ann %, ROCE Ann %, etc.)
- **Default path:** Resolved relative to the service: `stock_api_service/data/trendlyne_data.xlsx` (when running from repo root).

### Why count is 0 on Render

- The repo does **not** include `trendlyne_data.xlsx` (it’s your local/source data).
- On Render, the app starts but finds no Excel file, so it returns 0 stocks.

### How to fix it

1. **Option A – Commit the file (if allowed)**  
   - Add `stock_api_service/data/trendlyne_data.xlsx` to the repo and push.  
   - Render will deploy it and the default path will work.

2. **Option B – Environment variable (recommended if file is elsewhere)**  
   - Upload the Excel file to a **Render persistent disk** or another known path on the instance.  
   - In Render dashboard → Service → Environment, add:
     - `QUALITY_STOCKS_EXCEL_PATH` = full path to the file (e.g. `/opt/render/project/data/trendlyne_data.xlsx` if using a mounted disk).  
   - The service uses this path when set and the file exists.

3. **Option C – Build step**  
   - In Render, add a build step that downloads or copies `trendlyne_data.xlsx` into `stock_api_service/data/` (e.g. from a private URL or artifact), so the default path works.

### Verify

- **Debug endpoint:**  
  `GET https://stock-api-sdvy.onrender.com/api/quality-stocks/debug/info`  
  - Check `excel_file_exists` and `excel_path`. If the file is missing, `total_stocks_loaded` will be 0.
- **List responses:**  
  When the data file is missing, responses include an optional `message` explaining that the file was not found and pointing to the debug endpoint.

## Nifty stocks (optional)

- **Used by:** `/api/nifty-stocks`
- **Optional file:** `data/nifty_stocks.csv`  
- If the file is absent, the endpoint still returns 200 with `count: 0`, `stocks: []`.

## Summary

| Route group         | Data file                 | Env override              |
|---------------------|---------------------------|----------------------------|
| Quality stocks      | `data/trendlyne_data.xlsx`| `QUALITY_STOCKS_EXCEL_PATH`|
| Nifty stocks        | `data/nifty_stocks.csv`   | (path is fixed in code)    |

Once `trendlyne_data.xlsx` is present at the path the app uses (default or `QUALITY_STOCKS_EXCEL_PATH`), routes like `/api/quality-stocks/durability-valuation/best` will return non-zero counts when data matches the filters.
