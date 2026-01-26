# Nifty Stocks API Integration Guide

This guide shows how to add the Nifty stocks API endpoints to your existing `stock_api_service`.

## Files Added

1. `services/nifty_stocks_service.py` - Service to load and query Nifty stocks from CSV
2. `nifty_stocks_routes.py` - FastAPI routes for Nifty stocks endpoints

## Integration Steps

### Option 1: If you have a `main.py` file

Add the router to your existing FastAPI app:

```python
from fastapi import FastAPI
from nifty_stocks_routes import router as nifty_stocks_router

app = FastAPI(title="Stock API Service")

# ... your existing routes ...

# Add Nifty stocks routes
app.include_router(nifty_stocks_router)

# ... rest of your app ...
```

### Option 2: If you need to create `main.py`

Create a `main.py` file in the root of `stock_api_service`:

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

@app.get("/")
async def root():
    return {
        "message": "Stock API Service",
        "endpoints": {
            "nifty_stocks": "/api/nifty-stocks",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## API Endpoints

Once integrated, the following endpoints will be available:

### Get All Nifty Stocks
```
GET /api/nifty-stocks
```

### Get Stock by NSE Code (Query Parameter)
```
GET /api/nifty-stocks?nseCode=RELIANCE
```

### Get Stock by NSE Code (Path Parameter)
```
GET /api/nifty-stocks/RELIANCE
```

### Get Stock by ISIN
```
GET /api/nifty-stocks?isin=INE467B01029
```

### Search Stocks by Name
```
GET /api/nifty-stocks?search=Reliance
```

## Response Format

### All Stocks Response
```json
{
  "count": 50,
  "stocks": [
    {
      "stockName": "Reliance Industries Ltd",
      "nseCode": "RELIANCE",
      "isin": "INE467B01029"
    },
    ...
  ]
}
```

### Single Stock Response
```json
{
  "stockName": "Reliance Industries Ltd",
  "nseCode": "RELIANCE",
  "isin": "INE467B01029"
}
```

## CSV File Location

The service automatically looks for `data/nifty_stocks.csv` in:
1. Project root's `data` folder
2. Current directory's `data` folder

Your CSV file should have columns for:
- Stock name (column name should contain "name" or "stock")
- NSE code (column name should contain "nse", "code", or "symbol")
- ISIN (column name should contain "isin")

## Testing

After integration, test the endpoints:

```bash
# Get all stocks
curl http://localhost:8000/api/nifty-stocks

# Get by NSE code
curl http://localhost:8000/api/nifty-stocks?nseCode=RELIANCE

# Search by name
curl http://localhost:8000/api/nifty-stocks?search=Reliance
```

## Notes

- The service caches the CSV data after first load
- Use `service.clear_cache()` to reload if CSV is updated
- The CSV parser handles flexible column naming (case-insensitive)

