# Stock Information API Service

A FastAPI-based REST API service that provides stock information and calculates great stocks based on configurable parameters. Designed to work with Trendlyne data exports.

## Features

- **Stock Information Retrieval**: Get detailed information about stocks
- **Advanced Filtering**: Filter stocks by various criteria (sector, market cap, PE ratio, etc.)
- **Great Stocks Calculator**: Find investment opportunities based on configurable parameters
- **Trendlyne Integration**: Automatically loads and parses Trendlyne export files (CSV/Excel)
- **RESTful API**: Clean, well-documented API endpoints
- **CORS Enabled**: Ready for frontend integration

## Setup

### Prerequisites

**Python 3.8 or later must be installed.**

If Python is not installed:
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Restart your terminal after installation

Verify installation:
```powershell
python --version
```

### 1. Install Dependencies

**⚠️ If you get pandas build errors, use the fix script:**

```powershell
.\install_pandas_fix.ps1
```

**Option A: Using fix script (Recommended for Windows)**
```powershell
# This handles pandas installation issues automatically
.\install_pandas_fix.ps1
```

**Option B: Using standard install script**
```powershell
.\install.ps1
```

**Option C: Manual installation**
```powershell
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Install pandas using pre-built wheels (avoids build errors)
python -m pip install --only-binary :all: pandas

# Install other dependencies
python -m pip install fastapi uvicorn[standard] pydantic openpyxl python-multipart
```

If `python` doesn't work, try:
```powershell
py -m pip install -r requirements.txt
```

**See QUICK_INSTALL.md for detailed troubleshooting.**

### 2. Add Your Trendlyne Data File

Place your Trendlyne export file (CSV or Excel) in one of these locations:
- Project root directory
- `data/` subdirectory

Supported file names:
- `trendlyne_data.csv`
- `trendlyne_data.xlsx`
- `trendlyne_export.csv`
- `trendlyne_export.xlsx`
- `stock_data.csv`
- `stock_data.xlsx`

Or specify a custom path when initializing the data loader.

### 3. Run the API Server

**Option A: Using run script (Windows)**
```powershell
# Double-click run.bat or run in PowerShell:
.\run.bat
```

**Option B: Manual run**
```powershell
python main.py
```

Or using uvicorn directly:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: If you get "python is not recognized", use `py` instead of `python`, or see SETUP.md for troubleshooting.

The API will be available at `http://localhost:8000`

## API Endpoints

### Root
- **GET** `/` - API information and available endpoints

### Health Check
- **GET** `/health` - Check API health and data load status

### Get Stocks
- **GET** `/stocks` - Get list of stocks with optional filters
  - Query parameters:
    - `symbol` (optional): Filter by stock symbol
    - `sector` (optional): Filter by sector
    - `market_cap_min` (optional): Minimum market cap
    - `market_cap_max` (optional): Maximum market cap
    - `pe_min` (optional): Minimum PE ratio
    - `pe_max` (optional): Maximum PE ratio
    - `limit` (default: 100): Maximum number of results

### Get Stock by Symbol
- **GET** `/stocks/{symbol}` - Get detailed information about a specific stock by symbol (NSE Code, BSE Code, or Stock Code)

### Get Stock by ISIN
- **GET** `/stocks/isin/{isin}` - Get detailed information about a specific stock by ISIN code

### Find Great Stocks
- **POST** `/stocks/great` - Calculate and return great stocks based on criteria
  - Request body: `GreatStockCriteria` JSON object
  - Returns: List of stocks sorted by score

### Find Quality Stocks (Optimized)
- **POST** `/stocks/quality` - Find quality stocks with optimized weights for:
  - Trendlyne Durability & Valuation scores (low momentum importance)
  - Piotroski Score (financial health)
  - Growth metrics (revenue & profit growth)
  - Sector/Industry comparison (outperforming peers)
  - Query parameters for easy customization
  - Returns: List of quality stocks sorted by score

### Reload Data
- **POST** `/reload` - Reload stock data from Trendlyne file

### Statistics
- **GET** `/stats` - Get statistics about loaded stock data

