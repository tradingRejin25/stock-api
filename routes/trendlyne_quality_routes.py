"""
FastAPI routes for Trendlyne Quality Stocks API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from services.trendlyne_quality_service import (
    get_trendlyne_quality_service, 
    QualityFilteredStock,
    QualityTier
)
from pydantic import BaseModel

router = APIRouter(prefix="/api/trendlyne-quality", tags=["Trendlyne Quality Stocks"])


def _get_value_from_data(data: Dict[str, Any], excel_field: str, default: Any = None) -> Any:
    """Get value from data dict using Excel field name - tries exact match and variations"""
    # Try exact match first
    if excel_field in data:
        return data[excel_field]
    
    # Try without trailing spaces
    field_no_trailing = excel_field.rstrip()
    if field_no_trailing in data:
        return data[field_no_trailing]
    
    # Try with different spacing variations
    variations = [
        excel_field.replace('  ', ' '),  # Double space to single
        excel_field.strip(),  # All whitespace removed
    ]
    
    for var in variations:
        if var in data:
            return data[var]
    
    return default


def _safe_float(value: Any, default: Optional[float] = 0.0) -> Optional[float]:
    """Safely convert value to float - returns None if value is missing/invalid and default is None"""
    if value is None or value == '' or value == '-':
        return default
    try:
        if isinstance(value, str):
            value = value.replace(',', '').strip()
            # If string is empty after stripping, return default
            if not value or value.lower() in ['n/a', 'na', 'none', 'null']:
                return default
        result = float(value)
        return result
    except (ValueError, TypeError):
        return default


def _safe_int(value: Any, default: int = None) -> Optional[int]:
    """Safely convert value to int"""
    if value is None or value == '' or value == '-':
        return default
    try:
        if isinstance(value, str):
            value = value.replace(',', '').strip()
        return int(float(value))
    except (ValueError, TypeError):
        return default


class QualityFilteredStockResponse(BaseModel):
    """Response model for a quality filtered stock with mapped field names (NO Excel field names)"""
    # Basic Information
    stockName: str
    nseCode: Optional[str]
    bseCode: Optional[str]
    isin: Optional[str]
    
    # Core Quality Metrics (mapped from Excel fields)
    roe: Optional[float]
    roce: Optional[float]
    debtToEquity: Optional[float]
    interestCoverage: Optional[float]
    currentRatio: Optional[float]
    currentRatioTtm: Optional[float]
    promoterHolding: Optional[float]
    promoterHoldingChangeQoq: Optional[float]
    
    # Growth Metrics
    epsTtmGrowth: Optional[float]
    epsQtrYoYGrowth: Optional[float]
    basicEpsQoqGrowth: Optional[float]
    basicEpsTtm: Optional[float]
    netProfit3YGrowth: Optional[float]
    netProfit5YGrowth: Optional[float]
    netProfitQoqGrowth: Optional[float]
    
    # Profitability Metrics
    opmAnn: Optional[float]
    opmTtm: Optional[float]
    npmTtm: Optional[float]
    ebitdaAnn: Optional[float]
    ebitdaTtm: Optional[float]
    ebitdaAnnMargin: Optional[float]
    
    # Valuation Metrics
    pegTtm: Optional[float]
    priceToBook: Optional[float]
    priceToBookAdjusted: Optional[float]
    evPerEbitdaAnn: Optional[float]
    priceToSalesAnn: Optional[float]
    priceToSalesTtm: Optional[float]
    
    # Trendlyne Scores
    durabilityScore: Optional[int]
    valuationScore: Optional[int]
    industryScore: Optional[int]
    sectorScore: Optional[int]
    
    # Quality Scores
    piotroskiScore: Optional[int]
    altmanZscore: Optional[float]
    
    # Promoter Metrics
    promoterPledgePercentage: Optional[float]
    
    # Sector/Industry Metrics
    sectorRoce: Optional[float]
    industryRoce: Optional[float]
    sectorRoe: Optional[float]
    industryRoe: Optional[float]
    sectorPegTtm: Optional[float]
    industryPegTtm: Optional[float]
    sectorPbvTtm: Optional[float]
    industryPbvTtm: Optional[float]
    sectorNetProfitGrowthQtrQoq: Optional[float]
    sectorNetProfitGrowthAnnYoy: Optional[float]
    industryNetProfitGrowthQtrQoq: Optional[float]
    industryNetProfitGrowthAnnYoy: Optional[float]
    
    # SWOT Analysis
    swotStrengths: Optional[int]
    swotWeakness: Optional[int]
    swotOpportunities: Optional[int]
    swotThreats: Optional[int]
    
    # Forward Estimates
    fcEst1QForwardEbitQtr: Optional[float]
    fcEst1QFwdCashEpsQtr: Optional[float]
    fcEst1QFwdInterestExpenseQtr: Optional[float]
    
    # Calculated/Computed Fields (NOT from CSV - these are OK)
    qualityScore: float
    qualityTier: str
    consecutivePositiveQuarters: int
    profitGrowthConsistency: str
    marginStability: str
    promoterTrend: str
    cashFlowQuality: str
    roeTrend: str
    roceConsistency: str
    
    # Quality Metrics (from QualityFilteredStock - specific to trendlyne quality)
    qualityNotes: List[str]
    passedCriteria: Dict[str, bool]
    
    class Config:
        from_attributes = True


def _quality_stock_to_response(stock: QualityFilteredStock) -> QualityFilteredStockResponse:
    """Convert QualityFilteredStock to QualityFilteredStockResponse with mapped field names"""
    data = stock.data
    
    return QualityFilteredStockResponse(
        # Basic Information
        stockName=stock.stock,
        nseCode=stock.nse_code,
        bseCode=stock.bse_code,
        isin=stock.isin,
        
        # Core Quality Metrics (mapped from Excel field names)
        roe=_safe_float(_get_value_from_data(data, 'ROE Ann  %'), None),
        roce=_safe_float(_get_value_from_data(data, 'ROCE Ann  %'), None),
        debtToEquity=_safe_float(_get_value_from_data(data, 'Total Debt to Total Equity Ann '), None),
        interestCoverage=_safe_float(_get_value_from_data(data, 'Interest Coverage Ratio Ann '), None),
        currentRatio=_safe_float(_get_value_from_data(data, 'Current Ratio Ann '), None),
        currentRatioTtm=_safe_float(_get_value_from_data(data, 'Current Ratio TTM'), None),
        promoterHolding=_safe_float(_get_value_from_data(data, 'Promoter holding latest %'), None),
        promoterHoldingChangeQoq=_safe_float(_get_value_from_data(data, 'Promoter holding change QoQ %'), None),
        
        # Growth Metrics
        epsTtmGrowth=_safe_float(_get_value_from_data(data, 'EPS TTM Growth %')),
        epsQtrYoYGrowth=_safe_float(_get_value_from_data(data, 'EPS Qtr YoY Growth %')),
        basicEpsQoqGrowth=_safe_float(_get_value_from_data(data, 'Basic EPS QoQ Growth %')),
        basicEpsTtm=_safe_float(_get_value_from_data(data, 'Basic EPS TTM')),
        netProfit3YGrowth=_safe_float(_get_value_from_data(data, 'Net Profit 3Y Growth %')),
        netProfit5YGrowth=_safe_float(_get_value_from_data(data, 'Net Profit 5Y Growth %')),
        netProfitQoqGrowth=_safe_float(_get_value_from_data(data, 'Net Profit QoQ Growth %')),
        
        # Profitability Metrics
        opmAnn=_safe_float(_get_value_from_data(data, 'OPM Ann  %'), None),
        opmTtm=_safe_float(_get_value_from_data(data, 'OPM TTM %'), None),
        npmTtm=_safe_float(_get_value_from_data(data, 'NPM TTM %'), None),
        ebitdaAnn=_safe_float(_get_value_from_data(data, 'EBITDA Ann '), None),
        ebitdaTtm=_safe_float(_get_value_from_data(data, 'EBITDA TTM'), None),
        ebitdaAnnMargin=_safe_float(_get_value_from_data(data, 'EBITDA Ann  Margin %'), None),
        
        # Valuation Metrics
        pegTtm=_safe_float(_get_value_from_data(data, 'PEG TTM'), None),
        priceToBook=_safe_float(_get_value_from_data(data, 'Industry PBV TTM'), None),
        priceToBookAdjusted=_safe_float(_get_value_from_data(data, 'PBV Adjusted'), None),
        evPerEbitdaAnn=_safe_float(_get_value_from_data(data, 'EV Per EBITDA Ann '), None),
        priceToSalesAnn=_safe_float(_get_value_from_data(data, 'Price To Sales Ann '), None),
        priceToSalesTtm=_safe_float(_get_value_from_data(data, 'Price to Sales TTM'), None),
        
        # Trendlyne Scores
        durabilityScore=_safe_int(_get_value_from_data(data, 'Durability Score')),
        valuationScore=_safe_int(_get_value_from_data(data, 'Valuation Score')),
        industryScore=_safe_int(_get_value_from_data(data, 'Industry Score')),
        sectorScore=_safe_int(_get_value_from_data(data, 'Sector Score')),
        
        # Quality Scores
        piotroskiScore=_safe_int(_get_value_from_data(data, 'Piotroski Score')),
        altmanZscore=_safe_float(_get_value_from_data(data, 'Altman Zscore'), None),
        
        # Promoter Metrics
        promoterPledgePercentage=_safe_float(_get_value_from_data(data, 'Promoter holding pledge percentage % Qtr')),
        
        # Sector/Industry Metrics
        sectorRoce=_safe_float(_get_value_from_data(data, 'Sector ROCE'), None),
        industryRoce=_safe_float(_get_value_from_data(data, 'Industry ROCE'), None),
        sectorRoe=_safe_float(_get_value_from_data(data, 'Sector ROE'), None),
        industryRoe=_safe_float(_get_value_from_data(data, 'Industry ROE'), None),
        sectorPegTtm=_safe_float(_get_value_from_data(data, 'Sector PEG TTM'), None),
        industryPegTtm=_safe_float(_get_value_from_data(data, 'Industry PEG TTM'), None),
        sectorPbvTtm=_safe_float(_get_value_from_data(data, 'Sector PBV TTM'), None),
        industryPbvTtm=_safe_float(_get_value_from_data(data, 'Industry PBV TTM'), None),
        sectorNetProfitGrowthQtrQoq=_safe_float(_get_value_from_data(data, 'Sector Net Profit Growth Qtr QoQ %'), None),
        sectorNetProfitGrowthAnnYoy=_safe_float(_get_value_from_data(data, 'Sector Net Profit Growth Ann  YoY %'), None),
        industryNetProfitGrowthQtrQoq=_safe_float(_get_value_from_data(data, 'Industry Net Profit Growth Qtr QoQ %'), None),
        industryNetProfitGrowthAnnYoy=_safe_float(_get_value_from_data(data, 'Industry Net Profit Growth Ann  YoY %'), None),
        
        # SWOT Analysis
        swotStrengths=_safe_int(_get_value_from_data(data, 'SWOT Strengths')),
        swotWeakness=_safe_int(_get_value_from_data(data, 'SWOT Weakness')),
        swotOpportunities=_safe_int(_get_value_from_data(data, 'SWOT Opportunities')),
        swotThreats=_safe_int(_get_value_from_data(data, 'SWOT Threats')),
        
        # Forward Estimates
        fcEst1QForwardEbitQtr=_safe_float(_get_value_from_data(data, 'FC Est  1Q forward EBIT Qtr'), None),
        fcEst1QFwdCashEpsQtr=_safe_float(_get_value_from_data(data, 'FC Est  1Q fwd Cash EPS Qtr'), None),
        fcEst1QFwdInterestExpenseQtr=_safe_float(_get_value_from_data(data, 'FC Est  1Q fwd Interest Expense Qtr'), None),
        
        # Calculated/Computed Fields (set defaults since QualityFilteredStock doesn't calculate these)
        consecutivePositiveQuarters=0,  # Not calculated for QualityFilteredStock
        profitGrowthConsistency="",  # Not calculated for QualityFilteredStock
        marginStability="",  # Not calculated for QualityFilteredStock
        promoterTrend="",  # Not calculated for QualityFilteredStock
        cashFlowQuality="",  # Not calculated for QualityFilteredStock
        roeTrend="",  # Not calculated for QualityFilteredStock
        roceConsistency="",  # Not calculated for QualityFilteredStock
        
        # Quality Metrics (from QualityFilteredStock - specific to trendlyne quality)
        qualityScore=stock.quality_score,
        qualityTier=stock.quality_tier.value,
        qualityNotes=stock.quality_notes,
        passedCriteria=stock.passed_criteria,
    )


class QualityStocksResponse(BaseModel):
    """Response model for quality stocks list"""
    count: int
    tier: str
    stocks: List[QualityFilteredStockResponse]


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
            stocks=[_quality_stock_to_response(stock) for stock in stocks]
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
            stocks=[_quality_stock_to_response(stock) for stock in stocks]
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
            stocks=[_quality_stock_to_response(stock) for stock in stocks]
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
            stocks=[_quality_stock_to_response(stock) for stock in stocks]
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


@router.get("/{identifier}", response_model=QualityFilteredStockResponse)
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
                return _quality_stock_to_response(stock)
            if stock.nse_code and stock.nse_code.upper() == identifier.upper():
                return _quality_stock_to_response(stock)
            if stock.bse_code and stock.bse_code.upper() == identifier.upper():
                return _quality_stock_to_response(stock)
        
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










