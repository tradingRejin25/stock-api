"""
Main FastAPI application for Quality Stocks API Service
"""
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from routes.quality_stocks_routes import router as quality_stocks_router
from routes.ml_routes import router as ml_router

app = FastAPI(
    title="Quality Stocks API",
    description="API service for analyzing and filtering quality stocks from Trendlyne data; ML prediction for next 10 days.",
    version="1.0.0"
)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Add X-Process-Time (seconds) header so clients can account for Render/processing delay."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{elapsed:.3f}"
        return response


# Order: ProcessTime first (outer), then CORS (inner)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(ProcessTimeMiddleware)

# Include routers
app.include_router(quality_stocks_router)
app.include_router(ml_router)


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
            "search": "/api/quality-stocks/search?query={query}",
            "ml_health": "GET /api/ml/health",
            "ml_predict": "POST /api/ml/predict (body: symbol, candles[], store_for_training, forward_days=10)",
            "ml_candles": "POST /api/ml/candles (body: symbol, candles[] with optional rsi, sma5, sma20, sma50)",
            "ml_train": "POST /api/ml/train (?auto=1 to train only when accuracy suggests)",
            "ml_insights": "GET /api/ml/insights",
        },
        "note": "Quality stocks filtered by tier. ML: 10-day prediction; send candles from Flutter; model adapts from prediction accuracy."
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

