"""
FastAPI routes for Trendlyne Stocks API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from services.trendlyne_stocks_service import get_trendlyne_stocks_service, TrendlyneStock
from pydantic import BaseModel

router = APIRouter(prefix="/api/trendlyne-stocks", tags=["Trendlyne Stocks"])


class TrendlyneStocksResponse(BaseModel):
    """Response model for Trendlyne stocks list"""
    count: int
    stocks: List[TrendlyneStock]


class RefreshResponse(BaseModel):
    """Response model for refresh operation"""
    message: str
    files_loaded: int
    stocks_before: int
    stocks_after: int
    stocks_added: int
    total_files_processed: int


class StatisticsResponse(BaseModel):
    """Response model for statistics"""
    total_stocks: int
    loaded_files: List[str]
    total_files: int
    data_folder: str


@router.get("", response_model=TrendlyneStocksResponse)
async def get_trendlyne_stocks(
    nseCode: Optional[str] = Query(None, description="Filter by NSE code"),
    bseCode: Optional[str] = Query(None, description="Filter by BSE code"),
    isin: Optional[str] = Query(None, description="Filter by ISIN"),
    search: Optional[str] = Query(None, description="Search by stock name")
):
    """
    Get Trendlyne stocks with optional filters
    
    - **nseCode**: Get stock by NSE code (e.g., VENUSREM)
    - **bseCode**: Get stock by BSE code (e.g., 526953)
    - **isin**: Get stock by ISIN (e.g., INE411B01019)
    - **search**: Search stocks by name (case-insensitive partial match)
    
    If no filters are provided, returns all stocks.
    """
    service = get_trendlyne_stocks_service()
    
    try:
        # Filter by NSE code
        if nseCode:
            stock = service.get_stock_by_nse_code(nseCode)
            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock not found for NSE code: {nseCode}"
                )
            return TrendlyneStocksResponse(count=1, stocks=[stock])
        
        # Filter by BSE code
        if bseCode:
            stock = service.get_stock_by_bse_code(bseCode)
            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock not found for BSE code: {bseCode}"
                )
            return TrendlyneStocksResponse(count=1, stocks=[stock])
        
        # Filter by ISIN
        if isin:
            stock = service.get_stock_by_isin(isin)
            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock not found for ISIN: {isin}"
                )
            return TrendlyneStocksResponse(count=1, stocks=[stock])
        
        # Search by name
        if search:
            stocks = service.search_by_name(search)
            return TrendlyneStocksResponse(count=len(stocks), stocks=stocks)
        
        # Return all stocks
        stocks = service.get_all_stocks()
        return TrendlyneStocksResponse(count=len(stocks), stocks=stocks)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading Trendlyne stocks: {str(e)}"
        )


@router.get("/{identifier}", response_model=TrendlyneStock)
async def get_stock_by_identifier(identifier: str):
    """
    Get a specific stock by NSE code, BSE code, or ISIN (path parameter)
    The service will try to match by ISIN first, then NSE code, then BSE code
    """
    service = get_trendlyne_stocks_service()
    
    try:
        # Try ISIN first (typically starts with INE)
        if identifier.upper().startswith("INE"):
            stock = service.get_stock_by_isin(identifier)
            if stock:
                return stock
        
        # Try NSE code
        stock = service.get_stock_by_nse_code(identifier)
        if stock:
            return stock
        
        # Try BSE code
        stock = service.get_stock_by_bse_code(identifier)
        if stock:
            return stock
        
        raise HTTPException(
            status_code=404,
            detail=f"Stock not found for identifier: {identifier}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading stock: {str(e)}"
        )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_stocks():
    """
    Refresh stock data by reloading all CSV files
    This will update existing stocks and add new stocks from new files
    """
    service = get_trendlyne_stocks_service()
    
    try:
        stats = service.refresh_data()
        return RefreshResponse(
            message="Stock data refreshed successfully",
            **stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error refreshing stock data: {str(e)}"
        )


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """Get statistics about loaded stocks and files"""
    service = get_trendlyne_stocks_service()
    
    try:
        stats = service.get_statistics()
        return StatisticsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting statistics: {str(e)}"
        )











