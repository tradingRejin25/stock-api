"""
Quality Stocks Service - Analyzes stocks from Trendlyne Excel export
and categorizes them into Great, Aggressive, and Medium quality tiers.
"""
import os
import pandas as pd
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class QualityStock:
    """Represents a stock with quality metrics"""
    stock_name: str
    nse_code: str
    isin: str
    market_cap: float
    
    # Core Quality Metrics
    roe: float
    roce: float
    debt_to_equity: float
    interest_coverage: float
    current_ratio: float
    promoter_holding: float
    promoter_holding_change_1y: float
    
    # Growth Metrics
    eps_ttm_growth: float
    operating_rev_growth_ttm: float
    net_profit_ann: float
    net_profit_ann_1y_ago: float
    opm_ann: float
    opm_ann_1y_ago: float
    basic_eps_ttm: float
    basic_eps_ttm_1y_ago: float
    
    # Valuation Metrics
    pe_ttm: Optional[float]
    industry_pe_ttm: Optional[float]
    peg_ttm: Optional[float]
    price_to_book: Optional[float]
    ev_per_ebitda_ann: Optional[float]
    
    # Trendlyne Scores
    durability_score: Optional[int]
    valuation_score: Optional[int]
    
    # Quality Scores (Academic/Research-based)
    piotroski_score: Optional[int]
    altman_zscore: Optional[float]
    tobin_q_ratio: Optional[float]
    graham_number: Optional[float]
    
    # Additional Metrics
    eps_qtr_yoy_growth: float
    basic_eps_qoq_growth: float
    npm_ann: float
    npm_ttm: float
    
    # Quarterly Data for Better Analysis
    basic_eps_qtr: float
    basic_eps_1q_ago: float
    basic_eps_2q_ago: float
    net_profit_qtr: float
    net_profit_1q_ago: float
    net_profit_2q_ago: float
    opm_qtr: float
    opm_1q_ago: float
    opm_qtr_4q_ago: float
    
    # Promoter Holding Trends
    promoter_holding_change_qoq: float
    promoter_holding_change_2y: float
    
    # Additional Valuation
    sector_pe_ttm: Optional[float]
    sector_pbv_ttm: Optional[float]
    industry_pbv_ttm: Optional[float]
    
    # Additional Quality Metrics (from Excel)
    roa_ann: float  # Return on Assets
    roa_ann_1y_ago: float
    roe_1y_ago: float  # For trend analysis
    roe_2y_ago: float
    roe_3y_ago: float
    roe_4yr_ago: float
    roe_5y_ago: float
    roce_1y_ago: float
    roce_2y_ago: float
    roce_3y_ago: float
    roce_4yr_ago: float
    roce_5y_ago: float
    roce_3y_avg: float  # ROCE 3-year average
    roce_5y_avg: float  # ROCE 5-year average
    roa_ann_2y_ago: float
    roa_ann_3y_ago: float
    roa_ann_4yr_ago: float
    roa_ann_5y_ago: float
    cash_flow_return_on_assets: float
    cash_flow_return_on_assets_1y_ago: float
    cash_eps_ann: float
    cash_eps_ann_1y_ago: float
    cash_eps_1y_growth: float
    cash_eps_3y_growth: float
    cash_eps_5y_growth: float
    working_capital_turnover: float
    book_value: float
    price_to_sales_ann: Optional[float]
    price_to_sales_ttm: Optional[float]
    price_to_cashflow: Optional[float]
    graham_ratio: Optional[float]
    operating_profit_ttm: float
    operating_profit_ttm_1y_ago: float
    operating_profit_growth_qtr_yoy: float
    ebitda_ann: float
    ebitda_ttm: float
    ebitda_ann_margin: float
    ebit_ann_margin: float
    ebitda_qtr_yoy_growth: float
    promoter_pledge_percentage: float
    gross_npa_ratio: Optional[float]  # For banks
    capital_adequacy_ratio: Optional[float]  # For banks
    industry_score: Optional[int]
    sector_score: Optional[int]
    tl_checklist_positive_score: Optional[int]
    tl_checklist_negative_score: Optional[int]
    
    # Additional Revenue & Sales Metrics
    operating_revenue_ann: float
    operating_revenue_ann_1y_ago: float
    operating_revenue_ttm: float
    sales_growth_ann: float
    sales_growth_3y: float
    sales_growth_5y: float
    
    # Additional Profit Metrics
    net_profit_ann_2y_ago: float
    net_profit_ann_3y_ago: float
    net_profit_ann_4yr_ago: float
    net_profit_ann_5y_ago: float
    net_profit_ttm: float
    net_profit_ttm_3q_ago: float
    net_profit_ttm_4q_ago: float
    net_profit_ttm_5q_ago: float
    pbt_ann: float  # Profit Before Tax
    pbt_ann_1y_ago: float
    pbt_qtr: float
    pbt_1q_ago: float
    pbt_4q_ago: float
    total_profit_loss_ann: float
    
    # Additional Margin Metrics
    npm_4q_ago: float
    npm_1q_ago: float
    npm_qtr: float
    npm_ann_1y_ago: float
    opm_qtr_yoy_chg: float
    opm_ann_1y_ago: float
    opm_ttm: float
    
    # Additional EBITDA/EBIT Metrics
    ebitda_qtr: float
    ebitda_1q_ago: float
    ebitda_2q_ago: float
    ebitda_3q_ago: float
    ebitda_4q_ago: float
    ebitda_ann_1y_ago: float
    ebitda_ann_margin_percent: float
    ebitda_qtr_growth_yoy: float
    fc_est_1q_forward_ebit_qtr: float
    fc_est_1q_fwd_ebitda_qtr: float
    
    # Additional EPS Metrics
    basic_eps_3q_ago: float
    basic_eps_4q_ago: float
    eps_ann: float
    eps_ann_1y_ago: float
    
    # Asset & Efficiency Metrics
    asset_turnover: float
    inventory_turnover: float
    receivables_turnover: float
    fixed_asset_turnover: float
    
    # Debt & Liquidity Metrics
    total_debt: float
    short_term_debt: float
    long_term_debt: float
    quick_ratio: float
    cash_and_equivalents: float
    free_cash_flow: float
    free_cash_flow_1y_ago: float
    
    # Share & Capital Metrics
    share_capital: float
    reserves: float
    total_equity: float
    dividend_yield: Optional[float]
    dividend_payout_ratio: Optional[float]
    
    # Valuation Metrics (Additional)
    market_cap_to_sales: Optional[float]
    enterprise_value: Optional[float]
    
    # SWOT Analysis
    swot_strengths: str
    swot_weakness: str
    swot_threats: str
    swot_opportunities: str
    
    # Quality Score (calculated)
    quality_score: float = 0.0
    quality_tier: str = ""
    
    # Calculated Insights
    consecutive_positive_quarters: int = 0
    profit_growth_consistency: str = ""
    margin_stability: str = ""
    promoter_trend: str = ""
    cash_flow_quality: str = ""
    roe_trend: str = ""
    roce_consistency: str = ""


