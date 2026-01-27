"""
FastAPI routes for Trendlyne Quality Stocks API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from services.trendlyne_quality_service import (
    get_trendlyne_quality_service, 
    QualityFilteredStock,
    QualityTier
)
from pydantic import BaseModel

router = APIRouter(prefix="/api/trendlyne-quality", tags=["Trendlyne Quality Stocks"])


class QualityStocksResponse(BaseModel):
    """Response model for quality stocks list"""
    count: int
    tier: str
    stocks: List[QualityFilteredStock]


class QualityStatisticsResponse(BaseModel):
    """Response model for quality statistics"""
    great_count: int
    medium_count: int
    good_count: int
    total_count: int


@router.get("", response_model=QualityStocksResponse)
async def get_quality_stocks(
    tier: Optional[str] = Query(None, description="Filter by quality tier: great, medium, or good"),
    nseCode: Optional[str] = Query(None, description="Filter by NSE code"),
    bseCode: Optional[str] = Query(None, description="Filter by BSE code"),
    isin: Optional[str] = Query(None, description="Filter by ISIN"),
    search: Optional[str] = Query(None, description="Search by stock name"),
    minScore: Optional[float] = Query(None, description="Minimum quality score")
):
    """
    Get quality-filtered Trendlyne stocks
    
    - **tier**: Filter by quality tier (great, medium, good). If not specified, returns all tiers.
    - **nseCode**: Filter by NSE code
    - **bseCode**: Filter by BSE code
    - **isin**: Filter by ISIN
    - **search**: Search stocks by name
    - **minScore**: Minimum quality score (0-100)
    """
    service = get_trendlyne_quality_service()
    
    try:
        # Determine tier filter
        quality_tier = None
        if tier:
            tier_lower = tier.lower()
            if tier_lower == "great":
                quality_tier = QualityTier.GREAT
            elif tier_lower == "medium":
                quality_tier = QualityTier.MEDIUM
            elif tier_lower == "good":
                quality_tier = QualityTier.GOOD
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid tier. Must be 'great', 'medium', or 'good'"
                )
        
        # Get stocks by tier
        stocks = service.get_all_quality_stocks(quality_tier)
        
        # Apply additional filters
        if nseCode:
            stocks = [s for s in stocks if s.nse_code and s.nse_code.upper() == nseCode.upper()]
        
        if bseCode:
            stocks = [s for s in stocks if s.bse_code and s.bse_code.upper() == bseCode.upper()]
        
        if isin:
            stocks = [s for s in stocks if s.isin and s.isin.upper() == isin.upper()]
        
        if search:
            search_lower = search.lower()
            stocks = [s for s in stocks if search_lower in s.stock.lower()]
        
        if minScore is not None:
            stocks = [s for s in stocks if s.quality_score >= minScore]
        
        # Sort by quality score descending
        stocks.sort(key=lambda x: x.quality_score, reverse=True)
        
        tier_name = tier or "all"
        return QualityStocksResponse(
            count=len(stocks),
            tier=tier_name,
            stocks=stocks
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading quality stocks: {str(e)}"
        )


@router.get("/great", response_model=QualityStocksResponse)
async def get_great_quality_stocks(
    minScore: Optional[float] = Query(None, description="Minimum quality score")
):
    """Get stocks with GREAT quality tier"""
    service = get_trendlyne_quality_service()
    
    try:
        stocks = service.filter_great_quality_stocks()
        
        if minScore is not None:
            stocks = [s for s in stocks if s.quality_score >= minScore]
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="great",
            stocks=stocks
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading great quality stocks: {str(e)}"
        )


@router.get("/medium", response_model=QualityStocksResponse)
async def get_medium_quality_stocks(
    minScore: Optional[float] = Query(None, description="Minimum quality score")
):
    """Get stocks with MEDIUM quality tier"""
    service = get_trendlyne_quality_service()
    
    try:
        stocks = service.filter_medium_quality_stocks()
        
        if minScore is not None:
            stocks = [s for s in stocks if s.quality_score >= minScore]
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="medium",
            stocks=stocks
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading medium quality stocks: {str(e)}"
        )


@router.get("/good", response_model=QualityStocksResponse)
async def get_good_quality_stocks(
    minScore: Optional[float] = Query(None, description="Minimum quality score")
):
    """Get stocks with GOOD quality tier"""
    service = get_trendlyne_quality_service()
    
    try:
        stocks = service.filter_good_quality_stocks()
        
        if minScore is not None:
            stocks = [s for s in stocks if s.quality_score >= minScore]
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="good",
            stocks=stocks
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading good quality stocks: {str(e)}"
        )


@router.get("/statistics", response_model=QualityStatisticsResponse)
async def get_quality_statistics():
    """Get statistics about quality-filtered stocks"""
    service = get_trendlyne_quality_service()
    
    try:
        great = service.filter_great_quality_stocks()
        medium = service.filter_medium_quality_stocks()
        good = service.filter_good_quality_stocks()
        
        return QualityStatisticsResponse(
            great_count=len(great),
            medium_count=len(medium),
            good_count=len(good),
            total_count=len(great) + len(medium) + len(good)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting quality statistics: {str(e)}"
        )


@router.get("/{identifier}", response_model=QualityFilteredStock)
async def get_quality_stock_by_identifier(identifier: str):
    """
    Get a specific quality stock by NSE code, BSE code, or ISIN
    Returns the stock with quality tier and score if it passes quality filters
    """
    service = get_trendlyne_quality_service()
    
    try:
        # Get all quality stocks
        all_quality_stocks = service.get_all_quality_stocks()
        
        # Try to find by identifier
        for stock in all_quality_stocks:
            if stock.isin and stock.isin.upper() == identifier.upper():
                return stock
            if stock.nse_code and stock.nse_code.upper() == identifier.upper():
                return stock
            if stock.bse_code and stock.bse_code.upper() == identifier.upper():
                return stock
        
        raise HTTPException(
            status_code=404,
            detail=f"Quality stock not found for identifier: {identifier}. "
                   f"Note: Only stocks that pass quality filters are available."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading quality stock: {str(e)}"
        )