## Example Usage

### Get All Stocks
```bash
curl http://localhost:8000/stocks
```

### Get Stock by Symbol
```bash
curl http://localhost:8000/stocks/RELIANCE
```

### Get Stock by ISIN
```bash
curl http://localhost:8000/stocks/isin/INE002A01018
```

### Filter Stocks
```bash
curl "http://localhost:8000/stocks?sector=Technology&pe_max=25&limit=50"
```

### Find Great Stocks
```bash
curl -X POST http://localhost:8000/stocks/great \
  -H "Content-Type: application/json" \
  -d '{
    "min_market_cap": 1000,
    "max_pe_ratio": 25,
    "min_roe": 15,
    "min_revenue_growth": 10,
    "max_debt_to_equity": 1.0,
    "min_score": 60,
    "limit": 20,
    "sort_by": "score"
  }'
```

### Find Quality Stocks (Recommended)
```bash
# Using default quality criteria
curl "http://localhost:8000/stocks/quality?limit=30"

# Customizing quality criteria
curl "http://localhost:8000/stocks/quality?min_trendlyne_durability=70&min_piotroski=7&min_revenue_growth=15&limit=20"
```

Query parameters:
- `min_trendlyne_durability` (default: 65) - Minimum Durability Score
- `min_trendlyne_valuation` (default: 60) - Minimum Valuation Score
- `min_piotroski` (default: 6) - Minimum Piotroski Score (0-9)
- `min_revenue_growth` (default: 10) - Minimum Revenue Growth Annual YoY %
- `min_profit_growth` (default: 12) - Minimum Profit Growth Annual YoY %
- `min_revenue_growth_qtr` (default: 8) - Minimum Revenue Growth Qtr YoY %
- `max_pe_vs_sector` (default: 1.2) - Max PE vs Sector (120%)
- `max_pe_vs_industry` (default: 1.2) - Max PE vs Industry (120%)
- `min_growth_vs_sector` (default: 1.1) - Min Growth vs Sector (110%)
- `min_market_cap` (optional) - Minimum market cap
- `max_pe_ttm` (default: 30) - Maximum PE TTM
- `min_roe` (default: 12) - Minimum ROE %
- `min_score` (default: 70) - Minimum overall quality score
- `limit` (default: 30) - Maximum results

## Great Stocks Criteria

The `GreatStockCriteria` model supports the following parameters:

- **Market Cap**: `min_market_cap`, `max_market_cap`
- **Valuation**: `max_pe_ratio`, `max_pb_ratio`, `max_price_to_sales`
- **Profitability**: `min_roe`, `min_roa`, `min_profit_margin`, `min_operating_margin`
- **Growth**: `min_revenue_growth`, `min_profit_growth`
- **Financial Health**: `max_debt_to_equity`, `min_current_ratio`, `min_quick_ratio`
- **Dividend**: `min_dividend_yield`
- **Price Position**: `max_price_to_52w_high` (e.g., 0.8 = 80% of 52-week high)
- **Scoring**: `min_score` (0-100), `sort_by`, `limit`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Data Format

The API expects Trendlyne export files with columns such as:
- Symbol, Name, Sector, Industry
- Market Cap, Current Price
- PE Ratio, PB Ratio, Dividend Yield
- ROE, ROA, Debt to Equity
- Current Ratio, Quick Ratio
- EPS, Book Value
- Revenue Growth, Profit Growth
- 52 Week High/Low
- And more...

The data loader automatically maps various column name variations.

## Project Structure

```
stock_api_service/
├── main.py                 # FastAPI application
├── models/
│   └── stock.py           # Stock data models
├── services/
│   ├── data_loader.py     # Trendlyne data loader
│   └── stock_analyzer.py  # Stock analysis logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── data/                 # Optional: Place data files here
```

## Notes

- The API automatically loads data on startup
- If data file is not found, the API will start but endpoints will return 503 errors
- Use `/reload` endpoint to reload data without restarting the server
- The great stocks calculator uses a weighted scoring system based on the provided criteria

