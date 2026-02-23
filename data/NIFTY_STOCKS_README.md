# Replacing the Nifty stocks CSV with the actual list

The API reads from **`data/nifty_stocks.csv`**. To use the real Nifty 50 (or Nifty 500) list, replace the file while keeping the format below.

---

## Required CSV format

- **Header row** with at least:
  - One column whose name contains **"name"** or **"stock"** (company name), e.g. `stock_name`, `Stock Name`, `Company`
  - One column whose name contains **"nse"**, **"code"**, or **"symbol"** (NSE symbol), e.g. `nse_code`, `NSE Code`, `Symbol`
- **Optional:** a column whose name contains **"isin"** (ISIN), e.g. `isin`, `ISIN`
- **Encoding:** UTF-8
- **Delimiter:** comma (`,`)

Example (minimal):

```csv
stock_name,nse_code,isin
Reliance Industries Limited,NSE_EQ|INE002A01018,INE002A01018
TCS Limited,NSE_EQ|INE467B01029,INE467B01029
```

Column names are matched **case-insensitively**, so `Stock Name`, `NSE Code`, `ISIN` work too.

---

## Where to get the actual list

1. **NSE**
   - [NSE Indices – Nifty 50](https://www.nseindia.com/market-data/live-equity-market) → select the index → list of constituents (name, symbol, ISIN). Export or copy into Excel/CSV and save with the column names above.

2. **NSE bhav copy / reports**
   - NSE provides equity bhav copy and other reports that include symbol/name. You can take the list of Nifty 50 symbols from the index constituent list and match with names/ISIN from the bhav or another report, then build a CSV with `stock_name`, `nse_code`, `isin`.

3. **Your broker / screener**
   - Export “Nifty 50” or “Nifty 500” from your broker app or a site like Moneycontrol/Screener. If the export has different column names (e.g. “Company Name”, “Symbol”), **rename** them so one column has “name” or “stock” and one has “nse”/“code”/“symbol”, and optionally “isin”.

4. **Manual / Excel**
   - Create a CSV in Excel (or a text editor) with columns `stock_name`, `nse_code`, `isin` and paste the full Nifty 50 (or 500) list. Save as **CSV UTF-8** and name the file `nifty_stocks.csv`.

---

## Steps to replace the dummy file

1. Get or build the CSV with the required columns (name, nse code, isin optional).
2. Save it as **`nifty_stocks.csv`** (UTF-8, comma-separated).
3. Replace the existing file:
   - **Local:** overwrite `stock_api_service/data/nifty_stocks.csv` with your new file.
   - **Repo:**  
     `git add data/nifty_stocks.csv`  
     `git commit -m "Replace with actual Nifty list"`  
     `git push origin main`  
   (from the repo that deploys to Render.)
4. Redeploy on Render (or let auto-deploy run).  
   Then `GET /api/nifty-stocks` will return the new list.

---

## NSE symbol format

The app often uses symbols like `NSE_EQ|INE002A01018`. Your CSV can use:

- That full form in the nse/code/symbol column, or  
- Just the NSE trading symbol (e.g. `RELIANCE`, `TCS`) if your data source has only that.

If the Flutter app or breadth logic expects `NSE_EQ|ISIN`, ensure your `nse_code` column matches what the app uses (you can keep the dummy file’s format for a few rows and then fill the rest the same way).
