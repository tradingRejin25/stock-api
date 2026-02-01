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
    try:
        service = get_nifty_stocks_service()
        
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
    
    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        # Log the error for debugging
        import traceback
        print(f"❌ Error in get_nifty_stocks: {error_message}")
        print(traceback.format_exc())
        
        # Provide more helpful error message
        if "Firebase" in error_message or "Firestore" in error_message:
            raise HTTPException(
                status_code=503,
                detail=f"Nifty stocks service unavailable: Firebase Firestore is not configured. "
                       f"Please configure Firebase credentials or ensure CSV file is available. Error: {error_message}"
            )
        elif "CSV" in error_message or "not found" in error_message.lower():
            raise HTTPException(
                status_code=503,
                detail=f"Nifty stocks service unavailable: {error_message}"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error loading Nifty stocks: {error_message}"
        )


@router.get("/{nse_code}", response_model=NiftyStock)
async def get_stock_by_nse_code_path(nse_code: str):
    """Get a specific stock by NSE code (path parameter)"""
    try:
        service = get_nifty_stocks_service()
        stock = service.get_stock_by_nse_code(nse_code)
        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock not found for NSE code: {nse_code}"
            )
        return stock
    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        # Log the error for debugging
        import traceback
        print(f"❌ Error in get_stock_by_nse_code_path: {error_message}")
        print(traceback.format_exc())
        
        # Provide more helpful error message
        if "Firebase" in error_message or "Firestore" in error_message:
            raise HTTPException(
                status_code=503,
                detail=f"Nifty stocks service unavailable: Firebase Firestore is not configured. "
                       f"Please configure Firebase credentials or ensure CSV file is available. Error: {error_message}"
            )
        elif "CSV" in error_message or "not found" in error_message.lower():
            raise HTTPException(
                status_code=503,
                detail=f"Nifty stocks service unavailable: {error_message}"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error loading stock: {error_message}"
        )



