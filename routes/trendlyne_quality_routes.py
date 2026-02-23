"""
Backward compatibility: Flutter getMediumQualityStocks calls /api/trendlyne-quality/great.
Reuses quality_stocks service and response models.
"""
from fastapi import APIRouter, HTTPException
from routes.quality_stocks_routes import (
    quality_service,
    QualityStocksResponse,
    _stock_to_response,
)

router = APIRouter(prefix="/api/trendlyne-quality", tags=["Trendlyne Quality"])


@router.get("/great", response_model=QualityStocksResponse)
async def get_trendlyne_great():
    """Same as quality-stocks/aggressive. Used by Flutter getMediumQualityStocks."""
    try:
        stocks = quality_service.filter_aggressive_quality_stocks()
        return QualityStocksResponse(
            count=len(stocks),
            tier="Great",
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
