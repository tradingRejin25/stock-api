"""
FastAPI routes for Nifty Stocks API endpoints
Add these routes to your main FastAPI app
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from services.nifty_stocks_service import get_nifty_stocks_service, NiftyStock
from pydantic import BaseModel

router = APIRouter(prefix="/api/nifty-stocks", tags=["Nifty Stocks"])


class NiftyStocksResponse(BaseModel):
    """Response model for Nifty stocks list"""
    count: int
    stocks: List[NiftyStock]


@router.get("", response_model=NiftyStocksResponse)
async def get_nifty_stocks(
    nseCode: Optional[str] = Query(None, description="Filter by NSE code"),
    isin: Optional[str] = Query(None, description="Filter by ISIN"),
    search: Optional[str] = Query(None, description="Search by stock name")
):
    """
    Get Nifty stocks with optional filters
    
    - **nseCode**: Get stock by NSE code (e.g., RELIANCE)
    - **isin**: Get stock by ISIN (e.g., INE467B01029)
    - **search**: Search stocks by name (case-insensitive partial match)
    
    If no filters are provided, returns all stocks.
    """
    service = get_nifty_stocks_service()
    
    try:
        # Filter by NSE code
        if nseCode:
            stock = service.get_stock_by_nse_code(nseCode)
            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock not found for NSE code: {nseCode}"
                )
            return NiftyStocksResponse(count=1, stocks=[stock])
        
        # Filter by ISIN
        if isin:
            stock = service.get_stock_by_isin(isin)
            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock not found for ISIN: {isin}"
                )
            return NiftyStocksResponse(count=1, stocks=[stock])
        
        # Search by name
        if search:
            stocks = service.search_by_name(search)
            return NiftyStocksResponse(count=len(stocks), stocks=stocks)
        
        # Return all stocks
        stocks = service.get_all_stocks()
        return NiftyStocksResponse(count=len(stocks), stocks=stocks)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading Nifty stocks: {str(e)}"
        )


@router.get("/{nse_code}", response_model=NiftyStock)
async def get_stock_by_nse_code_path(nse_code: str):
    """Get a specific stock by NSE code (path parameter)"""
    service = get_nifty_stocks_service()
    
    try:
        stock = service.get_stock_by_nse_code(nse_code)
        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock not found for NSE code: {nse_code}"
            )
        return stock
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading stock: {str(e)}"
        )

