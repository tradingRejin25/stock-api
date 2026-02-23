# Quick Test Instructions

## Step 1: Verify Excel File
The service uses `trendlyne_data.xlsx` which should be here:
```
stock_api_service/data/trendlyne_data.xlsx
```
(It should already be in place!)

## Step 2: Run the Server

**Easiest way - Double-click:**
```
run_api.bat
```

**Or manually:**
```powershell
cd stock_api_service
.\run_api.bat
```

The server will:
- Check for Excel file
- Create virtual environment (if needed)
- Install dependencies
- Start the API server

## Step 3: Test in Browser

Once you see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open these URLs in your browser:

1. **Interactive API Docs** (Best for testing!):
   ```
   http://localhost:8000/docs
   ```
   - Click "Try it out" on any endpoint
   - Execute and see results

2. **Great Quality Stocks**:
   ```
   http://localhost:8000/api/quality-stocks/great
   ```

3. **All Endpoints**:
   ```
   http://localhost:8000/
   ```

## Quick Test Script

If you have Python requests installed, create `quick_test.py`:

```python
import requests

BASE = "http://localhost:8000"

# Test endpoints
print("Testing API...")
print("\n1. Root:", requests.get(f"{BASE}/").json())
print("\n2. Health:", requests.get(f"{BASE}/health").json())
print("\n3. Great Quality Stocks:")
data = requests.get(f"{BASE}/api/quality-stocks/great").json()
print(f"   Found {data['count']} stocks")
if data['stocks']:
    s = data['stocks'][0]
    print(f"   Example: {s['stockName']} - Score: {s['qualityScore']:.1f}")
```

Run: `python quick_test.py`