class QualityStocksService:
    """Service to analyze and filter quality stocks from CSV data"""
    
    def __init__(self, excel_path: str = None):
        if excel_path is None:
            # Try multiple possible paths
            possible_paths = [
                # Path relative to service file
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'trendlyne_data.xlsx'),
                # Absolute path (Windows)
                r'c:\Work\Trading\stock_ai\stock_api_service\data\trendlyne_data.xlsx',
                r'c:\Work\Trading\stock_api_service\data\trendlyne_data.xlsx',
                # Alternative relative path
                os.path.join('data', 'trendlyne_data.xlsx'),
            ]
            
            excel_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    excel_path = path
                    break
            
            if excel_path is None:
                # Use the first path as default (will show error if file not found)
                excel_path = possible_paths[0]
        
        self.excel_path = excel_path
        self.stocks: List[QualityStock] = []
    
    def _safe_float(self, value: Any, default: float = 0.0) -> float:
        """Safely convert value to float"""
        if value is None or value == '' or value == '-':
            return default
        try:
            return float(str(value).replace(',', ''))
        except (ValueError, TypeError):
            return default
    
    def _safe_int(self, value: Any, default: int = 0) -> int:
        """Safely convert value to int"""
        if value is None or value == '' or value == '-':
            return default
        try:
            return int(float(str(value).replace(',', '')))
        except (ValueError, TypeError):
            return default
    
    def load_stocks(self) -> List[QualityStock]:
        """Load and parse stocks from Excel file"""
        stocks = []
        
        try:
            # Check if file exists
            if not os.path.exists(self.excel_path):
                print(f"ERROR: Excel file not found at: {self.excel_path}")
                return []
            
            print(f"Loading stocks from: {self.excel_path}")
            # Read Excel file
            df = pd.read_excel(self.excel_path)
            print(f"Excel file loaded. Total rows: {len(df)}, Columns: {len(df.columns)}")
            
            # Convert DataFrame to list of dictionaries
            for _, row in df.iterrows():
                # Convert row to dictionary
                row_dict = row.to_dict()
                try:
                    stock = QualityStock(
                        stock_name=str(row_dict.get('Stock', '') or '').strip(),
                        nse_code=str(row_dict.get('NSE Code', '') or '').strip(),
                        isin=str(row_dict.get('ISIN', '') or '').strip(),
                        market_cap=self._safe_float(row_dict.get('Market Cap', 0)),
                        
                        # Core Quality Metrics
                        roe=self._safe_float(row_dict.get('ROE Ann  %', 0)),
                        roce=self._safe_float(row_dict.get('ROCE Ann  %', 0)),
                        debt_to_equity=self._safe_float(row_dict.get('Total Debt to Total Equity Ann ', 0)),
                        interest_coverage=self._safe_float(row_dict.get('Interest Coverage Ratio Ann ', 0)),
                        current_ratio=self._safe_float(row_dict.get('Current Ratio Ann ', 0)),
                        promoter_holding=self._safe_float(row_dict.get('Promoter holding latest %', 0)),
                        promoter_holding_change_1y=self._safe_float(row_dict.get('Promoter holding change 1Y %', 0)),
                        
                        # Growth Metrics
                        eps_ttm_growth=self._safe_float(row_dict.get('EPS TTM Growth %', 0)),
                        operating_rev_growth_ttm=self._safe_float(row_dict.get('Operating Rev  growth TTM %', 0)),
                        net_profit_ann=self._safe_float(row_dict.get('Net Profit Ann ', 0)),
                        net_profit_ann_1y_ago=self._safe_float(row_dict.get('Net Profit Ann  1Y Ago', 0)),
                        opm_ann=self._safe_float(row_dict.get('OPM Ann  %', 0)),
                        opm_ann_1y_ago=self._safe_float(row_dict.get('OPM Ann  1Y ago %', 0)),
                        basic_eps_ttm=self._safe_float(row_dict.get('Basic EPS TTM', 0)),
                        basic_eps_ttm_1y_ago=self._safe_float(row_dict.get('Basic EPS TTM 1Y Ago', 0)),
                        
                        # Valuation Metrics
                        # Note: Individual stock PE TTM not in Excel, can be calculated as Market Cap / (EPS * Shares)
                        # For now, using None - can be enhanced if needed
                        pe_ttm=None,
                        industry_pe_ttm=self._safe_float(row_dict.get('Industry PE TTM', 0)) if row_dict.get('Industry PE TTM') else None,
                        peg_ttm=self._safe_float(row_dict.get('PEG TTM', 0)) if row_dict.get('PEG TTM') else None,
                        price_to_book=self._safe_float(row_dict.get('Industry PBV TTM', 0)) if row_dict.get('Industry PBV TTM') else None,
                        ev_per_ebitda_ann=self._safe_float(row_dict.get('EV Per EBITDA Ann ', 0)) if row_dict.get('EV Per EBITDA Ann ') else None,
                        
                        # Trendlyne Scores
                        durability_score=self._safe_int(row_dict.get('Durability Score', 0)) if row_dict.get('Durability Score') else None,
                        valuation_score=self._safe_int(row_dict.get('Valuation Score', 0)) if row_dict.get('Valuation Score') else None,
                        
                        # Quality Scores (Academic/Research-based)
                        piotroski_score=self._safe_int(row_dict.get('Piotroski Score', 0)) if row_dict.get('Piotroski Score') else None,
                        altman_zscore=self._safe_float(row_dict.get('Altman Zscore', 0)) if row_dict.get('Altman Zscore') else None,
                        tobin_q_ratio=self._safe_float(row_dict.get('Tobin Q Ratio', 0)) if row_dict.get('Tobin Q Ratio') else None,
                        graham_number=self._safe_float(row_dict.get('Graham No ', 0)) if row_dict.get('Graham No ') else None,
                        
                        # Additional Metrics
                        eps_qtr_yoy_growth=self._safe_float(row_dict.get('EPS Qtr YoY Growth %', 0)),
                        basic_eps_qoq_growth=self._safe_float(row_dict.get('Basic EPS QoQ Growth %', 0)),
                        npm_ann=self._safe_float(row_dict.get('NPM Ann  %', 0)),
                        npm_ttm=self._safe_float(row_dict.get('NPM TTM %', 0)),
                        
                        # Quarterly Data
                        basic_eps_qtr=self._safe_float(row_dict.get('Basic EPS Qtr', 0)),
                        basic_eps_1q_ago=self._safe_float(row_dict.get('Basic EPS 1Q Ago', 0)),
                        basic_eps_2q_ago=self._safe_float(row_dict.get('Basic EPS 2Q Ago', 0)),
                        net_profit_qtr=self._safe_float(row_dict.get('Net Profit Qtr', 0)),
                        net_profit_1q_ago=self._safe_float(row_dict.get('Net Profit 1Q Ago', 0)),
                        net_profit_2q_ago=self._safe_float(row_dict.get('Net Profit 2Q Ago', 0)),
                        opm_qtr=self._safe_float(row_dict.get('Operating Profit Margin Qtr %', 0)),
                        opm_1q_ago=self._safe_float(row_dict.get('OPM 1Q ago %', 0)),
                        opm_qtr_4q_ago=self._safe_float(row_dict.get('OPM Qtr 4Qtr ago %', 0)),
                        
                        # Promoter Holding Trends
                        promoter_holding_change_qoq=self._safe_float(row_dict.get('Promoter holding change QoQ %', 0)),
                        promoter_holding_change_2y=self._safe_float(row_dict.get('Promoter holding change 2Y %', 0)),
                        
                        # Additional Valuation
                        sector_pe_ttm=self._safe_float(row_dict.get('Sector PE TTM', 0)) if row_dict.get('Sector PE TTM') else None,
                        sector_pbv_ttm=self._safe_float(row_dict.get('Sector PBV TTM', 0)) if row_dict.get('Sector PBV TTM') else None,
                        industry_pbv_ttm=self._safe_float(row_dict.get('Industry PBV TTM', 0)) if row_dict.get('Industry PBV TTM') else None,
                        
                        # Additional Quality Metrics - Historical ROE/ROCE/ROA
                        roa_ann=self._safe_float(row_dict.get('RoA Ann  %', 0) or row_dict.get('RoA Ann %', 0)),
                        roa_ann_1y_ago=self._safe_float(row_dict.get('RoA Ann  1Y Ago %', 0) or row_dict.get('RoA Ann 1Y Ago %', 0)),
                        roa_ann_2y_ago=self._safe_float(row_dict.get('RoA Ann  2Y Ago %', 0) or row_dict.get('RoA Ann 2Y Ago %', 0)),
                        roa_ann_3y_ago=self._safe_float(row_dict.get('RoA Ann  3Y Ago %', 0) or row_dict.get('RoA Ann 3Y Ago %', 0)),
                        roa_ann_4yr_ago=self._safe_float(row_dict.get('RoA Ann  4Yr Ago %', 0) or row_dict.get('RoA Ann 4Yr Ago %', 0)),
                        roa_ann_5y_ago=self._safe_float(row_dict.get('RoA Ann  5Y Ago %', 0) or row_dict.get('RoA Ann 5Y Ago %', 0)),
                        roe_1y_ago=self._safe_float(row_dict.get('ROE Ann  1Y Ago %', 0) or row_dict.get('ROE Ann 1Y Ago %', 0)),
                        roe_2y_ago=self._safe_float(row_dict.get('ROE Ann  2Y Ago %', 0) or row_dict.get('ROE Ann 2Y Ago %', 0)),
                        roe_3y_ago=self._safe_float(row_dict.get('ROE Ann  3Y Ago %', 0) or row_dict.get('ROE Ann 3Y Ago %', 0)),
                        roe_4yr_ago=self._safe_float(row_dict.get('ROE Ann  4Yr Ago %', 0) or row_dict.get('ROE Ann 4Yr Ago %', 0)),
                        roe_5y_ago=self._safe_float(row_dict.get('ROE Ann  5Y Ago %', 0) or row_dict.get('ROE Ann 5Y Ago %', 0)),
                        roce_1y_ago=self._safe_float(row_dict.get('ROCE Ann  1Y Ago %', 0) or row_dict.get('ROCE Ann 1Y Ago %', 0)),
                        roce_2y_ago=self._safe_float(row_dict.get('ROCE Ann  2Y Ago %', 0) or row_dict.get('ROCE Ann 2Y Ago %', 0)),
                        roce_3y_ago=self._safe_float(row_dict.get('ROCE Ann  3Y Ago %', 0) or row_dict.get('ROCE Ann 3Y Ago %', 0)),
                        roce_4yr_ago=self._safe_float(row_dict.get('ROCE Ann  4Yr Ago %', 0) or row_dict.get('ROCE Ann 4Yr Ago %', 0)),
                        roce_5y_ago=self._safe_float(row_dict.get('ROCE Ann  5Y Ago %', 0) or row_dict.get('ROCE Ann 5Y Ago %', 0)),
                        roce_3y_avg=self._safe_float(row_dict.get('ROCE Ann  3Y Avg %', 0) or row_dict.get('ROCE Ann 3Y Avg %', 0)),
                        roce_5y_avg=self._safe_float(row_dict.get('ROCE Ann  5Y Avg %', 0) or row_dict.get('ROCE Ann 5Y Avg %', 0)),
                        cash_flow_return_on_assets=self._safe_float(row_dict.get('Cash Flow Return on Assets Ann ', 0) or row_dict.get('Cash Flow Return on Assets Ann', 0)),
                        cash_flow_return_on_assets_1y_ago=self._safe_float(row_dict.get('Cash Flow Return on Assets Ann  1Y ago', 0) or row_dict.get('Cash Flow Return on Assets Ann 1Y ago', 0)),
                        cash_eps_ann=self._safe_float(row_dict.get('Cash EPS Ann ', 0) or row_dict.get('Cash EPS Ann', 0)),
                        cash_eps_ann_1y_ago=self._safe_float(row_dict.get('Cash EPS Ann  1Y Ago', 0) or row_dict.get('Cash EPS Ann 1Y Ago', 0)),
                        cash_eps_1y_growth=self._safe_float(row_dict.get('Cash EPS 1Y Growth %', 0)),
                        cash_eps_3y_growth=self._safe_float(row_dict.get('Cash EPS 3Y Growth %', 0)),
                        cash_eps_5y_growth=self._safe_float(row_dict.get('Cash EPS 5Y Growth %', 0)),
                        working_capital_turnover=self._safe_float(row_dict.get('Working Capital Turnover Ann ', 0) or row_dict.get('Working Capital Turnover Ann', 0)),
                        book_value=self._safe_float(row_dict.get('Book Value Inc Reval Reserve Ann ', 0) or row_dict.get('Book Value Inc Reval Reserve Ann', 0)),
                        price_to_sales_ann=self._safe_float(row_dict.get('Price To Sales Ann ', 0) or row_dict.get('Price To Sales Ann', 0)) if (row_dict.get('Price To Sales Ann ') or row_dict.get('Price To Sales Ann')) else None,
                        price_to_sales_ttm=self._safe_float(row_dict.get('Price to Sales TTM', 0) or row_dict.get('Price To Sales TTM', 0)) if (row_dict.get('Price to Sales TTM') or row_dict.get('Price To Sales TTM')) else None,
                        price_to_cashflow=self._safe_float(row_dict.get('Price to Cashflow from Operations', 0) or row_dict.get('Price To Cashflow from Operations', 0)) if (row_dict.get('Price to Cashflow from Operations') or row_dict.get('Price To Cashflow from Operations')) else None,
                        graham_ratio=self._safe_float(row_dict.get('Graham Ratio', 0)) if row_dict.get('Graham Ratio') else None,
                        operating_profit_ttm=self._safe_float(row_dict.get('Operating Profit TTM', 0)),
                        operating_profit_ttm_1y_ago=self._safe_float(row_dict.get('Operating Profit TTM 1Y Ago', 0)),
                        operating_profit_growth_qtr_yoy=self._safe_float(row_dict.get('Operating Profit Growth Qtr YoY %', 0)),
                        ebitda_ann=self._safe_float(row_dict.get('EBITDA Ann ', 0) or row_dict.get('EBITDA Ann', 0)),
                        ebitda_ttm=self._safe_float(row_dict.get('EBITDA TTM', 0)),
                        ebitda_ann_margin=self._safe_float(row_dict.get('EBITDA Ann  margin %', 0) or row_dict.get('EBITDA Ann margin %', 0)),
                        ebit_ann_margin=self._safe_float(row_dict.get('EBIT Ann  Margin %', 0) or row_dict.get('EBIT Ann Margin %', 0)),
                        ebitda_qtr_yoy_growth=self._safe_float(row_dict.get('EBITDA Qtr YoY Growth %', 0)),
                        promoter_pledge_percentage=self._safe_float(row_dict.get('Promoter holding pledge percentage % Qtr', 0) or row_dict.get('Promoter holding pledge percentage % Qtr', 0)),
                        gross_npa_ratio=self._safe_float(row_dict.get('Gross NPA ratio Qtr %', 0)) if row_dict.get('Gross NPA ratio Qtr %') else None,
                        capital_adequacy_ratio=self._safe_float(row_dict.get('Capital Adequacy Ratios Ann  %', 0) or row_dict.get('Capital Adequacy Ratios Ann %', 0)) if (row_dict.get('Capital Adequacy Ratios Ann  %') or row_dict.get('Capital Adequacy Ratios Ann %')) else None,
                        industry_score=self._safe_int(row_dict.get('Industry Score', 0)) if row_dict.get('Industry Score') else None,
                        sector_score=self._safe_int(row_dict.get('Sector Score', 0)) if row_dict.get('Sector Score') else None,
                        tl_checklist_positive_score=self._safe_int(row_dict.get('TL Checklist Positive Score', 0)) if row_dict.get('TL Checklist Positive Score') else None,
                        tl_checklist_negative_score=self._safe_int(row_dict.get('TL Checklist Negative Score', 0)) if row_dict.get('TL Checklist Negative Score') else None,
                        
                        # Additional Revenue & Sales Metrics
                        operating_revenue_ann=self._safe_float(row_dict.get('Operating Revenue Ann ', 0) or row_dict.get('Operating Revenue Ann', 0) or row_dict.get('Operating Rev Ann', 0)),
                        operating_revenue_ann_1y_ago=self._safe_float(row_dict.get('Operating Revenue Ann  1Y Ago', 0) or row_dict.get('Operating Revenue Ann 1Y Ago', 0)),
                        operating_revenue_ttm=self._safe_float(row_dict.get('Operating Revenue TTM', 0) or row_dict.get('Operating Rev TTM', 0)),
                        sales_growth_ann=self._safe_float(row_dict.get('Sales Growth Ann %', 0) or row_dict.get('Sales Growth %', 0)),
                        sales_growth_3y=self._safe_float(row_dict.get('Sales Growth 3Y %', 0) or row_dict.get('Sales 3Y Growth %', 0)),
                        sales_growth_5y=self._safe_float(row_dict.get('Sales Growth 5Y %', 0) or row_dict.get('Sales 5Y Growth %', 0)),
                        
                        # Additional Profit Metrics
                        net_profit_ann_2y_ago=self._safe_float(row_dict.get('Net Profit Ann  2Y Ago', 0) or row_dict.get('Net Profit Ann 2Y Ago', 0)),
                        net_profit_ann_3y_ago=self._safe_float(row_dict.get('Net Profit Ann  3Y Ago', 0) or row_dict.get('Net Profit Ann 3Y Ago', 0)),
                        net_profit_ann_4yr_ago=self._safe_float(row_dict.get('Net Profit Ann  4Yr Ago', 0) or row_dict.get('Net Profit Ann 4Yr Ago', 0)),
                        net_profit_ann_5y_ago=self._safe_float(row_dict.get('Net Profit Ann  5Y Ago', 0) or row_dict.get('Net Profit Ann 5Y Ago', 0)),
                        net_profit_ttm=self._safe_float(row_dict.get('Net Profit TTM', 0)),
                        net_profit_ttm_3q_ago=self._safe_float(row_dict.get('Net Profit TTM 3Q Ago', 0)),
                        net_profit_ttm_4q_ago=self._safe_float(row_dict.get('Net Profit TTM 4Q Ago', 0)),
                        net_profit_ttm_5q_ago=self._safe_float(row_dict.get('Net Profit TTM 5Q Ago', 0)),
                        pbt_ann=self._safe_float(row_dict.get('PBT Ann ', 0) or row_dict.get('PBT Ann', 0)),
                        pbt_ann_1y_ago=self._safe_float(row_dict.get('PBT Ann  1Y Ago', 0) or row_dict.get('PBT Ann 1Y Ago', 0)),
                        pbt_qtr=self._safe_float(row_dict.get('PBT Qtr', 0)),
                        pbt_1q_ago=self._safe_float(row_dict.get('PBT 1Q Ago', 0)),
                        pbt_4q_ago=self._safe_float(row_dict.get('PBT 4Q Ago', 0)),
                        total_profit_loss_ann=self._safe_float(row_dict.get('Total Profit Loss Ann ', 0) or row_dict.get('Total Profit Loss Ann', 0)),
                        
                        # Additional Margin Metrics
                        npm_4q_ago=self._safe_float(row_dict.get('NPM 4Q ago %', 0) or row_dict.get('NPM 4Q Ago %', 0)),
                        npm_1q_ago=self._safe_float(row_dict.get('NPM 1Q ago %', 0) or row_dict.get('NPM 1Q Ago %', 0)),
                        npm_qtr=self._safe_float(row_dict.get('NPM Qtr %', 0)),
                        npm_ann_1y_ago=self._safe_float(row_dict.get('NPM Ann  1Y ago %', 0) or row_dict.get('NPM Ann 1Y ago %', 0)),
                        opm_qtr_yoy_chg=self._safe_float(row_dict.get('OPM Qtr YoY Chg %', 0)),
                        opm_ttm=self._safe_float(row_dict.get('OPM TTM %', 0)),
                        
                        # Additional EBITDA/EBIT Metrics
                        ebitda_qtr=self._safe_float(row_dict.get('EBITDA Qtr', 0)),
                        ebitda_1q_ago=self._safe_float(row_dict.get('EBITDA 1Q Ago', 0)),
                        ebitda_2q_ago=self._safe_float(row_dict.get('EBITDA 2Q Ago', 0)),
                        ebitda_3q_ago=self._safe_float(row_dict.get('EBITDA 3Q Ago', 0)),
                        ebitda_4q_ago=self._safe_float(row_dict.get('EBITDA 4Q Ago', 0)),
                        ebitda_ann_1y_ago=self._safe_float(row_dict.get('EBITDA Ann  1Y Ago', 0) or row_dict.get('EBITDA Ann 1Y Ago', 0)),
                        ebitda_ann_margin_percent=self._safe_float(row_dict.get('EBITDA Ann Margin %', 0) or row_dict.get('EBITDA Ann  margin %', 0)),
                        ebitda_qtr_growth_yoy=self._safe_float(row_dict.get('EBITDA Qtr growth YoY %', 0) or row_dict.get('EBITDA Qtr Growth YoY %', 0)),
                        fc_est_1q_forward_ebit_qtr=self._safe_float(row_dict.get('FC Est 1Q forward EBIT Qtr', 0) or row_dict.get('FC Est 1Q forward EBIT Qtr', 0)),
                        fc_est_1q_fwd_ebitda_qtr=self._safe_float(row_dict.get('FC Est 1Q fwd EBITDA Qtr', 0) or row_dict.get('FC Est 1Q fwd EBITDA Qtr', 0)),
                        
                        # Additional EPS Metrics
                        basic_eps_3q_ago=self._safe_float(row_dict.get('Basic EPS 3Q Ago', 0)),
                        basic_eps_4q_ago=self._safe_float(row_dict.get('Basic EPS 4Q Ago', 0)),
                        eps_ann=self._safe_float(row_dict.get('EPS Ann ', 0) or row_dict.get('EPS Ann', 0)),
                        eps_ann_1y_ago=self._safe_float(row_dict.get('EPS Ann  1Y Ago', 0) or row_dict.get('EPS Ann 1Y Ago', 0)),
                        
                        # Asset & Efficiency Metrics (with fallbacks)
                        asset_turnover=self._safe_float(row_dict.get('Asset Turnover Ann ', 0) or row_dict.get('Asset Turnover', 0) or row_dict.get('Total Asset Turnover', 0)),
                        inventory_turnover=self._safe_float(row_dict.get('Inventory Turnover', 0)),
                        receivables_turnover=self._safe_float(row_dict.get('Receivables Turnover', 0) or row_dict.get('Debtors Turnover', 0)),
                        fixed_asset_turnover=self._safe_float(row_dict.get('Fixed Asset Turnover', 0)),
                        
                        # Debt & Liquidity Metrics
                        total_debt=self._safe_float(row_dict.get('Total Debt', 0) or row_dict.get('Total Debt Ann', 0)),
                        short_term_debt=self._safe_float(row_dict.get('Short Term Debt', 0)),
                        long_term_debt=self._safe_float(row_dict.get('Long Term Debt', 0)),
                        quick_ratio=self._safe_float(row_dict.get('Quick Ratio', 0)),
                        cash_and_equivalents=self._safe_float(row_dict.get('Cash and Equivalents', 0) or row_dict.get('Cash & Equivalents', 0)),
                        free_cash_flow=self._safe_float(row_dict.get('Free Cash Flow', 0) or row_dict.get('FCF', 0)),
                        free_cash_flow_1y_ago=self._safe_float(row_dict.get('Free Cash Flow 1Y Ago', 0)),
                        
                        # Share & Capital Metrics
                        share_capital=self._safe_float(row_dict.get('Share Capital', 0)),
                        reserves=self._safe_float(row_dict.get('Reserves', 0) or row_dict.get('Total Reserves', 0)),
                        total_equity=self._safe_float(row_dict.get('Total Equity', 0) or row_dict.get('Shareholders Equity', 0)),
                        dividend_yield=self._safe_float(row_dict.get('Dividend Yield %', 0)) if row_dict.get('Dividend Yield %') else None,
                        dividend_payout_ratio=self._safe_float(row_dict.get('Dividend Payout Ratio %', 0)) if row_dict.get('Dividend Payout Ratio %') else None,
                        
                        # Valuation Metrics (Additional)
                        market_cap_to_sales=self._safe_float(row_dict.get('Market Cap to Sales', 0)) if row_dict.get('Market Cap to Sales') else None,
                        enterprise_value=self._safe_float(row_dict.get('Enterprise Value', 0) or row_dict.get('EV', 0)) if (row_dict.get('Enterprise Value') or row_dict.get('EV')) else None,
                        
                        # SWOT Analysis
                        swot_strengths=str(row_dict.get('SWOT Strengths', '') or ''),
                        swot_weakness=str(row_dict.get('SWOT Weakness', '') or ''),
                        swot_threats=str(row_dict.get('SWOT Threats', '') or ''),
                        swot_opportunities=str(row_dict.get('SWOT Opportunities', '') or ''),
                        )
                    
                    # Calculate additional insights with error handling
                    try:
                        stock.cash_flow_quality = self._assess_cash_flow_quality(stock) or "Unknown"
                    except:
                        stock.cash_flow_quality = "Unknown"
                    
                    try:
                        stock.roe_trend = self._assess_roe_trend(stock) or "Unknown"
                    except:
                        stock.roe_trend = "Unknown"
                    
                    try:
                        stock.roce_consistency = self._assess_roce_consistency(stock) or "Unknown"
                    except:
                        stock.roce_consistency = "Unknown"
                    
                    # Calculate insights after creating stock
                    try:
                        stock.consecutive_positive_quarters = self._count_consecutive_positive_quarters(stock)
                    except:
                        stock.consecutive_positive_quarters = 0
                    
                    try:
                        stock.profit_growth_consistency = self._assess_profit_growth_consistency(stock) or "Unknown"
                    except:
                        stock.profit_growth_consistency = "Unknown"
                    
                    try:
                        stock.margin_stability = self._assess_margin_stability(stock) or "Unknown"
                    except:
                        stock.margin_stability = "Unknown"
                    
                    try:
                        stock.promoter_trend = self._assess_promoter_trend(stock) or "Unknown"
                    except:
                        stock.promoter_trend = "Unknown"
                    
                    if stock.nse_code:  # Only add stocks with NSE code
                        stocks.append(stock)
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
            
            self.stocks = stocks
            print(f"Successfully loaded {len(stocks)} stocks")
            return stocks
        
        except FileNotFoundError:
            print(f"Excel file not found at: {self.excel_path}")
            return []
        except Exception as e:
            print(f"Error loading stocks: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def calculate_quality_score(self, stock: QualityStock) -> float:
        """
        Calculate quality score based on multiple parameters
        Higher score = Better quality
        """
        score = 0.0
        max_score = 0.0
        
        # 1. ROE (0-20 points)
        if stock.roe > 20:
            score += 20
        elif stock.roe > 15:
            score += 15
        elif stock.roe > 12:
            score += 10
        elif stock.roe > 8:
            score += 5
        max_score += 20
        
        # 2. ROCE (0-20 points)
        if stock.roce > 25:
            score += 20
        elif stock.roce > 20:
            score += 15
        elif stock.roce > 15:
            score += 10
        elif stock.roce > 10:
            score += 5
        max_score += 20
        
        # 3. Debt/Equity (0-15 points) - Lower is better
        if stock.debt_to_equity == 0:
            score += 15
        elif stock.debt_to_equity < 0.3:
            score += 12
        elif stock.debt_to_equity < 0.5:
            score += 10
        elif stock.debt_to_equity < 1.0:
            score += 7
        elif stock.debt_to_equity < 1.5:
            score += 3
        max_score += 15
        
        # 4. Interest Coverage (0-10 points)
        if stock.interest_coverage > 10:
            score += 10
        elif stock.interest_coverage > 5:
            score += 8
        elif stock.interest_coverage > 3:
            score += 5
        elif stock.interest_coverage > 1.5:
            score += 2
        max_score += 10
        
        # 5. Current Ratio (0-10 points)
        if stock.current_ratio > 2.0:
            score += 10
        elif stock.current_ratio > 1.5:
            score += 8
        elif stock.current_ratio > 1.2:
            score += 5
        elif stock.current_ratio > 1.0:
            score += 2
        max_score += 10
        
        # 6. Promoter Holding (0-5 points)
        if stock.promoter_holding > 50:
            score += 5
        elif stock.promoter_holding > 30:
            score += 3
        elif stock.promoter_holding > 20:
            score += 1
        # Bonus for increasing promoter holding
        if stock.promoter_holding_change_1y > 0:
            score += 2
        max_score += 7
        
        # 7. EPS Growth (0-10 points)
        if stock.eps_ttm_growth > 20:
            score += 10
        elif stock.eps_ttm_growth > 10:
            score += 7
        elif stock.eps_ttm_growth > 5:
            score += 4
        elif stock.eps_ttm_growth > 0:
            score += 2
        max_score += 10
        
        # 8. Revenue Growth (0-10 points)
        if stock.operating_rev_growth_ttm > 20:
            score += 10
        elif stock.operating_rev_growth_ttm > 15:
            score += 8
        elif stock.operating_rev_growth_ttm > 10:
            score += 5
        elif stock.operating_rev_growth_ttm > 5:
            score += 2
        max_score += 10
        
        # 9. Profit Growth Consistency (0-8 points)
        if stock.net_profit_ann > 0 and stock.net_profit_ann_1y_ago > 0:
            profit_growth = ((stock.net_profit_ann - stock.net_profit_ann_1y_ago) / 
                           abs(stock.net_profit_ann_1y_ago)) * 100
            if profit_growth > 20:
                score += 8
            elif profit_growth > 10:
                score += 5
            elif profit_growth > 0:
                score += 2
        max_score += 8
        
        # 10. Operating Margin Trend (0-5 points)
        if stock.opm_ann > stock.opm_ann_1y_ago and stock.opm_ann > 15:
            score += 5
        elif stock.opm_ann > stock.opm_ann_1y_ago:
            score += 3
        elif stock.opm_ann > 10:
            score += 1
        max_score += 5
        
        # 11. PEG Ratio (0-5 points) - Only if positive
        if stock.peg_ttm and stock.peg_ttm > 0:
            if 0.7 <= stock.peg_ttm <= 1.5:
                score += 5
            elif 0.5 <= stock.peg_ttm <= 2.0:
                score += 3
            elif stock.peg_ttm < 0.5:
                score += 1
        max_score += 5
        
        # 12. Quarterly EPS Growth (0-8 points) - Prefer 2+ consecutive positive quarters
        if stock.consecutive_positive_quarters >= 2:
            score += 8
        elif stock.consecutive_positive_quarters == 1:
            score += 4
        elif stock.basic_eps_qoq_growth > 0:
            score += 2
        max_score += 8
        
        # 13. PE vs Industry PE (0-5 points) - Prefer lower or similar
        if stock.pe_ttm and stock.industry_pe_ttm and stock.industry_pe_ttm > 0:
            pe_ratio = stock.pe_ttm / stock.industry_pe_ttm
            if pe_ratio < 0.9:  # Lower than industry
                score += 5
            elif pe_ratio <= 1.1:  # Similar to industry
                score += 3
            elif pe_ratio <= 1.3:  # Slightly higher
                score += 1
        elif stock.sector_pe_ttm and stock.sector_pe_ttm > 0:
            # Use sector PE as fallback
            if stock.pe_ttm:
                pe_ratio = stock.pe_ttm / stock.sector_pe_ttm
                if pe_ratio < 0.9:
                    score += 4
                elif pe_ratio <= 1.1:
                    score += 2
        max_score += 5
        
        # 14. Price to Book (0-5 points) - Sector dependent, lower is generally better
        if stock.price_to_book:
            if stock.price_to_book < 1.0:  # Undervalued
                score += 5
            elif stock.price_to_book < 2.0:
                score += 3
            elif stock.price_to_book < 3.0:
                score += 1
        elif stock.industry_pbv_ttm:
            # Compare to industry average
            if stock.industry_pbv_ttm < 2.0:
                score += 2
        max_score += 5
        
        # 15. EV/EBITDA (0-5 points) - Important for capital-heavy stocks
        if stock.ev_per_ebitda_ann:
            if stock.ev_per_ebitda_ann < 8:  # Very attractive
                score += 5
            elif stock.ev_per_ebitda_ann < 12:  # Reasonable
                score += 3
            elif stock.ev_per_ebitda_ann < 15:  # Acceptable
                score += 1
        max_score += 5
        
        # 16. Promoter Trend Bonus (0-3 points) - Stable or rising is better
        if stock.promoter_trend in ["Rising (Strong)", "Rising"]:
            score += 3
        elif stock.promoter_trend == "Rising (Moderate)":
            score += 2
        elif stock.promoter_trend == "Stable":
            score += 1
        max_score += 3
        
        # 17. Margin Stability Bonus (0-3 points)
        if stock.margin_stability == "Expanding":
            score += 3
        elif stock.margin_stability == "Stable":
            score += 2
        elif stock.margin_stability == "Moderately Stable":
            score += 1
        max_score += 3
        
        # 18. Profit Growth Consistency Bonus (0-4 points)
        if stock.profit_growth_consistency == "Very Consistent":
            score += 4
        elif stock.profit_growth_consistency == "Consistent":
            score += 3
        elif stock.profit_growth_consistency == "Moderate":
            score += 1
        max_score += 4
        
        # 19. Trendlyne Scores (0-14 points)
        tl_score = 0
        if stock.durability_score:
            tl_score += min(stock.durability_score / 2, 7)  # Max 7 points
        if stock.valuation_score:
            tl_score += min(stock.valuation_score / 2, 7)  # Max 7 points
        score += tl_score
        max_score += 14
        
        # 20. Piotroski Score (0-9 points) - F-Score: 0-9 scale
        if stock.piotroski_score is not None:
            # Piotroski score is already 0-9, scale to 9 points
            score += min(stock.piotroski_score, 9)
        max_score += 9
        
        # 21. Altman Z-Score (0-6 points) - Financial distress predictor
        if stock.altman_zscore:
            if stock.altman_zscore > 3.0:  # Safe zone
                score += 6
            elif stock.altman_zscore > 2.7:  # Grey zone (safe)
                score += 4
            elif stock.altman_zscore > 1.8:  # Grey zone (caution)
                score += 2
            # Below 1.8 is distress zone - 0 points
        max_score += 6
        
        # 22. Tobin Q Ratio (0-5 points) - Market vs Book value
        if stock.tobin_q_ratio:
            if 0.8 <= stock.tobin_q_ratio <= 1.2:  # Fairly valued
                score += 5
            elif 0.6 <= stock.tobin_q_ratio < 0.8:  # Undervalued
                score += 4
            elif 1.2 < stock.tobin_q_ratio <= 1.5:  # Slightly overvalued
                score += 2
            elif stock.tobin_q_ratio > 1.5:  # Overvalued
                score += 1
            # Very low (< 0.6) might indicate distress - 0 points
        max_score += 5
        
        # 23. Graham Number (0-4 points) - Intrinsic value indicator
        if stock.graham_number and stock.market_cap > 0:
            # Compare market cap to Graham number (lower market cap = better)
            # This is a simplified check - ideally compare to current price
            # Higher Graham number relative to market cap suggests undervaluation
            if stock.graham_number > 0:
                # If Graham number is significantly positive, it's a good sign
                # We'll give points based on presence and reasonableness
                score += 2  # Base points for having a Graham number
                # Additional points if it suggests good fundamentals
                if stock.graham_number > stock.market_cap * 0.5:
                    score += 2  # Suggests reasonable valuation
        max_score += 4
        
        # 24. ROA (Return on Assets) (0-5 points) - Asset efficiency
        if stock.roa_ann > 10:
            score += 5
        elif stock.roa_ann > 7:
            score += 4
        elif stock.roa_ann > 5:
            score += 3
        elif stock.roa_ann > 3:
            score += 1
        # Bonus for improving ROA
        if stock.roa_ann > stock.roa_ann_1y_ago and stock.roa_ann > 5:
            score += 1
        max_score += 6
        
        # 25. Cash Flow Quality (0-5 points) - Cash generation ability
        if stock.cash_flow_return_on_assets > 10:
            score += 5
        elif stock.cash_flow_return_on_assets > 7:
            score += 4
        elif stock.cash_flow_return_on_assets > 5:
            score += 3
        elif stock.cash_flow_return_on_assets > 0:
            score += 1
        # Bonus for improving cash flow
        if stock.cash_flow_quality == "Improving":
            score += 1
        max_score += 6
        
        # 26. Cash EPS Growth (0-4 points) - Quality earnings indicator
        if stock.cash_eps_1y_growth > 20:
            score += 4
        elif stock.cash_eps_1y_growth > 10:
            score += 3
        elif stock.cash_eps_1y_growth > 5:
            score += 2
        elif stock.cash_eps_1y_growth > 0:
            score += 1
        max_score += 4
        
        # 27. Working Capital Efficiency (0-3 points)
        if stock.working_capital_turnover > 10:
            score += 3
        elif stock.working_capital_turnover > 5:
            score += 2
        elif stock.working_capital_turnover > 2:
            score += 1
        max_score += 3
        
        # 28. Operating Profit TTM Growth (0-4 points) - Better than annual
        if stock.operating_profit_ttm > 0 and stock.operating_profit_ttm_1y_ago > 0 and stock.operating_profit_ttm_1y_ago != 0:
            op_profit_growth = ((stock.operating_profit_ttm - stock.operating_profit_ttm_1y_ago) / 
                               abs(stock.operating_profit_ttm_1y_ago)) * 100
            if op_profit_growth > 20:
                score += 4
            elif op_profit_growth > 10:
                score += 3
            elif op_profit_growth > 5:
                score += 2
            elif op_profit_growth > 0:
                score += 1
        max_score += 4
        
        # 29. EBITDA Quality (0-4 points) - Operational efficiency
        if stock.ebitda_ann_margin > 25:
            score += 4
        elif stock.ebitda_ann_margin > 20:
            score += 3
        elif stock.ebitda_ann_margin > 15:
            score += 2
        elif stock.ebitda_ann_margin > 10:
            score += 1
        # Bonus for EBITDA growth
        if stock.ebitda_qtr_yoy_growth > 15:
            score += 1
        max_score += 5
        
        # 30. Price to Sales (0-3 points) - Revenue valuation
        if stock.price_to_sales_ttm:
            if stock.price_to_sales_ttm < 1.0:
                score += 3
            elif stock.price_to_sales_ttm < 2.0:
                score += 2
            elif stock.price_to_sales_ttm < 3.0:
                score += 1
        elif stock.price_to_sales_ann:
            if stock.price_to_sales_ann < 1.0:
                score += 3
            elif stock.price_to_sales_ann < 2.0:
                score += 2
        max_score += 3
        
        # 31. Price to Cashflow (0-3 points) - Cash valuation
        if stock.price_to_cashflow:
            if stock.price_to_cashflow < 10:
                score += 3
            elif stock.price_to_cashflow < 15:
                score += 2
            elif stock.price_to_cashflow < 20:
                score += 1
        max_score += 3
        
        # 32. ROCE Consistency (0-3 points) - Long-term consistency
        if stock.roce_consistency == "Very Consistent":
            score += 3
        elif stock.roce_consistency == "Consistent":
            score += 2
        elif stock.roce_consistency == "Improving":
            score += 1
        max_score += 3
        
        # 33. ROE Trend (0-2 points) - Multi-year trend
        if stock.roe_trend == "Consistently Rising":
            score += 2
        elif stock.roe_trend == "Rising":
            score += 1
        max_score += 2
        
        # 34. Promoter Pledge (0-2 points) - Lower is better (risk indicator)
        if stock.promoter_pledge_percentage == 0:
            score += 2
        elif stock.promoter_pledge_percentage < 10:
            score += 1
        # High pledge (> 25%) might be a concern but not penalizing heavily
        max_score += 2
        
        # 35. Industry/Sector Relative Performance (0-3 points)
        if stock.industry_score:
            score += min(stock.industry_score / 20, 1.5)  # Max 1.5 points
        if stock.sector_score:
            score += min(stock.sector_score / 20, 1.5)  # Max 1.5 points
        max_score += 3
        
        # 36. TL Checklist (0-2 points) - Quality checklist
        if stock.tl_checklist_positive_score and stock.tl_checklist_negative_score:
            net_score = stock.tl_checklist_positive_score - stock.tl_checklist_negative_score
            if net_score > 10:
                score += 2
            elif net_score > 5:
                score += 1
        max_score += 2
        
        # 37. Bank-specific metrics (0-3 points) - For financial stocks
        if stock.gross_npa_ratio is not None:
            # Lower NPA is better
            if stock.gross_npa_ratio < 1.0:
                score += 2
            elif stock.gross_npa_ratio < 2.0:
                score += 1
        if stock.capital_adequacy_ratio:
            # Higher is better (should be > 10%)
            if stock.capital_adequacy_ratio > 15:
                score += 1
        max_score += 3
        
        # 38. Sales Growth (3Y & 5Y) (0-4 points) - Long-term growth sustainability
        if stock.sales_growth_3y > 15:
            score += 2
        elif stock.sales_growth_3y > 10:
            score += 1
        if stock.sales_growth_5y > 12:
            score += 2
        elif stock.sales_growth_5y > 8:
            score += 1
        max_score += 4
        
        # 39. Free Cash Flow (0-4 points) - Cash generation ability
        if stock.free_cash_flow > 0:
            if stock.free_cash_flow > stock.free_cash_flow_1y_ago and stock.free_cash_flow_1y_ago > 0:
                # Improving FCF
                fcf_growth = ((stock.free_cash_flow - stock.free_cash_flow_1y_ago) / abs(stock.free_cash_flow_1y_ago)) * 100
                if fcf_growth > 20:
                    score += 4
                elif fcf_growth > 10:
                    score += 3
                elif fcf_growth > 0:
                    score += 2
            else:
                score += 1  # Positive FCF
        max_score += 4
        
        # 40. Asset Turnover Ratios (0-3 points) - Efficiency metrics
        if stock.asset_turnover > 1.5:
            score += 1
        if stock.inventory_turnover > 5:
            score += 1
        if stock.receivables_turnover > 8:
            score += 1
        max_score += 3
        
        # 41. Quick Ratio (0-2 points) - Better liquidity indicator than current ratio
        if stock.quick_ratio > 1.5:
            score += 2
        elif stock.quick_ratio > 1.0:
            score += 1
        max_score += 2
        
        # 42. Dividend Metrics (0-3 points) - Shareholder returns
        if stock.dividend_yield and stock.dividend_yield > 2:
            score += 1
        if stock.dividend_payout_ratio and 20 <= stock.dividend_payout_ratio <= 60:
            # Reasonable payout ratio (not too high, not too low)
            score += 1
        if stock.dividend_yield and stock.dividend_yield > 0:
            score += 1  # Bonus for paying dividends
        max_score += 3
        
        # 43. Cash EPS Multi-year Growth (0-3 points) - Quality earnings trend
        if stock.cash_eps_3y_growth > 15:
            score += 2
        elif stock.cash_eps_3y_growth > 10:
            score += 1
        if stock.cash_eps_5y_growth > 12:
            score += 1
        max_score += 3
        
        # 44. PBT Growth (0-2 points) - Pre-tax profit quality
        if stock.pbt_ann > 0 and stock.pbt_ann_1y_ago > 0:
            pbt_growth = ((stock.pbt_ann - stock.pbt_ann_1y_ago) / abs(stock.pbt_ann_1y_ago)) * 100
            if pbt_growth > 15:
                score += 2
            elif pbt_growth > 0:
                score += 1
        max_score += 2
        
        # 45. Net Profit TTM Trend (0-2 points) - Recent profit momentum
        if stock.net_profit_ttm > 0:
            if stock.net_profit_ttm_3q_ago > 0:
                # Compare recent quarters
                if stock.net_profit_ttm > stock.net_profit_ttm_3q_ago:
                    score += 2
                elif stock.net_profit_ttm > stock.net_profit_ttm_4q_ago:
                    score += 1
        max_score += 2
        
        # 46. ROA Trend (0-2 points) - Multi-year asset efficiency
        if stock.roa_ann > stock.roa_ann_1y_ago > stock.roa_ann_2y_ago:
            score += 2
        elif stock.roa_ann > stock.roa_ann_1y_ago:
            score += 1
        max_score += 2
        
        # 47. Cash & Equivalents (0-2 points) - Financial strength
        if stock.market_cap > 0 and stock.cash_and_equivalents > 0:
            try:
                cash_ratio = stock.cash_and_equivalents / stock.market_cap
            except (ZeroDivisionError, TypeError):
                cash_ratio = 0
            if cash_ratio > 0.1:  # > 10% of market cap
                score += 2
            elif cash_ratio > 0.05:  # > 5% of market cap
                score += 1
        max_score += 2
        
        # 48. Enterprise Value vs Market Cap (0-2 points) - Capital structure
        if stock.enterprise_value and stock.market_cap > 0:
            ev_mc_ratio = stock.enterprise_value / stock.market_cap
            if 0.9 <= ev_mc_ratio <= 1.1:  # Similar (low debt)
                score += 2
            elif ev_mc_ratio < 1.2:  # Reasonable
                score += 1
        max_score += 2
        
        # Normalize to 0-100 scale
        if max_score > 0:
            normalized_score = (score / max_score) * 100
        else:
            normalized_score = 0.0
        
        return round(normalized_score, 2)
    
    def filter_great_quality_stocks(self) -> List[QualityStock]:
        """Filter stocks meeting great quality criteria - no limits, only quality stocks"""
        if not self.stocks:
            self.load_stocks()
        
        # Calculate scores
        for stock in self.stocks:
            stock.quality_score = self.calculate_quality_score(stock)
        
        # Filter based on strict criteria - using ALL parameters
        # Only include stocks that meet ALL quality thresholds
        great_stocks = []
        for stock in self.stocks:
            # Check all quality parameters - strict but practical criteria
            # Core financial metrics (must meet these - these are the most important)
            # Made slightly more lenient to account for data variations
            core_requirements = (
                stock.roe > 12 and
                stock.roce > 15 and
                stock.debt_to_equity < 1.0 and
                stock.interest_coverage > 3 and
                stock.current_ratio > 1.2 and
                stock.eps_ttm_growth > 0 and
                stock.operating_rev_growth_ttm > 10 and
                stock.quality_score >= 60 and  # Lowered to 60 to be more inclusive
                stock.market_cap > 0
            )
            
            # Additional quality checks (lenient - allow missing/zero data)
            # These are nice-to-have but not critical
            additional_checks = (
                # ROA - allow missing
                (stock.roa_ann > 5 or stock.roa_ann == 0) and
                # Cash flow - allow missing
                (stock.cash_flow_return_on_assets > 0 or stock.cash_flow_return_on_assets == 0) and
                # Cash flow quality - allow unknown/missing
                (stock.cash_flow_quality != "Negative" or stock.cash_flow_quality in ["", "Unknown"]) and
                # Promoter pledge - allow missing
                (stock.promoter_pledge_percentage < 30 or stock.promoter_pledge_percentage == 0) and
                # Altman Z-Score - allow missing
                (stock.altman_zscore is None or stock.altman_zscore > 1.8) and
                # Quick ratio - allow missing
                (stock.quick_ratio > 1.0 or stock.quick_ratio == 0) and
                # Net profit TTM - allow missing
                (stock.net_profit_ttm > 0 or stock.net_profit_ttm == 0) and
                # Dividend yield - allow missing
                (stock.dividend_yield is None or stock.dividend_yield >= 0)
            )
            
            # Growth consistency checks (very lenient - these are calculated fields)
            # Allow empty/unknown values since they might not be calculated correctly
            growth_checks = (
                (stock.consecutive_positive_quarters >= 1 or stock.consecutive_positive_quarters == 0) and
                (stock.profit_growth_consistency in ["Consistent", "Very Consistent", "Moderate", "", "Unknown"] or 
                 stock.profit_growth_consistency not in ["Inconsistent", "Negative"]) and
                (stock.margin_stability in ["Stable", "Expanding", "Moderately Stable", "", "Unknown"] or
                 stock.margin_stability not in ["Volatile", "Negative"])
            )
            
            meets_criteria = core_requirements and additional_checks and growth_checks
            
            if meets_criteria:
                stock.quality_tier = "Great"
                great_stocks.append(stock)
        
        # Sort by quality score descending (no limit)
        great_stocks.sort(key=lambda x: x.quality_score, reverse=True)
        return great_stocks
    
    def filter_aggressive_quality_stocks(self) -> List[QualityStock]:
        """Filter stocks for aggressive growth (higher risk, higher reward) - only quality stocks"""
        if not self.stocks:
            self.load_stocks()
        
        # Calculate scores
        for stock in self.stocks:
            stock.quality_score = self.calculate_quality_score(stock)
        
        aggressive_stocks = []
        for stock in self.stocks:
            # More lenient criteria but still quality-focused
            # Exclude stocks that don't meet minimum quality thresholds
            if (stock.roe > 10 and
                stock.roce > 12 and
                stock.debt_to_equity < 1.5 and
                stock.interest_coverage > 2 and
                (stock.eps_ttm_growth > 15 or stock.operating_rev_growth_ttm > 20) and
                stock.quality_score >= 60 and
                stock.market_cap > 0 and
                # Exclude stocks with negative or inconsistent growth
                stock.profit_growth_consistency != "Inconsistent" and
                stock.margin_stability != "Volatile" and
                # Additional quality checks
                stock.roa_ann > 3 and  # Minimum asset efficiency
                stock.cash_flow_quality != "Negative" and  # Positive cash flow
                stock.promoter_pledge_percentage < 40 and  # Reasonable pledge level
                (stock.altman_zscore is None or stock.altman_zscore > 1.5) and  # Not in severe distress
                # Enhanced checks with new fields
                stock.quick_ratio > 0.8 and  # Reasonable quick ratio
                (stock.free_cash_flow > 0 or stock.free_cash_flow == 0) and  # Not negative FCF
                stock.net_profit_ttm > 0):  # Positive TTM profit
                stock.quality_tier = "Aggressive"
                aggressive_stocks.append(stock)
        
        # Sort by growth potential (EPS growth + Revenue growth)
        aggressive_stocks.sort(
            key=lambda x: (x.eps_ttm_growth + x.operating_rev_growth_ttm) / 2,
            reverse=True
        )
        return aggressive_stocks
    
    def filter_medium_quality_stocks(self, exclude_great: List[QualityStock] = None, exclude_aggressive: List[QualityStock] = None) -> List[QualityStock]:
        """Filter stocks for medium/good quality (balanced risk-reward) - only significant quality stocks"""
        if not self.stocks:
            self.load_stocks()
        
        # Calculate scores
        for stock in self.stocks:
            stock.quality_score = self.calculate_quality_score(stock)
        
        medium_stocks = []
        # Get great and aggressive stocks to exclude them (if not provided)
        if exclude_great is None:
            exclude_great = []
        if exclude_aggressive is None:
            exclude_aggressive = []
        
        great_nse_codes = {s.nse_code for s in exclude_great}
        aggressive_nse_codes = {s.nse_code for s in exclude_aggressive}
        
        for stock in self.stocks:
            # Skip if already in great or aggressive
            if stock.nse_code in great_nse_codes or stock.nse_code in aggressive_nse_codes:
                continue
            
            # Good quality criteria - still significant quality
            # Exclude stocks that don't meet minimum quality thresholds
            if (stock.roe > 8 and
                stock.roce > 10 and
                stock.debt_to_equity < 2.0 and
                stock.interest_coverage > 1.5 and
                stock.quality_score >= 55 and  # Raised minimum to 55 (was 50)
                stock.quality_score < 70 and  # Not great quality
                stock.market_cap > 0 and
                # Exclude poor quality indicators
                stock.profit_growth_consistency != "Inconsistent" and
                stock.margin_stability != "Volatile" and
                # Exclude poor cash flow quality
                stock.cash_flow_quality != "Negative" and
                # Enhanced checks with new fields
                stock.roa_ann > 2 and  # Minimum asset efficiency
                stock.promoter_pledge_percentage < 50 and  # Reasonable pledge
                (stock.altman_zscore is None or stock.altman_zscore > 1.2) and  # Not in severe distress
                stock.quick_ratio > 0.7 and  # Reasonable liquidity
                stock.net_profit_ttm > 0 and  # Positive TTM profit
                # At least some positive growth
                (stock.eps_ttm_growth > -5 or stock.operating_rev_growth_ttm > 5)):
                stock.quality_tier = "Good"
                medium_stocks.append(stock)
        
        # Sort by quality score
        medium_stocks.sort(key=lambda x: x.quality_score, reverse=True)
        return medium_stocks
    
    def get_stock_by_nse_code(self, nse_code: str) -> Optional[QualityStock]:
        """Get a specific stock by NSE code"""
        if not self.stocks:
            self.load_stocks()
        
        for stock in self.stocks:
            if stock.nse_code.upper() == nse_code.upper():
                stock.quality_score = self.calculate_quality_score(stock)
                return stock
        return None
    
    def _count_consecutive_positive_quarters(self, stock: QualityStock) -> int:
        """Count consecutive quarters with positive EPS growth"""
        count = 0
        quarters = [
            (stock.basic_eps_qtr, stock.basic_eps_1q_ago),
            (stock.basic_eps_1q_ago, stock.basic_eps_2q_ago),
        ]
        
        for current, previous in quarters:
            if current > 0 and previous > 0 and current > previous:
                count += 1
            elif current > 0 and previous <= 0:
                count += 1
            else:
                break
        
        return count
    
    def _assess_profit_growth_consistency(self, stock: QualityStock) -> str:
        """Assess if profit growth is consistent (not one-time)"""
        if stock.net_profit_ann <= 0 or stock.net_profit_ann_1y_ago <= 0:
            return "Negative"
        
        # Check YoY growth
        if stock.net_profit_ann_1y_ago == 0:
            return "Inconsistent"  # Can't calculate growth if previous year is zero
        profit_growth_yoy = ((stock.net_profit_ann - stock.net_profit_ann_1y_ago) / 
                           abs(stock.net_profit_ann_1y_ago)) * 100
        
        # Check quarterly consistency
        quarters_positive = 0
        if stock.net_profit_qtr > 0:
            quarters_positive += 1
        if stock.net_profit_1q_ago > 0:
            quarters_positive += 1
        if stock.net_profit_2q_ago > 0:
            quarters_positive += 1
        
        if profit_growth_yoy > 15 and quarters_positive >= 2:
            return "Very Consistent"
        elif profit_growth_yoy > 10 and quarters_positive >= 2:
            return "Consistent"
        elif profit_growth_yoy > 0:
            return "Moderate"
        else:
            return "Inconsistent"
    
    def _assess_margin_stability(self, stock: QualityStock) -> str:
        """Assess operating margin stability/trend"""
        if stock.opm_ann <= 0:
            return "Negative"
        
        # Check if expanding
        if stock.opm_ann > stock.opm_ann_1y_ago:
            if stock.opm_qtr > stock.opm_1q_ago:
                return "Expanding"
            else:
                return "Expanding (Volatile)"
        
        # Check stability
        margin_change = abs(stock.opm_ann - stock.opm_ann_1y_ago) / max(stock.opm_ann_1y_ago, 1)
        if margin_change < 0.05:  # Less than 5% change
            return "Stable"
        elif margin_change < 0.15:
            return "Moderately Stable"
        else:
            return "Volatile"
    
    def _assess_promoter_trend(self, stock: QualityStock) -> str:
        """Assess promoter holding trend"""
        if stock.promoter_holding_change_1y > 1:
            if stock.promoter_holding_change_qoq > 0:
                return "Rising (Strong)"
            else:
                return "Rising"
        elif stock.promoter_holding_change_1y > 0:
            return "Rising (Moderate)"
        elif abs(stock.promoter_holding_change_1y) < 1:
            return "Stable"
        else:
            return "Declining"
    
    def _assess_cash_flow_quality(self, stock: QualityStock) -> str:
        """Assess cash flow quality"""
        if stock.cash_flow_return_on_assets > 0 and stock.cash_flow_return_on_assets_1y_ago > 0:
            if stock.cash_flow_return_on_assets > stock.cash_flow_return_on_assets_1y_ago:
                return "Improving"
            elif abs(stock.cash_flow_return_on_assets - stock.cash_flow_return_on_assets_1y_ago) < 2:
                return "Stable"
            else:
                return "Declining"
        elif stock.cash_flow_return_on_assets > 0:
            return "Positive"
        else:
            return "Negative"
    
    def _assess_roe_trend(self, stock: QualityStock) -> str:
        """Assess ROE trend over multiple years"""
        if stock.roe > stock.roe_1y_ago > stock.roe_2y_ago and stock.roe_2y_ago > stock.roe_3y_ago:
            return "Consistently Rising"
        elif stock.roe > stock.roe_1y_ago:
            return "Rising"
        elif abs(stock.roe - stock.roe_1y_ago) < 2:
            return "Stable"
        else:
            return "Declining"
    
    def _assess_roce_consistency(self, stock: QualityStock) -> str:
        """Assess ROCE consistency using 3Y and 5Y averages"""
        if stock.roce_3y_avg > 0 and stock.roce_5y_avg > 0:
            # Check if current ROCE is close to averages (consistent)
            diff_3y = abs(stock.roce - stock.roce_3y_avg)
            diff_5y = abs(stock.roce - stock.roce_5y_avg)
            
            if diff_3y < 3 and diff_5y < 5:
                return "Very Consistent"
            elif diff_3y < 5:
                return "Consistent"
            elif stock.roce > stock.roce_3y_avg:
                return "Improving"
            else:
                return "Volatile"
        return "Insufficient Data"

