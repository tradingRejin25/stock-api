"""
Main FastAPI application for Stock API Service
Includes Nifty Stocks API endpoints
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nifty_stocks_routes import router as nifty_stocks_router
from routes.trendlyne_stocks_routes import router as trendlyne_stocks_router
from routes.trendlyne_quality_routes import router as trendlyne_quality_router
from routes.quality_stocks_routes import router as quality_stocks_router

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

# Include Trendlyne stocks routes
app.include_router(trendlyne_stocks_router)

# Include Trendlyne quality stocks routes
app.include_router(trendlyne_quality_router)

# Include Quality stocks routes (new API with SWOT and sector/industry metrics)
app.include_router(quality_stocks_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Stock API Service",
        "version": "1.0.0",
        "endpoints": {
            "nifty_stocks": "/api/nifty-stocks",
            "nifty_stocks_by_nse": "/api/nifty-stocks?nseCode=RELIANCE",
            "nifty_stocks_by_isin": "/api/nifty-stocks?isin=INE467B01029",
            "nifty_stocks_search": "/api/nifty-stocks?search=Reliance",
            "trendlyne_stocks": "/api/trendlyne-stocks",
            "trendlyne_stocks_by_nse": "/api/trendlyne-stocks?nseCode=VENUSREM",
            "trendlyne_stocks_by_isin": "/api/trendlyne-stocks?isin=INE411B01019",
            "trendlyne_stocks_search": "/api/trendlyne-stocks?search=Venus",
            "trendlyne_stocks_refresh": "/api/trendlyne-stocks/refresh",
            "trendlyne_stocks_statistics": "/api/trendlyne-stocks/statistics",
            "trendlyne_quality_stocks": "/api/trendlyne-quality",
            "trendlyne_quality_great": "/api/trendlyne-quality/great",
            "trendlyne_quality_medium": "/api/trendlyne-quality/medium",
            "trendlyne_quality_good": "/api/trendlyne-quality/good",
            "trendlyne_quality_statistics": "/api/trendlyne-quality/statistics",
            "quality_stocks_great": "/api/quality-stocks/great",
            "quality_stocks_aggressive": "/api/quality-stocks/aggressive",
            "quality_stocks_good": "/api/quality-stocks/good",
            "quality_stocks_all": "/api/quality-stocks/all",
            "quality_stocks_durability_valuation": "/api/quality-stocks/durability-valuation?min_durability=60&min_valuation=60",
            "quality_stocks_durability_valuation_stats": "/api/quality-stocks/durability-valuation/stats",
            "quality_stocks_search": "/api/quality-stocks/search?query=RELIANCE",
            "quality_stocks_by_nse": "/api/quality-stocks/stock/{nse_code}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "stock-api-service"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Stock API Service...")
    print("📋 Nifty Stocks API available at: http://localhost:8000/api/nifty-stocks")
    print("📊 Trendlyne Stocks API available at: http://localhost:8000/api/trendlyne-stocks")
    print("⭐ Trendlyne Quality Stocks API available at: http://localhost:8000/api/trendlyne-quality")
    print("🎯 Quality Stocks API (with SWOT) available at: http://localhost:8000/api/quality-stocks")
    print("📚 API Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)



