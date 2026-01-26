"""
Main FastAPI application for Quality Stocks API Service
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.quality_stocks_routes import router as quality_stocks_router

app = FastAPI(
    title="Quality Stocks API",
    description="API service for analyzing and filtering quality stocks from Trendlyne data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quality_stocks_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Quality Stocks API Service",
        "version": "1.0.0",
        "endpoints": {
            "great_quality": "/api/quality-stocks/great",
            "aggressive_quality": "/api/quality-stocks/aggressive",
            "good_quality": "/api/quality-stocks/good",
            "all_quality": "/api/quality-stocks/all",
            "stock_by_code": "/api/quality-stocks/stock/{nse_code}",
            "search": "/api/quality-stocks/search?query={query}"
        },
        "note": "All endpoints return only quality stocks - non-significant stocks are filtered out. No limits applied."
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

