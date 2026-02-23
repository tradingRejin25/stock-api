# How to Run the Quality Stocks API

## ⚠️ IMPORTANT: Excel File Required!

The service uses `trendlyne_data.xlsx` which should already be in:
```
C:\Work\Trading\stock_ai\stock_api_service\data\trendlyne_data.xlsx
```

If not found, the service will try to locate it automatically.

## Step-by-Step Instructions

### 1. Navigate to the correct directory
```powershell
cd C:\Work\Trading\stock_ai\stock_api_service
```

### 2. Check your setup
```powershell
.\check_setup.bat
```
This will tell you if the CSV file is in place.

### 3. Run the API server

**Option A: Simple version (recommended)**
```powershell
.\run_api_simple.bat
```

**Option B: Original version**
```powershell
.\run_api.bat
```

**Option C: Manual (if batch files don't work)**
```powershell
# Create virtual environment (first time only)
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

Once you see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open in browser:
- **Interactive Docs**: http://localhost:8000/docs
- **Great Quality Stocks**: http://localhost:8000/api/quality-stocks/great
- **All Endpoints**: http://localhost:8000/

## Troubleshooting

### "Excel file not found"
- Make sure `trendlyne_data.xlsx` is in `stock_api_service\data\` folder
- Check the file name is exactly `trendlyne_data.xlsx` (case-sensitive)

### "Batch file not recognized"
- Make sure you're in the correct directory: `C:\Work\Trading\stock_ai\stock_api_service`
- Try running with full path: `C:\Work\Trading\stock_ai\stock_api_service\run_api_simple.bat`

### "Python not found"
- Install Python 3.11 or later
- Make sure Python is in your PATH

### "Port already in use"
- Change port in the command: `--port 8001`
- Or close the application using port 8000

## Quick Test (After Server Starts)

In a new PowerShell window:
```powershell
# Test health
Invoke-RestMethod http://localhost:8000/health

# Test great quality stocks
Invoke-RestMethod http://localhost:8000/api/quality-stocks/great | ConvertTo-Json -Depth 3
```

