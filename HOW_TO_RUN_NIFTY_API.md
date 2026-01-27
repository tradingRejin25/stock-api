# How to Run Nifty Stocks API

## Prerequisites

1. **Python 3.8+ installed**
   ```powershell
   python --version
   ```

2. **Install dependencies** (if not already installed)
   ```powershell
   cd ..\stock_api_service
   pip install fastapi uvicorn pydantic
   ```

## Step 1: Ensure main.py includes Nifty Stocks routes

If you have a `main.py` file, make sure it includes the Nifty stocks router:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nifty_stocks_routes import router as nifty_stocks_router

app = FastAPI(
    title="Stock API Service",
    description="API service for stock information and Nifty stocks",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Nifty stocks routes
app.include_router(nifty_stocks_router)

# ... your existing routes ...

@app.get("/")
async def root():
    return {
        "message": "Stock API Service",
        "endpoints": {
            "nifty_stocks": "/api/nifty-stocks",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Step 2: Navigate to stock_api_service directory

```powershell
cd ..\stock_api_service
```

## Step 3: Run the API Server

### Option A: Using Python directly
```powershell
python main.py
```

### Option B: Using uvicorn (recommended)
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option C: If Python command doesn't work
```powershell
py main.py
# or
py -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 4: Verify the API is running

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 5: Test the API

### Open in Browser
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

### Test with curl

```powershell
# Get all Nifty stocks
curl http://localhost:8000/api/nifty-stocks

# Get stock by NSE code
curl http://localhost:8000/api/nifty-stocks?nseCode=RELIANCE

# Search by name
curl http://localhost:8000/api/nifty-stocks?search=Reliance

# Get by ISIN
curl http://localhost:8000/api/nifty-stocks?isin=INE467B01029
```

### Test with PowerShell (Invoke-WebRequest)

```powershell
# Get all stocks
Invoke-WebRequest -Uri "http://localhost:8000/api/nifty-stocks" | Select-Object -ExpandProperty Content

# Get by NSE code
Invoke-WebRequest -Uri "http://localhost:8000/api/nifty-stocks?nseCode=RELIANCE" | Select-Object -ExpandProperty Content
```

## Available Endpoints

Once running, these endpoints are available:

1. **GET /api/nifty-stocks** - Get all Nifty stocks
2. **GET /api/nifty-stocks?nseCode={code}** - Get stock by NSE code
3. **GET /api/nifty-stocks?isin={isin}** - Get stock by ISIN
4. **GET /api/nifty-stocks?search={query}** - Search stocks by name
5. **GET /api/nifty-stocks/{nse_code}** - Get stock by NSE code (path parameter)

## Troubleshooting

### Error: "Module not found"
```powershell
pip install fastapi uvicorn pydantic
```

### Error: "CSV file not found"
- Ensure `data/nifty_stocks.csv` exists in the `stock_api_service` directory
- The file should have columns for: Stock Name, NSE Code, ISIN

### Error: "python is not recognized"
- Use `py` instead of `python`
- Or add Python to your PATH

### Port already in use
```powershell
# Use a different port
uvicorn main:app --reload --port 8001
```

## Quick Start Script

Create a `run_nifty_api.bat` file:

```batch
@echo off
cd /d %~dp0
echo Starting Nifty Stocks API...
python main.py
pause
```

Then just double-click `run_nifty_api.bat` to start the server.



