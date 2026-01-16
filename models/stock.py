"""
Stock data models
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Stock(BaseModel):
    """Stock information model"""
    symbol: str = Field(..., description="Stock symbol")
    isin: Optional[str] = Field(None, description="ISIN code")
    name: Optional[str] = Field(None, description="Company name")
    sector: Optional[str] = Field(None, description="Sector")
    industry: Optional[str] = Field(None, description="Industry")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    current_price: Optional[float] = Field(None, description="Current price")
    pe_ratio: Optional[float] = Field(None, description="Price to Earnings ratio")
    pb_ratio: Optional[float] = Field(None, description="Price to Book ratio")
    dividend_yield: Optional[float] = Field(None, description="Dividend yield (%)")
    roe: Optional[float] = Field(None, description="Return on Equity (%)")
    roa: Optional[float] = Field(None, description="Return on Assets (%)")
    debt_to_equity: Optional[float] = Field(None, description="Debt to Equity ratio")
    current_ratio: Optional[float] = Field(None, description="Current ratio")
    quick_ratio: Optional[float] = Field(None, description="Quick ratio")
    eps: Optional[float] = Field(None, description="Earnings per Share")
    book_value: Optional[float] = Field(None, description="Book value per share")
    face_value: Optional[float] = Field(None, description="Face value")
    price_to_sales: Optional[float] = Field(None, description="Price to Sales ratio")
    ev_to_ebitda: Optional[float] = Field(None, description="EV to EBITDA ratio")
    profit_margin: Optional[float] = Field(None, description="Profit margin (%)")
    operating_margin: Optional[float] = Field(None, description="Operating margin (%)")
    revenue_growth: Optional[float] = Field(None, description="Revenue growth (%)")
    profit_growth: Optional[float] = Field(None, description="Profit growth (%)")
    fii_holding: Optional[float] = Field(None, description="FII holding (%)")
    dii_holding: Optional[float] = Field(None, description="DII holding (%)")
    promoter_holding: Optional[float] = Field(None, description="Promoter holding (%)")
    public_holding: Optional[float] = Field(None, description="Public holding (%)")
    week_52_high: Optional[float] = Field(None, alias="52_week_high", description="52 week high")
    week_52_low: Optional[float] = Field(None, alias="52_week_low", description="52 week low")
    
    # Trendlyne Scores
    trendlyne_durability_score: Optional[float] = Field(None, description="Trendlyne Durability Score")
    trendlyne_valuation_score: Optional[float] = Field(None, description="Trendlyne Valuation Score")
    trendlyne_momentum_score: Optional[float] = Field(None, description="Trendlyne Momentum Score")
    dvm_classification: Optional[str] = Field(None, description="DVM Classification Text")
    prev_day_durability_score: Optional[float] = Field(None, description="Previous Day Durability Score")
    prev_day_valuation_score: Optional[float] = Field(None, description="Previous Day Valuation Score")
    prev_day_momentum_score: Optional[float] = Field(None, description="Previous Day Momentum Score")
    prev_week_durability_score: Optional[float] = Field(None, description="Previous Week Durability Score")
    prev_week_valuation_score: Optional[float] = Field(None, description="Previous Week Valuation Score")
    prev_week_momentum_score: Optional[float] = Field(None, description="Previous Week Momentum Score")
    prev_month_durability_score: Optional[float] = Field(None, description="Previous Month Durability Score")
    prev_month_valuation_score: Optional[float] = Field(None, description="Previous Month Valuation Score")
    prev_month_momentum_score: Optional[float] = Field(None, description="Previous Month Momentum Score")
    normalized_momentum_score: Optional[float] = Field(None, description="Normalized Momentum Score")
    
    # Quarterly Financials
    operating_revenue_qtr: Optional[float] = Field(None, description="Operating Revenue (Quarterly)")
    net_profit_qtr: Optional[float] = Field(None, description="Net Profit (Quarterly)")
    revenue_qoq_growth: Optional[float] = Field(None, description="Revenue QoQ Growth %")
    revenue_growth_qtr_yoy: Optional[float] = Field(None, description="Revenue Growth Qtr YoY %")
    net_profit_qtr_growth_yoy: Optional[float] = Field(None, description="Net Profit Qtr Growth YoY %")
    net_profit_qoq_growth: Optional[float] = Field(None, description="Net Profit QoQ Growth %")
    operating_profit_margin_qtr: Optional[float] = Field(None, description="Operating Profit Margin Qtr %")
    operating_profit_margin_qtr_4q_ago: Optional[float] = Field(None, description="Operating Profit Margin Qtr 4Qtr ago %")
    
    # TTM (Trailing Twelve Months) Financials
    operating_revenue_ttm: Optional[float] = Field(None, description="Operating Revenue TTM")
    net_profit_ttm: Optional[float] = Field(None, description="Net Profit TTM")
    
    # Annual Financials
    operating_revenue_annual: Optional[float] = Field(None, description="Operating Revenue Annual")
    net_profit_annual: Optional[float] = Field(None, description="Net Profit Annual")
    revenue_growth_annual_yoy: Optional[float] = Field(None, description="Revenue Growth Annual YoY %")
    net_profit_annual_yoy_growth: Optional[float] = Field(None, description="Net Profit Annual YoY Growth %")
    
    # Cash Flow
    cash_from_financing_annual: Optional[float] = Field(None, description="Cash from Financing Annual Activity")
    cash_from_investing_annual: Optional[float] = Field(None, description="Cash from Investing Activity Annual")
    cash_from_operating_annual: Optional[float] = Field(None, description="Cash from Operating Activity Annual")
    net_cash_flow_annual: Optional[float] = Field(None, description="Net Cash Flow Annual")
    
    # Sector Comparisons
    sector_revenue_growth_qtr_yoy: Optional[float] = Field(None, description="Sector Revenue Growth Qtr YoY %")
    sector_net_profit_growth_qtr_yoy: Optional[float] = Field(None, description="Sector Net Profit Growth Qtr YoY %")
    sector_revenue_growth_qtr_qoq: Optional[float] = Field(None, description="Sector Revenue Growth Qtr QoQ %")
    sector_net_profit_growth_qtr_qoq: Optional[float] = Field(None, description="Sector Net Profit Growth Qtr QoQ %")
    sector_revenue_growth_annual_yoy: Optional[float] = Field(None, description="Sector Revenue Growth Annual YoY %")
    sector_pe_ttm: Optional[float] = Field(None, description="Sector PE TTM")
    sector_peg_ttm: Optional[float] = Field(None, description="Sector PEG TTM")
    sector_price_to_book_ttm: Optional[float] = Field(None, description="Sector Price to Book TTM")
    sector_roe: Optional[float] = Field(None, description="Sector Return on Equity ROE")
    sector_roa: Optional[float] = Field(None, description="Sector Return on Assets")
    
    # Industry Comparisons
    industry_pe_ttm: Optional[float] = Field(None, description="Industry PE TTM")
    industry_peg_ttm: Optional[float] = Field(None, description="Industry PEG TTM")
    industry_price_to_book_ttm: Optional[float] = Field(None, description="Industry Price to Book TTM")
    industry_roe: Optional[float] = Field(None, description="Industry Return on Equity ROE")
    industry_roa: Optional[float] = Field(None, description="Industry Return on Assets")
    
    # PE Ratios (Multiple)
    pe_ttm: Optional[float] = Field(None, description="PE TTM Price to Earnings")
    forecaster_pe_1y_forward: Optional[float] = Field(None, description="Forecaster Estimates 1Y forward PE")
    pe_3yr_avg: Optional[float] = Field(None, description="PE 3Yr Average")
    pe_5yr_avg: Optional[float] = Field(None, description="PE 5Yr Average")
    pct_days_below_current_pe: Optional[float] = Field(None, description="%Days traded below current PE Price to Earnings")
    
    # PEG Ratios
    peg_ttm: Optional[float] = Field(None, description="PEG TTM PE to Growth")
    forecaster_peg_1y_forward: Optional[float] = Field(None, description="Forecaster Estimates 1Y forward PEG")
    
    # Price to Book
    pct_days_below_current_pb: Optional[float] = Field(None, description="%Days traded below current Price to Book Value")
    
    # EPS
    eps_ttm_growth: Optional[float] = Field(None, description="EPS TTM Growth %")
    
    # Piotroski Score
    piotroski_score: Optional[float] = Field(None, description="Piotroski Score")
    
    # Financial Results
    latest_financial_result: Optional[str] = Field(None, description="Latest financial result")
    result_announced_date: Optional[str] = Field(None, description="Result Announced Date")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class StockFilters(BaseModel):
    """Filters for stock queries"""
    symbol: Optional[str] = None
    sector: Optional[str] = None
    market_cap_min: Optional[float] = None
    market_cap_max: Optional[float] = None
    pe_min: Optional[float] = None
    pe_max: Optional[float] = None
    pb_min: Optional[float] = None
    pb_max: Optional[float] = None
    roe_min: Optional[float] = None
    roe_max: Optional[float] = None
    dividend_yield_min: Optional[float] = None
    dividend_yield_max: Optional[float] = None

class GreatStockCriteria(BaseModel):
    """Criteria for identifying great stocks"""
    # Market cap filters
    min_market_cap: Optional[float] = Field(None, description="Minimum market cap")
    max_market_cap: Optional[float] = Field(None, description="Maximum market cap")
    
    # Valuation filters
    max_pe_ratio: Optional[float] = Field(None, description="Maximum PE ratio")
    max_pb_ratio: Optional[float] = Field(None, description="Maximum PB ratio")
    max_price_to_sales: Optional[float] = Field(None, description="Maximum Price to Sales ratio")
    max_pe_ttm: Optional[float] = Field(None, description="Maximum PE TTM")
    max_peg_ttm: Optional[float] = Field(None, description="Maximum PEG TTM")
    
    # Profitability filters
    min_roe: Optional[float] = Field(None, description="Minimum ROE (%)")
    min_roa: Optional[float] = Field(None, description="Minimum ROA (%)")
    min_profit_margin: Optional[float] = Field(None, description="Minimum profit margin (%)")
    min_operating_margin: Optional[float] = Field(None, description="Minimum operating margin (%)")
    min_operating_profit_margin_qtr: Optional[float] = Field(None, description="Minimum Operating Profit Margin Qtr %")
    
    # Growth filters
    min_revenue_growth: Optional[float] = Field(None, description="Minimum revenue growth Annual YoY (%)")
    min_profit_growth: Optional[float] = Field(None, description="Minimum profit growth Annual YoY (%)")
    min_revenue_growth_qtr_yoy: Optional[float] = Field(None, description="Minimum Revenue Growth Qtr YoY %")
    min_net_profit_qtr_growth_yoy: Optional[float] = Field(None, description="Minimum Net Profit Qtr Growth YoY %")
    min_revenue_qoq_growth: Optional[float] = Field(None, description="Minimum Revenue QoQ Growth %")
    min_net_profit_qoq_growth: Optional[float] = Field(None, description="Minimum Net Profit QoQ Growth %")
    min_eps_ttm_growth: Optional[float] = Field(None, description="Minimum EPS TTM Growth %")
    
    # Financial health filters
    max_debt_to_equity: Optional[float] = Field(None, description="Maximum debt to equity ratio")
    min_current_ratio: Optional[float] = Field(None, description="Minimum current ratio")
    min_quick_ratio: Optional[float] = Field(None, description="Minimum quick ratio")
    min_piotroski_score: Optional[float] = Field(None, description="Minimum Piotroski Score (0-9)")
    
    # Cash flow filters
    min_cash_from_operating_annual: Optional[float] = Field(None, description="Minimum Cash from Operating Activity Annual")
    min_net_cash_flow_annual: Optional[float] = Field(None, description="Minimum Net Cash Flow Annual")
    
    # Trendlyne Score filters
    min_trendlyne_durability_score: Optional[float] = Field(None, description="Minimum Trendlyne Durability Score")
    min_trendlyne_valuation_score: Optional[float] = Field(None, description="Minimum Trendlyne Valuation Score")
    min_trendlyne_momentum_score: Optional[float] = Field(None, description="Minimum Trendlyne Momentum Score")
    min_normalized_momentum_score: Optional[float] = Field(None, description="Minimum Normalized Momentum Score")
    
    # Sector/Industry comparison filters
    max_pe_vs_sector: Optional[float] = Field(None, description="Maximum PE ratio vs Sector (e.g., 1.2 = 120% of sector PE)")
    max_pe_vs_industry: Optional[float] = Field(None, description="Maximum PE ratio vs Industry (e.g., 1.2 = 120% of industry PE)")
    min_revenue_growth_vs_sector: Optional[float] = Field(None, description="Minimum Revenue Growth vs Sector (e.g., 1.1 = 110% of sector growth)")
    min_profit_growth_vs_sector: Optional[float] = Field(None, description="Minimum Profit Growth vs Sector (e.g., 1.1 = 110% of sector growth)")
    
    # Dividend filters
    min_dividend_yield: Optional[float] = Field(None, description="Minimum dividend yield (%)")
    
    # Price position filters
    max_price_to_52w_high: Optional[float] = Field(None, description="Maximum price as % of 52 week high (e.g., 0.8 = 80%)")
    max_pct_days_below_pe: Optional[float] = Field(None, description="Maximum %Days traded below current PE (higher = better value)")
    max_pct_days_below_pb: Optional[float] = Field(None, description="Maximum %Days traded below current PB (higher = better value)")
    
    # Score weights (for custom scoring)
    use_trendlyne_scores: bool = Field(True, description="Include Trendlyne scores in overall score calculation")
    trendlyne_weight: float = Field(0.3, ge=0, le=1, description="Weight for Trendlyne scores (0-1)")
    valuation_weight: float = Field(0.2, ge=0, le=1, description="Weight for valuation metrics (0-1)")
    profitability_weight: float = Field(0.25, ge=0, le=1, description="Weight for profitability metrics (0-1)")
    growth_weight: float = Field(0.25, ge=0, le=1, description="Weight for growth metrics (0-1)")
    
    # Minimum score (weighted combination of criteria)
    min_score: Optional[float] = Field(None, description="Minimum overall score (0-100)")
    
    # Limit results
    limit: int = Field(50, ge=1, le=500, description="Maximum number of results to return")
    
    # Sort by
    sort_by: str = Field("score", description="Sort by: 'score', 'market_cap', 'pe_ratio', 'roe', 'revenue_growth', 'trendlyne_durability_score', 'trendlyne_valuation_score', 'trendlyne_momentum_score', 'piotroski_score'")

