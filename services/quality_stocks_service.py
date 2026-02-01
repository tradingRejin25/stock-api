"""
Quality Stocks Service - Analyzes stocks from Trendlyne CSV export
and categorizes them into Great, Aggressive, and Medium quality tiers.
"""
import csv
import os
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
    
    # Additional Quality Metrics (from CSV)
    roa_ann: float  # Return on Assets
    roa_ann_1y_ago: float
    roe_1y_ago: float  # For trend analysis
    roe_2y_ago: float
    roe_3y_ago: float
    roce_3y_avg: float  # ROCE 3-year average
    roce_5y_avg: float  # ROCE 5-year average
    cash_flow_return_on_assets: float
    cash_flow_return_on_assets_1y_ago: float
    cash_eps_ann: float
    cash_eps_ann_1y_ago: float
    cash_eps_1y_growth: float
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
    
    # SWOT Analysis
    swot_strengths: Optional[int]
    swot_weakness: Optional[int]
    swot_opportunities: Optional[int]
    swot_threats: Optional[int]
    
    # Additional Sector/Industry Metrics
    sector_roce: Optional[float]
    industry_roce: Optional[float]
    sector_roe: Optional[float]
    industry_roe: Optional[float]
    sector_peg_ttm: Optional[float]
    industry_peg_ttm: Optional[float]
    sector_net_profit_growth_qtr_qoq: Optional[float]
    sector_net_profit_growth_ann_yoy: Optional[float]
    industry_net_profit_growth_qtr_qoq: Optional[float]
    industry_net_profit_growth_ann_yoy: Optional[float]
    price_to_book_adjusted: Optional[float]
    fc_est_1q_forward_ebit_qtr: Optional[float]
    
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
    
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            # Try multiple possible paths
            possible_paths = [
                # Path relative to service file
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'filtered_stocks.csv'),
                # Absolute path (Windows)
                r'c:\Work\Trading\stock_api_service\data\filtered_stocks.csv',
                # Alternative relative path
                os.path.join('data', 'filtered_stocks.csv'),
            ]
            
            csv_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    csv_path = path
                    break
            
            if csv_path is None:
                # Use the first path as default (will show error if file not found)
                csv_path = possible_paths[0]
        
        self.csv_path = csv_path
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
        """Load and parse stocks from CSV file"""
        stocks = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        stock = QualityStock(
                            stock_name=row.get('Stock', '').strip(),
                            nse_code=row.get('NSE Code', '').strip(),
                            isin=row.get('ISIN', '').strip(),
                            market_cap=self._safe_float(row.get('Market Cap', 0)),
                            
                            # Core Quality Metrics
                            roe=self._safe_float(row.get('ROE Ann  %', 0)),
                            roce=self._safe_float(row.get('ROCE Ann  %', 0)),
                            debt_to_equity=self._safe_float(row.get('Total Debt to Total Equity Ann ', 0)),
                            interest_coverage=self._safe_float(row.get('Interest Coverage Ratio Ann ', 0)),
                            current_ratio=self._safe_float(row.get('Current Ratio Ann ', 0)),
                            promoter_holding=self._safe_float(row.get('Promoter holding latest %', 0)),
                            promoter_holding_change_1y=self._safe_float(row.get('Promoter holding change 1Y %', 0)),
                            
                            # Growth Metrics
                            eps_ttm_growth=self._safe_float(row.get('EPS TTM Growth %', 0)),
                            operating_rev_growth_ttm=self._safe_float(row.get('Operating Rev  growth TTM %', 0)),
                            net_profit_ann=self._safe_float(row.get('Net Profit Ann ', 0)),
                            net_profit_ann_1y_ago=self._safe_float(row.get('Net Profit Ann  1Y Ago', 0)),
                            opm_ann=self._safe_float(row.get('OPM Ann  %', 0)),
                            opm_ann_1y_ago=self._safe_float(row.get('OPM Ann  1Y ago %', 0)),
                            basic_eps_ttm=self._safe_float(row.get('Basic EPS TTM', 0)),
                            basic_eps_ttm_1y_ago=self._safe_float(row.get('Basic EPS TTM 1Y Ago', 0)),
                            
                            # Valuation Metrics
                            # Note: Individual stock PE TTM not in CSV, can be calculated as Market Cap / (EPS * Shares)
                            # For now, using None - can be enhanced if needed
                            pe_ttm=None,
                            industry_pe_ttm=self._safe_float(row.get('Industry PE TTM', 0)) if row.get('Industry PE TTM') else None,
                            peg_ttm=self._safe_float(row.get('PEG TTM', 0)) if row.get('PEG TTM') else None,
                            price_to_book=self._safe_float(row.get('Industry PBV TTM', 0)) if row.get('Industry PBV TTM') else None,
                            ev_per_ebitda_ann=self._safe_float(row.get('EV Per EBITDA Ann ', 0)) if row.get('EV Per EBITDA Ann ') else None,
                            
                            # Trendlyne Scores
                            durability_score=self._safe_int(row.get('Durability Score', 0)) if row.get('Durability Score') else None,
                            valuation_score=self._safe_int(row.get('Valuation Score', 0)) if row.get('Valuation Score') else None,
                            
                            # Quality Scores (Academic/Research-based)
                            piotroski_score=self._safe_int(row.get('Piotroski Score', 0)) if row.get('Piotroski Score') else None,
                            altman_zscore=self._safe_float(row.get('Altman Zscore', 0)) if row.get('Altman Zscore') else None,
                            tobin_q_ratio=self._safe_float(row.get('Tobin Q Ratio', 0)) if row.get('Tobin Q Ratio') else None,
                            graham_number=self._safe_float(row.get('Graham No ', 0)) if row.get('Graham No ') else None,
                            
                            # Additional Metrics
                            eps_qtr_yoy_growth=self._safe_float(row.get('EPS Qtr YoY Growth %', 0)),
                            basic_eps_qoq_growth=self._safe_float(row.get('Basic EPS QoQ Growth %', 0)),
                            npm_ann=self._safe_float(row.get('NPM Ann  %', 0)),
                            npm_ttm=self._safe_float(row.get('NPM TTM %', 0)),
                            
                            # Quarterly Data
                            basic_eps_qtr=self._safe_float(row.get('Basic EPS Qtr', 0)),
                            basic_eps_1q_ago=self._safe_float(row.get('Basic EPS 1Q Ago', 0)),
                            basic_eps_2q_ago=self._safe_float(row.get('Basic EPS 2Q Ago', 0)),
                            net_profit_qtr=self._safe_float(row.get('Net Profit Qtr', 0)),
                            net_profit_1q_ago=self._safe_float(row.get('Net Profit 1Q Ago', 0)),
                            net_profit_2q_ago=self._safe_float(row.get('Net Profit 2Q Ago', 0)),
                            opm_qtr=self._safe_float(row.get('Operating Profit Margin Qtr %', 0)),
                            opm_1q_ago=self._safe_float(row.get('OPM 1Q ago %', 0)),
                            opm_qtr_4q_ago=self._safe_float(row.get('OPM Qtr 4Qtr ago %', 0)),
                            
                            # Promoter Holding Trends
                            promoter_holding_change_qoq=self._safe_float(row.get('Promoter holding change QoQ %', 0)),
                            promoter_holding_change_2y=self._safe_float(row.get('Promoter holding change 2Y %', 0)),
                            
                            # Additional Valuation
                            sector_pe_ttm=self._safe_float(row.get('Sector PE TTM', 0)) if row.get('Sector PE TTM') else None,
                            sector_pbv_ttm=self._safe_float(row.get('Sector PBV TTM', 0)) if row.get('Sector PBV TTM') else None,
                            industry_pbv_ttm=self._safe_float(row.get('Industry PBV TTM', 0)) if row.get('Industry PBV TTM') else None,
                            
                            # Additional Quality Metrics
                            roa_ann=self._safe_float(row.get('RoA Ann  %', 0)),
                            roa_ann_1y_ago=self._safe_float(row.get('RoA Ann  1Y Ago %', 0)),
                            roe_1y_ago=self._safe_float(row.get('ROE Ann  1Y Ago %', 0)),
                            roe_2y_ago=self._safe_float(row.get('ROE Ann  2Y Ago %', 0)),
                            roe_3y_ago=self._safe_float(row.get('ROE Ann  3Y Ago %', 0)),
                            roce_3y_avg=self._safe_float(row.get('ROCE Ann  3Y Avg %', 0)),
                            roce_5y_avg=self._safe_float(row.get('ROCE Ann  5Y Avg %', 0)),
                            cash_flow_return_on_assets=self._safe_float(row.get('Cash Flow Return on Assets Ann ', 0)),
                            cash_flow_return_on_assets_1y_ago=self._safe_float(row.get('Cash Flow Return on Assets Ann  1Y ago', 0)),
                            cash_eps_ann=self._safe_float(row.get('Cash EPS Ann ', 0)),
                            cash_eps_ann_1y_ago=self._safe_float(row.get('Cash EPS Ann  1Y Ago', 0)),
                            cash_eps_1y_growth=self._safe_float(row.get('Cash EPS 1Y Growth %', 0)),
                            working_capital_turnover=self._safe_float(row.get('Working Capital Turnover Ann ', 0)),
                            book_value=self._safe_float(row.get('Book Value Inc Reval Reserve Ann ', 0)),
                            price_to_sales_ann=self._safe_float(row.get('Price To Sales Ann ', 0)) if row.get('Price To Sales Ann ') else None,
                            price_to_sales_ttm=self._safe_float(row.get('Price to Sales TTM', 0)) if row.get('Price to Sales TTM') else None,
                            price_to_cashflow=self._safe_float(row.get('Price to Cashflow from Operations', 0)) if row.get('Price to Cashflow from Operations') else None,
                            graham_ratio=self._safe_float(row.get('Graham Ratio', 0)) if row.get('Graham Ratio') else None,
                            operating_profit_ttm=self._safe_float(row.get('Operating Profit TTM', 0)),
                            operating_profit_ttm_1y_ago=self._safe_float(row.get('Operating Profit TTM 1Y Ago', 0)),
                            operating_profit_growth_qtr_yoy=self._safe_float(row.get('Operating Profit Growth Qtr YoY %', 0)),
                            ebitda_ann=self._safe_float(row.get('EBITDA Ann ', 0)),
                            ebitda_ttm=self._safe_float(row.get('EBITDA TTM', 0)),
                            ebitda_ann_margin=self._safe_float(row.get('EBITDA Ann  margin %', 0)),
                            ebit_ann_margin=self._safe_float(row.get('EBIT Ann  Margin %', 0)),
                            ebitda_qtr_yoy_growth=self._safe_float(row.get('EBITDA Qtr YoY Growth %', 0)),
                            promoter_pledge_percentage=self._safe_float(row.get('Promoter holding pledge percentage % Qtr', 0)),
                            gross_npa_ratio=self._safe_float(row.get('Gross NPA ratio Qtr %', 0)) if row.get('Gross NPA ratio Qtr %') else None,
                            capital_adequacy_ratio=self._safe_float(row.get('Capital Adequacy Ratios Ann  %', 0)) if row.get('Capital Adequacy Ratios Ann  %') else None,
                            industry_score=self._safe_int(row.get('Industry Score', 0)) if row.get('Industry Score') else None,
                            sector_score=self._safe_int(row.get('Sector Score', 0)) if row.get('Sector Score') else None,
                            tl_checklist_positive_score=self._safe_int(row.get('TL Checklist Positive Score', 0)) if row.get('TL Checklist Positive Score') else None,
                            tl_checklist_negative_score=self._safe_int(row.get('TL Checklist Negative Score', 0)) if row.get('TL Checklist Negative Score') else None,
                            
                            # SWOT Analysis
                            swot_strengths=self._safe_int(row.get('SWOT Strengths', 0)) if row.get('SWOT Strengths') else None,
                            swot_weakness=self._safe_int(row.get('SWOT Weakness', 0)) if row.get('SWOT Weakness') else None,
                            swot_opportunities=self._safe_int(row.get('SWOT Opportunities', 0)) if row.get('SWOT Opportunities') else None,
                            swot_threats=self._safe_int(row.get('SWOT Threats', 0)) if row.get('SWOT Threats') else None,
                            
                            # Additional Sector/Industry Metrics
                            sector_roce=self._safe_float(row.get('Sector ROCE', 0)) if row.get('Sector ROCE') else None,
                            industry_roce=self._safe_float(row.get('Industry ROCE', 0)) if row.get('Industry ROCE') else None,
                            sector_roe=self._safe_float(row.get('Sector ROE', 0)) if row.get('Sector ROE') else None,
                            industry_roe=self._safe_float(row.get('Industry ROE', 0)) if row.get('Industry ROE') else None,
                            sector_peg_ttm=self._safe_float(row.get('Sector PEG TTM', 0)) if row.get('Sector PEG TTM') else None,
                            industry_peg_ttm=self._safe_float(row.get('Industry PEG TTM', 0)) if row.get('Industry PEG TTM') else None,
                            sector_net_profit_growth_qtr_qoq=self._safe_float(row.get('Sector Net Profit Growth Qtr QoQ %', 0)) if row.get('Sector Net Profit Growth Qtr QoQ %') else None,
                            sector_net_profit_growth_ann_yoy=self._safe_float(row.get('Sector Net Profit Growth Ann  YoY %', 0)) if row.get('Sector Net Profit Growth Ann  YoY %') else None,
                            industry_net_profit_growth_qtr_qoq=self._safe_float(row.get('Industry Net Profit Growth Qtr QoQ %', 0)) if row.get('Industry Net Profit Growth Qtr QoQ %') else None,
                            industry_net_profit_growth_ann_yoy=self._safe_float(row.get('Industry Net Profit Growth Ann  YoY %', 0)) if row.get('Industry Net Profit Growth Ann  YoY %') else None,
                            price_to_book_adjusted=self._safe_float(row.get('PBV Adjusted', 0)) if row.get('PBV Adjusted') else None,
                            fc_est_1q_forward_ebit_qtr=self._safe_float(row.get('FC Est  1Q forward EBIT Qtr', 0)) if row.get('FC Est  1Q forward EBIT Qtr') else None,
                        )
                        
                        # Calculate additional insights
                        stock.cash_flow_quality = self._assess_cash_flow_quality(stock)
                        stock.roe_trend = self._assess_roe_trend(stock)
                        stock.roce_consistency = self._assess_roce_consistency(stock)
                        
                        # Calculate insights after creating stock
                        stock.consecutive_positive_quarters = self._count_consecutive_positive_quarters(stock)
                        stock.profit_growth_consistency = self._assess_profit_growth_consistency(stock)
                        stock.margin_stability = self._assess_margin_stability(stock)
                        stock.promoter_trend = self._assess_promoter_trend(stock)
                        
                        if stock.nse_code:  # Only add stocks with NSE code
                            stocks.append(stock)
                    except Exception as e:
                        print(f"Error parsing row: {e}")
                        continue
            
            self.stocks = stocks
            return stocks
        
        except FileNotFoundError:
            print(f"CSV file not found at: {self.csv_path}")
            return []
        except Exception as e:
            print(f"Error loading stocks: {e}")
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
        if stock.operating_profit_ttm > 0 and stock.operating_profit_ttm_1y_ago > 0:
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
            # Check all quality parameters - strict criteria using ALL available metrics
            meets_criteria = (
                stock.roe > 12 and
                stock.roce > 15 and
                stock.debt_to_equity < 1.0 and
                stock.interest_coverage > 3 and
                stock.current_ratio > 1.2 and
                stock.eps_ttm_growth > 0 and
                stock.operating_rev_growth_ttm > 10 and
                stock.consecutive_positive_quarters >= 1 and  # At least 1 positive quarter
                stock.profit_growth_consistency in ["Consistent", "Very Consistent", "Moderate"] and
                stock.margin_stability in ["Stable", "Expanding", "Moderately Stable"] and
                stock.quality_score >= 70 and
                stock.market_cap > 0 and  # Ensure valid market cap
                # Additional quality checks using new metrics
                stock.roa_ann > 5 and  # Good asset efficiency
                stock.cash_flow_return_on_assets > 0 and  # Positive cash flow
                stock.cash_flow_quality != "Negative" and  # Good cash flow quality
                stock.promoter_pledge_percentage < 30 and  # Low promoter pledge (risk)
                (stock.altman_zscore is None or stock.altman_zscore > 1.8)  # Not in distress zone
            )
            
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
                (stock.altman_zscore is None or stock.altman_zscore > 1.5)):  # Not in severe distress
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
                # At least some positive growth
                (stock.eps_ttm_growth > -5 or stock.operating_rev_growth_ttm > 5) and
                # Exclude high promoter pledge (risk indicator)
                stock.promoter_pledge_percentage < 50):
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

