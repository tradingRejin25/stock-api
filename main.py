"""
FastAPI Stock Information Service
Provides stock information and calculates great stocks based on configurable parameters
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import logging

from models.stock import Stock, StockFilters, GreatStockCriteria
from services.data_loader import TrendlyneDataLoader
from services.stock_analyzer import StockAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stock Information API",
    description="API service for stock information and great stocks calculation",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global data loader and analyzer
data_loader = TrendlyneDataLoader()
stock_analyzer = StockAnalyzer()

# Load data on startup
@app.on_event("startup")
async def startup_event():
    """Load Trendlyne data on application startup"""
    try:
        data_loader.load_data()
        logger.info("Stock data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading stock data: {e}")
        logger.warning("Application will start but stock data may not be available")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Stock Information API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "stocks": "/stocks",
            "stock_by_symbol": "/stocks/{symbol}",
            "stock_by_isin": "/stocks/isin/{isin}",
            "great_stocks": "/stocks/great",
            "quality_stocks": "/stocks/quality",
            "reload_data": "/reload",
            "statistics": "/stats"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "data_loaded": data_loader.is_data_loaded(),
        "stock_count": len(data_loader.get_all_stocks()) if data_loader.is_data_loaded() else 0
    }

@app.get("/stocks", response_model=List[Stock])
async def get_stocks(
    symbol: Optional[str] = Query(None, description="Filter by stock symbol"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    market_cap_min: Optional[float] = Query(None, description="Minimum market cap"),
    market_cap_max: Optional[float] = Query(None, description="Maximum market cap"),
    pe_min: Optional[float] = Query(None, description="Minimum PE ratio"),
    pe_max: Optional[float] = Query(None, description="Maximum PE ratio"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results")
):
    """
    Get list of stocks with optional filters
    """
    if not data_loader.is_data_loaded():
        raise HTTPException(status_code=503, detail="Stock data not loaded. Please reload data first.")
    
    filters = StockFilters(
        symbol=symbol,
        sector=sector,
        market_cap_min=market_cap_min,
        market_cap_max=market_cap_max,
        pe_min=pe_min,
        pe_max=pe_max
    )
    
    stocks = stock_analyzer.filter_stocks(data_loader.get_all_stocks(), filters)
    
    return stocks[:limit]

@app.get("/stocks/quality", response_model=List[Stock])
async def get_quality_stocks(
    min_trendlyne_durability: Optional[float] = Query(65, description="Minimum Trendlyne Durability Score"),
    min_trendlyne_valuation: Optional[float] = Query(60, description="Minimum Trendlyne Valuation Score"),
    min_piotroski: Optional[float] = Query(6, description="Minimum Piotroski Score (0-9)"),
    min_revenue_growth: Optional[float] = Query(10, description="Minimum Revenue Growth Annual YoY %"),
    min_profit_growth: Optional[float] = Query(12, description="Minimum Profit Growth Annual YoY %"),
    min_revenue_growth_qtr: Optional[float] = Query(8, description="Minimum Revenue Growth Qtr YoY %"),
    max_pe_vs_sector: Optional[float] = Query(1.2, description="Maximum PE vs Sector (e.g., 1.2 = 120%)"),
    max_pe_vs_industry: Optional[float] = Query(1.2, description="Maximum PE vs Industry (e.g., 1.2 = 120%)"),
    min_growth_vs_sector: Optional[float] = Query(1.1, description="Minimum Growth vs Sector (e.g., 1.1 = 110%)"),
    min_market_cap: Optional[float] = Query(None, description="Minimum market cap"),
    max_pe_ttm: Optional[float] = Query(30, description="Maximum PE TTM"),
    min_roe: Optional[float] = Query(12, description="Minimum ROE %"),
    min_score: Optional[float] = Query(70, description="Minimum overall quality score (0-100)"),
    limit: int = Query(30, ge=1, le=500, description="Maximum number of results")
):
    """
    Find great quality stocks with emphasis on:
    - Trendlyne Durability & Valuation scores (low momentum importance)
    - Piotroski Score (financial health)
    - Growth metrics (revenue & profit growth)
    - Sector/Industry comparison (outperforming peers)
    
    This endpoint uses optimized weights for quality-focused investing.
    """
    if not data_loader.is_data_loaded():
        raise HTTPException(status_code=503, detail="Stock data not loaded. Please reload data first.")
    
    try:
        # Create criteria optimized for quality stocks
        criteria = GreatStockCriteria(
            # Market cap filter
            min_market_cap=min_market_cap,
            
            # Valuation filters
            max_pe_ttm=max_pe_ttm,
            max_pe_vs_sector=max_pe_vs_sector,
            max_pe_vs_industry=max_pe_vs_industry,
            
            # Profitability filters
            min_roe=min_roe,
            min_piotroski_score=min_piotroski,
            
            # Growth filters
            min_revenue_growth=min_revenue_growth,
            min_profit_growth=min_profit_growth,
            min_revenue_growth_qtr_yoy=min_revenue_growth_qtr,
            min_revenue_growth_vs_sector=min_growth_vs_sector,
            
            # Trendlyne score filters
            min_trendlyne_durability_score=min_trendlyne_durability,
            min_trendlyne_valuation_score=min_trendlyne_valuation,
            # Low importance to momentum - set threshold lower or None
            min_trendlyne_momentum_score=None,
            
            # Score configuration for quality focus
            use_trendlyne_scores=True,
            trendlyne_weight=0.35,  # High weight for durability/valuation
            valuation_weight=0.15,  # Lower weight (Trendlyne covers this)
            profitability_weight=0.25,  # High weight (includes Piotroski)
            growth_weight=0.25,  # High weight for growth metrics
            
            # Minimum score
            min_score=min_score,
            
            # Limit and sort
            limit=limit,
            sort_by="score"
        )
        
        great_stocks = stock_analyzer.find_great_stocks(
            data_loader.get_all_stocks(),
            criteria
        )
        
        return great_stocks
    except Exception as e:
        logger.error(f"Error finding quality stocks: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding quality stocks: {str(e)}")

@app.get("/stocks/isin/{isin}", response_model=Stock)
async def get_stock_by_isin(isin: str):
    """
    Get detailed information about a specific stock by ISIN code
    """
    if not data_loader.is_data_loaded():
        raise HTTPException(status_code=503, detail="Stock data not loaded. Please reload data first.")
    
    stock = stock_analyzer.find_stock_by_isin(data_loader.get_all_stocks(), isin)
    
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock with ISIN '{isin}' not found")
    
    return stock

@app.get("/stocks/{symbol}", response_model=Stock)
async def get_stock_by_symbol(symbol: str):
    """
    Get detailed information about a specific stock by symbol (NSE Code, BSE Code, or Stock Code)
    """
    if not data_loader.is_data_loaded():
        raise HTTPException(status_code=503, detail="Stock data not loaded. Please reload data first.")
    
    stock = stock_analyzer.find_stock_by_symbol(data_loader.get_all_stocks(), symbol.upper())
    
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock with symbol '{symbol}' not found")
    
    return stock

@app.post("/stocks/great", response_model=List[Stock])
async def get_great_stocks(criteria: GreatStockCriteria):
    """
    Calculate and return great stocks based on configurable parameters
    """
    if not data_loader.is_data_loaded():
        raise HTTPException(status_code=503, detail="Stock data not loaded. Please reload data first.")
    
    try:
        great_stocks = stock_analyzer.find_great_stocks(
            data_loader.get_all_stocks(),
            criteria
        )
        
        return great_stocks
    except Exception as e:
        logger.error(f"Error calculating great stocks: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating great stocks: {str(e)}")

@app.post("/reload")
async def reload_data():
    """
    Reload stock data from Trendlyne file
    """
    try:
        data_loader.load_data()
        stock_count = len(data_loader.get_all_stocks())
        return {
            "status": "success",
            "message": "Data reloaded successfully",
            "stock_count": stock_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error reloading data: {e}")
        raise HTTPException(status_code=500, detail=f"Error reloading data: {str(e)}")

@app.get("/stats")
async def get_statistics():
    """
    Get statistics about loaded stock data
    """
    if not data_loader.is_data_loaded():
        raise HTTPException(status_code=503, detail="Stock data not loaded. Please reload data first.")
    
    stocks = data_loader.get_all_stocks()
    stats = stock_analyzer.calculate_statistics(stocks)
    
    return stats

if __name__ == "__main__":
    import uvicorn
    import os
    # Use PORT environment variable if available (for cloud hosting)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

