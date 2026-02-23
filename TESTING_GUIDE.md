# Testing Guide - Quality Stocks API

## Quick Start

### Step 1: Add CSV File
Place your `filtered_stocks.csv` file in the `stock_api_service/data/` folder:
```
stock_api_service/
  └── data/
      └── filtered_stocks.csv  ← Place your file here
```

### Step 2: Run the API Server

**Option A: Using the batch script (Windows)**
```bash
cd stock_api_service
run_api.bat
```

**Option B: Manual setup**
```bash
cd stock_api_service

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Test the API

Once the server is running, you'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Open in browser:**
- API Documentation: http://localhost:8000/docs
- Root endpoint: http://localhost:8000/
- Health check: http://localhost:8000/health

**Test endpoints using curl or browser:**

1. **Great Quality Stocks**
   ```
   http://localhost:8000/api/quality-stocks/great
   ```

2. **Aggressive Quality Stocks**
   ```
   http://localhost:8000/api/quality-stocks/aggressive
   ```

3. **Good Quality Stocks**
   ```
   http://localhost:8000/api/quality-stocks/good
   ```

4. **All Quality Stocks**
   ```
   http://localhost:8000/api/quality-stocks/all
   ```

5. **Search Stocks**
   ```
   http://localhost:8000/api/quality-stocks/search?query=tata&limit=5
   ```

6. **Get Specific Stock**
   ```
   http://localhost:8000/api/quality-stocks/stock/RELIANCE
   ```

## Testing with Python

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test root endpoint
print("1. Testing root endpoint...")
response = requests.get(f"{BASE_URL}/")
print(json.dumps(response.json(), indent=2))
print()

# Test health check
print("2. Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(json.dumps(response.json(), indent=2))
print()

# Test great quality stocks
print("3. Testing great quality stocks...")
response = requests.get(f"{BASE_URL}/api/quality-stocks/great")
data = response.json()
print(f"Found {data['count']} great quality stocks")
if data['stocks']:
    print(f"First stock: {data['stocks'][0]['stockName']} ({data['stocks'][0]['nseCode']})")
    print(f"  ROE: {data['stocks'][0]['roe']}%")
    print(f"  ROCE: {data['stocks'][0]['roce']}%")
    print(f"  Quality Score: {data['stocks'][0]['qualityScore']:.2f}")
print()

# Test search
print("4. Testing search...")
response = requests.get(f"{BASE_URL}/api/quality-stocks/search?query=tata&limit=3")
data = response.json()
print(f"Found {len(data)} stocks matching 'tata'")
for stock in data:
    print(f"  - {stock['stockName']} ({stock['nseCode']})")
print()

# Test specific stock
print("5. Testing specific stock lookup...")
if data:
    nse_code = data[0]['nseCode']
    response = requests.get(f"{BASE_URL}/api/quality-stocks/stock/{nse_code}")
    if response.status_code == 200:
        stock = response.json()
        print(f"Stock: {stock['stockName']}")
        print(f"  Market Cap: {stock['marketCap']:,.0f}")
        print(f"  ROE: {stock['roe']}%")
        print(f"  ROCE: {stock['roce']}%")
        print(f"  Quality Score: {stock['qualityScore']:.2f}")
        print(f"  Quality Tier: {stock['qualityTier']}")
    else:
        print(f"Error: {response.status_code} - {response.json()}")
```

Run it:
```bash
python test_api.py
```

## Testing with PowerShell

```powershell
# Test root endpoint
Invoke-RestMethod -Uri "http://localhost:8000/" | ConvertTo-Json

# Test great quality stocks
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/quality-stocks/great"
Write-Host "Found $($response.count) great quality stocks"
$response.stocks[0] | ConvertTo-Json

# Test search
Invoke-RestMethod -Uri "http://localhost:8000/api/quality-stocks/search?query=tata&limit=3" | ConvertTo-Json
```

## Expected Response Format

### Great Quality Stocks Response:
```json
{
  "count": 25,
  "tier": "Great",
  "stocks": [
    {
      "stockName": "RELIANCE",
      "nseCode": "RELIANCE",
      "isin": "INE467B01029",
      "marketCap": 1500000.0,
      "roe": 15.5,
      "roce": 18.2,
      "debtToEquity": 0.8,
      "interestCoverage": 5.2,
      "currentRatio": 1.5,
      "qualityScore": 78.5,
      "qualityTier": "Great",
      "profitGrowthConsistency": "Consistent",
      "marginStability": "Stable",
      "promoterTrend": "Rising",
      // ... 50+ more metrics
    }
  ]
}
```

## Troubleshooting

### Issue: "No stocks loaded"
- **Solution**: Check if `filtered_stocks.csv` is in `stock_api_service/data/` folder
- Verify CSV file format matches Trendlyne export
- Check file encoding (should be UTF-8)

### Issue: "Module not found"
- **Solution**: 
  ```bash
  pip install -r requirements.txt
  ```

### Issue: "Port already in use"
- **Solution**: Change port in `run_api.bat` or command:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8001
  ```

### Issue: "CSV parsing errors"
- **Solution**: Check CSV file has all required columns
- Verify no special characters causing encoding issues
- Check CSV delimiter (should be comma)

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

1. Start the server
2. Open browser: http://localhost:8000/docs
3. You can test all endpoints directly from the browser!
4. Click "Try it out" on any endpoint
5. Execute and see the response

This is the easiest way to test the API!



