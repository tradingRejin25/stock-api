"""
API Routes for Quality Stocks Service
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.quality_stocks_service import QualityStocksService, QualityStock
from pydantic import BaseModel

router = APIRouter(prefix="/api/quality-stocks", tags=["Quality Stocks"])

# Initialize service
quality_service = QualityStocksService()


class StockResponse(BaseModel):
    """Response model for a single stock - ONLY fields that exist in CSV"""
    # Basic Information
    stockName: str
    nseCode: str
    bseCode: str
    isin: str
    
    # Core Quality Metrics
    roe: float
    roce: float
    debtToEquity: float
    interestCoverage: float
    currentRatio: float
    currentRatioTtm: float
    promoterHolding: float
    promoterHoldingChangeQoq: float
    
    # Growth Metrics
    epsTtmGrowth: float
    epsQtrYoYGrowth: float
    basicEpsQoqGrowth: float
    basicEpsTtm: float
    netProfit3YGrowth: float
    netProfit5YGrowth: float
    netProfitQoqGrowth: float
    
    # Profitability Metrics
    opmAnn: float
    opmTtm: float
    npmTtm: float
    ebitdaAnn: float
    ebitdaTtm: float
    ebitdaAnnMargin: float
    
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
    promoterPledgePercentage: float
    
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
    
    class Config:
        from_attributes = True


class QualityStocksResponse(BaseModel):
    """Response model for quality stocks list"""
    count: int
    tier: str
    stocks: List[StockResponse]


def _stock_to_response(stock: QualityStock) -> StockResponse:
    """Convert QualityStock to StockResponse - ONLY fields that exist in CSV"""
    return StockResponse(
        # Basic Information
        stockName=stock.stock_name,
        nseCode=stock.nse_code,
        bseCode=stock.bse_code,
        isin=stock.isin,
        
        # Core Quality Metrics
        roe=stock.roe,
        roce=stock.roce,
        debtToEquity=stock.debt_to_equity,
        interestCoverage=stock.interest_coverage,
        currentRatio=stock.current_ratio,
        currentRatioTtm=stock.current_ratio_ttm,
        promoterHolding=stock.promoter_holding,
        promoterHoldingChangeQoq=stock.promoter_holding_change_qoq,
        
        # Growth Metrics
        epsTtmGrowth=stock.eps_ttm_growth,
        epsQtrYoYGrowth=stock.eps_qtr_yoy_growth,
        basicEpsQoqGrowth=stock.basic_eps_qoq_growth,
        basicEpsTtm=stock.basic_eps_ttm,
        netProfit3YGrowth=stock.net_profit_3y_growth,
        netProfit5YGrowth=stock.net_profit_5y_growth,
        netProfitQoqGrowth=stock.net_profit_qoq_growth,
        
        # Profitability Metrics
        opmAnn=stock.opm_ann,
        opmTtm=stock.opm_ttm,
        npmTtm=stock.npm_ttm,
        ebitdaAnn=stock.ebitda_ann,
        ebitdaTtm=stock.ebitda_ttm,
        ebitdaAnnMargin=stock.ebitda_ann_margin,
        
        # Valuation Metrics
        pegTtm=stock.peg_ttm,
        priceToBook=stock.price_to_book,
        priceToBookAdjusted=stock.price_to_book_adjusted,
        evPerEbitdaAnn=stock.ev_per_ebitda_ann,
        priceToSalesAnn=stock.price_to_sales_ann,
        priceToSalesTtm=stock.price_to_sales_ttm,
        
        # Trendlyne Scores
        durabilityScore=stock.durability_score,
        valuationScore=stock.valuation_score,
        industryScore=stock.industry_score,
        sectorScore=stock.sector_score,
        
        # Quality Scores
        piotroskiScore=stock.piotroski_score,
        altmanZscore=stock.altman_zscore,
        
        # Promoter Metrics
        promoterPledgePercentage=stock.promoter_pledge_percentage,
        
        # Sector/Industry Metrics
        sectorRoce=stock.sector_roce,
        industryRoce=stock.industry_roce,
        sectorRoe=stock.sector_roe,
        industryRoe=stock.industry_roe,
        sectorPegTtm=stock.sector_peg_ttm,
        industryPegTtm=stock.industry_peg_ttm,
        sectorPbvTtm=stock.sector_pbv_ttm,
        industryPbvTtm=stock.industry_pbv_ttm,
        sectorNetProfitGrowthQtrQoq=stock.sector_net_profit_growth_qtr_qoq,
        sectorNetProfitGrowthAnnYoy=stock.sector_net_profit_growth_ann_yoy,
        industryNetProfitGrowthQtrQoq=stock.industry_net_profit_growth_qtr_qoq,
        industryNetProfitGrowthAnnYoy=stock.industry_net_profit_growth_ann_yoy,
        
        # SWOT Analysis
        swotStrengths=stock.swot_strengths,
        swotWeakness=stock.swot_weakness,
        swotOpportunities=stock.swot_opportunities,
        swotThreats=stock.swot_threats,
        
        # Forward Estimates
        fcEst1QForwardEbitQtr=stock.fc_est_1q_forward_ebit_qtr,
        fcEst1QFwdCashEpsQtr=stock.fc_est_1q_fwd_cash_eps_qtr,
        fcEst1QFwdInterestExpenseQtr=stock.fc_est_1q_fwd_interest_expense_qtr,
        
        # Calculated/Computed Fields
        qualityScore=stock.quality_score,
        qualityTier=stock.quality_tier,
        consecutivePositiveQuarters=stock.consecutive_positive_quarters,
        profitGrowthConsistency=stock.profit_growth_consistency,
        marginStability=stock.margin_stability,
        promoterTrend=stock.promoter_trend,
        cashFlowQuality=stock.cash_flow_quality,
        roeTrend=stock.roe_trend,
        roceConsistency=stock.roce_consistency,
    )


@router.get("/great", response_model=QualityStocksResponse)
async def get_great_quality_stocks():
    """
    Get all great quality stocks with strict criteria (no limits):
    - ROE > 12%
    - ROCE > 15%
    - Debt/Equity < 1
    - Interest Coverage > 3
    - Current Ratio > 1.2
    - Revenue Growth > 10%
    - Quality Score >= 70
    - Consistent profit growth
    - Stable/expanding margins
    """
    try:
        stocks = quality_service.filter_great_quality_stocks()
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="Great",
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching great quality stocks: {str(e)}")


@router.get("/aggressive", response_model=QualityStocksResponse)
async def get_aggressive_quality_stocks():
    """
    Get all aggressive quality stocks (higher growth potential, no limits):
    - ROE > 10%
    - ROCE > 12%
    - Debt/Equity < 1.5
    - Interest Coverage > 2
    - High growth (EPS > 15% or Revenue > 20%)
    - Quality Score >= 60
    - Consistent profit growth (not inconsistent)
    - Stable margins (not volatile)
    """
    try:
        stocks = quality_service.filter_aggressive_quality_stocks()
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="Aggressive",
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching aggressive quality stocks: {str(e)}")


@router.get("/good", response_model=QualityStocksResponse)
async def get_good_quality_stocks():
    """
    Get all good quality stocks (balanced risk-reward, no limits):
    - ROE > 8%
    - ROCE > 10%
    - Debt/Equity < 2.0
    - Interest Coverage > 1.5
    - Quality Score 55-70 (excludes great quality)
    - Consistent profit growth
    - Stable margins
    - Some positive growth indicators
    """
    try:
        stocks = quality_service.filter_medium_quality_stocks()
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="Good",
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching good quality stocks: {str(e)}")


@router.get("/all", response_model=dict)
async def get_all_quality_stocks():
    """
    Get all quality stocks categorized by tier (no limits - only quality stocks)
    Returns great, aggressive, and good quality stocks only.
    Stocks that don't meet quality thresholds are excluded.
    """
    try:
        great = quality_service.filter_great_quality_stocks()
        aggressive = quality_service.filter_aggressive_quality_stocks()
        # Pass great and aggressive to avoid duplicates
        good = quality_service.filter_medium_quality_stocks(exclude_great=great, exclude_aggressive=aggressive)
        
        return {
            "great": QualityStocksResponse(
                count=len(great),
                tier="Great",
                stocks=[_stock_to_response(stock) for stock in great]
            ).model_dump(),
            "aggressive": QualityStocksResponse(
                count=len(aggressive),
                tier="Aggressive",
                stocks=[_stock_to_response(stock) for stock in aggressive]
            ).model_dump(),
            "good": QualityStocksResponse(
                count=len(good),
                tier="Good",
                stocks=[_stock_to_response(stock) for stock in good]
            ).model_dump(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all quality stocks: {str(e)}")


@router.get("/stock/{nse_code}", response_model=StockResponse)
async def get_stock_by_nse_code(nse_code: str):
    """
    Get a specific stock by NSE code with quality analysis
    """
    try:
        stock = quality_service.get_stock_by_nse_code(nse_code)
        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock with NSE code {nse_code} not found")
        
        return _stock_to_response(stock)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock: {str(e)}")


@router.get("/durability-valuation/stats")
async def get_durability_valuation_stats():
    """
    Get statistics about durability and valuation scores in the dataset.
    Useful for understanding score distribution before filtering.
    
    Returns:
        Dictionary with statistics including min, max, avg, median, and score ranges
    """
    try:
        stats = quality_service.get_durability_valuation_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching score statistics: {str(e)}")


@router.get("/durability-valuation/best", response_model=QualityStocksResponse)
async def get_best_durability_valuation_stocks():
    """
    Get stocks with BEST durability and valuation scores.
    
    Uses high quality thresholds:
    - Durability >= 70 (above average, good durability)
    - Valuation >= 50 (above average, good valuation)
    
    These represent stocks with good durability and valuation scores.
    """
    try:
        stocks = quality_service.filter_by_durability_valuation(
            min_durability=70,  # Good durability (above average of 60.3)
            min_valuation=50    # Good valuation (above average of 38.2)
        )
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="Best Durability & Valuation (Durability>=70, Valuation>=50)",
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching best durability-valuation stocks: {str(e)}")


@router.get("/durability-valuation/excellent", response_model=QualityStocksResponse)
async def get_excellent_durability_valuation_stocks():
    """
    Get stocks with EXCELLENT durability and valuation scores (top 10%).
    
    Uses top 10% thresholds based on actual score distribution:
    - Durability >= 80 (top 10% threshold)
    - Valuation >= 53 (top 10% threshold)
    
    These represent the cream of the crop - stocks with exceptional durability and valuation.
    """
    try:
        stocks = quality_service.filter_by_durability_valuation(
            min_durability=80,  # Top 10% threshold
            min_valuation=53    # Top 10% threshold
        )
        
        return QualityStocksResponse(
            count=len(stocks),
            tier="Excellent Durability & Valuation (Durability>=80, Valuation>=53)",
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching excellent durability-valuation stocks: {str(e)}")


@router.get("/durability-valuation", response_model=QualityStocksResponse)
async def get_durability_valuation_stocks(
    min_durability: Optional[int] = Query(None, ge=0, le=100, description="Minimum durability score (0-100)"),
    max_durability: Optional[int] = Query(None, ge=0, le=100, description="Maximum durability score (0-100)"),
    min_valuation: Optional[int] = Query(None, ge=0, le=100, description="Minimum valuation score (0-100)"),
    max_valuation: Optional[int] = Query(None, ge=0, le=100, description="Maximum valuation score (0-100)")
):
    """
    Get stocks filtered by durability and valuation scores with flexible criteria.
    Supports both minimum and maximum thresholds for each score.
    
    This endpoint is useful for finding stocks with specific durability and valuation score ranges.
    No other criteria are applied - only Trendlyne Durability and Valuation scores.
    
    Examples:
    - Get best stocks (top 20%): /api/quality-stocks/durability-valuation/best
    - Get excellent stocks (top 10%): /api/quality-stocks/durability-valuation/excellent
    - Get stocks with durability >= 70 and valuation >= 50 (default):
      /api/quality-stocks/durability-valuation
    - Get stocks with custom thresholds:
      /api/quality-stocks/durability-valuation?min_durability=60&min_valuation=60
    - Get stocks with durability between 50-80:
      /api/quality-stocks/durability-valuation?min_durability=50&max_durability=80
    
    Args:
        min_durability: Minimum durability score (None = no minimum)
        max_durability: Maximum durability score (None = no maximum)
        min_valuation: Minimum valuation score (None = no minimum)
        max_valuation: Maximum valuation score (None = no maximum)
    
    Returns:
        List of stocks meeting the criteria, sorted by combined score
    """
    try:
        # If no criteria specified, use good quality defaults (above average)
        if min_durability is None and max_durability is None and min_valuation is None and max_valuation is None:
            min_durability = 70  # Above average (avg is 60.3)
            min_valuation = 50   # Above average (avg is 38.2)
        
        stocks = quality_service.filter_by_durability_valuation(
            min_durability=min_durability,
            max_durability=max_durability,
            min_valuation=min_valuation,
            max_valuation=max_valuation
        )
        
        # Build tier description
        criteria_parts = []
        if min_durability is not None:
            criteria_parts.append(f"Durability>={min_durability}")
        if max_durability is not None:
            criteria_parts.append(f"Durability<={max_durability}")
        if min_valuation is not None:
            criteria_parts.append(f"Valuation>={min_valuation}")
        if max_valuation is not None:
            criteria_parts.append(f"Valuation<={max_valuation}")
        
        tier_desc = "Durability & Valuation" + (f" ({', '.join(criteria_parts)})" if criteria_parts else " (Any)")
        
        return QualityStocksResponse(
            count=len(stocks),
            tier=tier_desc,
            stocks=[_stock_to_response(stock) for stock in stocks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching durability-valuation stocks: {str(e)}")


@router.get("/search", response_model=List[StockResponse])
async def search_stocks(
    query: str = Query(..., min_length=1, description="Search by stock name or NSE code"),
    limit: Optional[int] = Query(20, ge=1, le=100, description="Limit number of results")
):
    """
    Search stocks by name or NSE code
    """
    try:
        if not quality_service.stocks:
            quality_service.load_stocks()
        
        query_lower = query.lower()
        matching_stocks = []
        
        for stock in quality_service.stocks:
            if (query_lower in stock.stock_name.lower() or 
                query_lower in stock.nse_code.lower()):
                stock.quality_score = quality_service.calculate_quality_score(stock)
                matching_stocks.append(_stock_to_response(stock))
        
        return matching_stocks[:limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching stocks: {str(e)}")

