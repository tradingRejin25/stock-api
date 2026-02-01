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
    """Represents a stock with quality metrics - ONLY fields that exist in CSV"""
    # Basic Information (from CSV)
    stock_name: str  # 'Stock'
    nse_code: str  # 'NSE Code'
    bse_code: str  # 'BSE Code'
    isin: str  # 'ISIN'
    
    # Core Quality Metrics (from CSV)
    roe: float  # 'ROE Ann  %'
    roce: float  # 'ROCE Ann  %'
    debt_to_equity: float  # 'Total Debt to Total Equity Ann '
    interest_coverage: float  # 'Interest Coverage Ratio Ann '
    current_ratio: float  # 'Current Ratio Ann '
    current_ratio_ttm: float  # 'Current Ratio TTM'
    promoter_holding: float  # 'Promoter holding latest %'
    promoter_holding_change_qoq: float  # 'Promoter holding change QoQ %'
    
    # Growth Metrics (from CSV)
    eps_ttm_growth: float  # 'EPS TTM Growth %'
    eps_qtr_yoy_growth: float  # 'EPS Qtr YoY Growth %'
    basic_eps_qoq_growth: float  # 'Basic EPS QoQ Growth %'
    basic_eps_ttm: float  # 'Basic EPS TTM'
    net_profit_3y_growth: float  # 'Net Profit 3Y Growth %'
    net_profit_5y_growth: float  # 'Net Profit 5Y Growth %'
    net_profit_qoq_growth: float  # 'Net Profit QoQ Growth %'
    
    # Profitability Metrics (from CSV)
    opm_ann: float  # 'OPM Ann  %'
    opm_ttm: float  # 'OPM TTM %'
    npm_ttm: float  # 'NPM TTM %'
    ebitda_ann: float  # 'EBITDA Ann '
    ebitda_ttm: float  # 'EBITDA TTM'
    ebitda_ann_margin: float  # 'EBITDA Ann  Margin %'
    
    # Valuation Metrics (from CSV)
    peg_ttm: Optional[float]  # 'PEG TTM'
    price_to_book: Optional[float]  # 'Industry PBV TTM'
    price_to_book_adjusted: Optional[float]  # 'PBV Adjusted'
    ev_per_ebitda_ann: Optional[float]  # 'EV Per EBITDA Ann '
    price_to_sales_ann: Optional[float]  # 'Price To Sales Ann '
    price_to_sales_ttm: Optional[float]  # 'Price to Sales TTM'
    
    # Trendlyne Scores (from CSV)
    durability_score: Optional[int]  # 'Durability Score'
    valuation_score: Optional[int]  # 'Valuation Score'
    industry_score: Optional[int]  # 'Industry Score'
    sector_score: Optional[int]  # 'Sector Score'
    
    # Quality Scores (from CSV)
    piotroski_score: Optional[int]  # 'Piotroski Score'
    altman_zscore: Optional[float]  # 'Altman Zscore'
    
    # Promoter Metrics (from CSV)
    promoter_pledge_percentage: float  # 'Promoter holding pledge percentage % Qtr'
    
    # Sector/Industry Metrics (from CSV)
    sector_roce: Optional[float]  # 'Sector ROCE'
    industry_roce: Optional[float]  # 'Industry ROCE'
    sector_roe: Optional[float]  # 'Sector ROE'
    industry_roe: Optional[float]  # 'Industry ROE'
    sector_peg_ttm: Optional[float]  # 'Sector PEG TTM'
    industry_peg_ttm: Optional[float]  # 'Industry PEG TTM'
    sector_pbv_ttm: Optional[float]  # 'Sector PBV TTM'
    industry_pbv_ttm: Optional[float]  # 'Industry PBV TTM'
    sector_net_profit_growth_qtr_qoq: Optional[float]  # 'Sector Net Profit Growth Qtr QoQ %'
    sector_net_profit_growth_ann_yoy: Optional[float]  # 'Sector Net Profit Growth Ann  YoY %'
    industry_net_profit_growth_qtr_qoq: Optional[float]  # 'Industry Net Profit Growth Qtr QoQ %'
    industry_net_profit_growth_ann_yoy: Optional[float]  # 'Industry Net Profit Growth Ann  YoY %'
    
    # SWOT Analysis (from CSV)
    swot_strengths: Optional[int]  # 'SWOT Strengths'
    swot_weakness: Optional[int]  # 'SWOT Weakness'
    swot_opportunities: Optional[int]  # 'SWOT Opportunities'
    swot_threats: Optional[int]  # 'SWOT Threats'
    
    # Forward Estimates (from CSV)
    fc_est_1q_forward_ebit_qtr: Optional[float]  # 'FC Est  1Q forward EBIT Qtr'
    fc_est_1q_fwd_cash_eps_qtr: Optional[float]  # 'FC Est  1Q fwd Cash EPS Qtr'
    fc_est_1q_fwd_interest_expense_qtr: Optional[float]  # 'FC Est  1Q fwd Interest Expense Qtr'
    
    # Calculated/Computed Fields (NOT from CSV - these are OK to keep)
    quality_score: float = 0.0
    quality_tier: str = ""
    consecutive_positive_quarters: int = 0
    profit_growth_consistency: str = ""
    margin_stability: str = ""
    promoter_trend: str = ""
    cash_flow_quality: str = ""
    roe_trend: str = ""
    roce_consistency: str = ""


class QualityStocksService:
    """Service to analyze and filter quality stocks from CSV data"""
    
    def __init__(self, csv_path: str = None, data_folder: str = None):
        """
        Initialize the service
        
        Args:
            csv_path: Optional single CSV file path (deprecated, use data_folder instead)
            data_folder: Optional path to data folder. If not provided, looks for data folder relative to project root
        """
        # Find data folder
        if data_folder is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_folder = os.path.join(project_root, 'data')
        
        self.data_folder = data_folder
        self.csv_path = csv_path  # Keep for backward compatibility
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
    
    def _find_csv_files(self) -> List[str]:
        """Find all CSV files matching the pattern trendlyne-filtered (N).csv"""
        csv_files = []
        
        if not os.path.exists(self.data_folder):
            return csv_files
        
        import re
        pattern = re.compile(r'trendlyne-filtered\s*\((\d+)\)\.csv', re.IGNORECASE)
        
        for filename in os.listdir(self.data_folder):
            if pattern.match(filename):
                csv_files.append(os.path.join(self.data_folder, filename))
        
        # Sort by file number
        def extract_number(file_path: str) -> int:
            match = pattern.match(os.path.basename(file_path))
            return int(match.group(1)) if match else 0
        
        csv_files.sort(key=extract_number)
        return csv_files
    
    def load_stocks(self) -> List[QualityStock]:
        """Load and parse stocks from all CSV files matching trendlyne-filtered pattern"""
        stocks = []
        stocks_by_key = {}  # Use ISIN or NSE code as key to avoid duplicates
        
        # Find all CSV files
        csv_files = self._find_csv_files()
        
        if not csv_files:
            # Fallback to single file if specified
            if self.csv_path and os.path.exists(self.csv_path):
                csv_files = [self.csv_path]
            else:
                print(f"CSV files not found in: {self.data_folder}")
                return stocks
        
        print(f"Found {len(csv_files)} CSV files to load")
        
        # Load from all CSV files
        for csv_file in csv_files:
            try:
                with open(csv_file, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        try:
                            # Get durability and valuation scores - simple direct access
                            # Check exact field names first, then try variations
                            durability_score_raw = row.get('Durability Score') or row.get('Durability') or row.get('DurabilityScore')
                            if durability_score_raw is not None and str(durability_score_raw).strip() not in ['', '-', 'N/A', 'NA', 'None']:
                                durability_score = self._safe_int(durability_score_raw)
                            else:
                                durability_score = None
                            
                            valuation_score_raw = row.get('Valuation Score') or row.get('Valuation') or row.get('ValuationScore')
                            if valuation_score_raw is not None and str(valuation_score_raw).strip() not in ['', '-', 'N/A', 'NA', 'None']:
                                valuation_score = self._safe_int(valuation_score_raw)
                            else:
                                valuation_score = None
                            
                            # ONLY read fields that actually exist in CSV
                            stock = QualityStock(
                            # Basic Information
                            stock_name=row.get('Stock', '').strip(),
                            nse_code=row.get('NSE Code', '').strip(),
                            bse_code=row.get('BSE Code', '').strip(),
                            isin=row.get('ISIN', '').strip(),
                            
                            # Core Quality Metrics
                            roe=self._safe_float(row.get('ROE Ann  %', 0)),
                            roce=self._safe_float(row.get('ROCE Ann  %', 0)),
                            debt_to_equity=self._safe_float(row.get('Total Debt to Total Equity Ann ', 0)),
                            interest_coverage=self._safe_float(row.get('Interest Coverage Ratio Ann ', 0)),
                            current_ratio=self._safe_float(row.get('Current Ratio Ann ', 0)),
                            current_ratio_ttm=self._safe_float(row.get('Current Ratio TTM', 0)),
                            promoter_holding=self._safe_float(row.get('Promoter holding latest %', 0)),
                            promoter_holding_change_qoq=self._safe_float(row.get('Promoter holding change QoQ %', 0)),
                            
                            # Growth Metrics
                            eps_ttm_growth=self._safe_float(row.get('EPS TTM Growth %', 0)),
                            eps_qtr_yoy_growth=self._safe_float(row.get('EPS Qtr YoY Growth %', 0)),
                            basic_eps_qoq_growth=self._safe_float(row.get('Basic EPS QoQ Growth %', 0)),
                            basic_eps_ttm=self._safe_float(row.get('Basic EPS TTM', 0)),
                            net_profit_3y_growth=self._safe_float(row.get('Net Profit 3Y Growth %', 0)),
                            net_profit_5y_growth=self._safe_float(row.get('Net Profit 5Y Growth %', 0)),
                            net_profit_qoq_growth=self._safe_float(row.get('Net Profit QoQ Growth %', 0)),
                            
                            # Profitability Metrics
                            opm_ann=self._safe_float(row.get('OPM Ann  %', 0)),
                            opm_ttm=self._safe_float(row.get('OPM TTM %', 0)),
                            npm_ttm=self._safe_float(row.get('NPM TTM %', 0)),
                            ebitda_ann=self._safe_float(row.get('EBITDA Ann ', 0)),
                            ebitda_ttm=self._safe_float(row.get('EBITDA TTM', 0)),
                            ebitda_ann_margin=self._safe_float(row.get('EBITDA Ann  Margin %', 0)),
                            
                            # Valuation Metrics
                            peg_ttm=self._safe_float(row.get('PEG TTM', 0)) if row.get('PEG TTM') else None,
                            price_to_book=self._safe_float(row.get('Industry PBV TTM', 0)) if row.get('Industry PBV TTM') else None,
                            price_to_book_adjusted=self._safe_float(row.get('PBV Adjusted', 0)) if row.get('PBV Adjusted') else None,
                            ev_per_ebitda_ann=self._safe_float(row.get('EV Per EBITDA Ann ', 0)) if row.get('EV Per EBITDA Ann ') else None,
                            price_to_sales_ann=self._safe_float(row.get('Price To Sales Ann ', 0)) if row.get('Price To Sales Ann ') else None,
                            price_to_sales_ttm=self._safe_float(row.get('Price to Sales TTM', 0)) if row.get('Price to Sales TTM') else None,
                            
                            # Trendlyne Scores
                            durability_score=durability_score,
                            valuation_score=valuation_score,
                            industry_score=self._safe_int(row.get('Industry Score', 0)) if row.get('Industry Score') else None,
                            sector_score=self._safe_int(row.get('Sector Score', 0)) if row.get('Sector Score') else None,
                            
                            # Quality Scores
                            piotroski_score=self._safe_int(row.get('Piotroski Score', 0)) if row.get('Piotroski Score') else None,
                            altman_zscore=self._safe_float(row.get('Altman Zscore', 0)) if row.get('Altman Zscore') else None,
                            
                            # Promoter Metrics
                            promoter_pledge_percentage=self._safe_float(row.get('Promoter holding pledge percentage % Qtr', 0)),
                            
                            # Sector/Industry Metrics
                            sector_roce=self._safe_float(row.get('Sector ROCE', 0)) if row.get('Sector ROCE') else None,
                            industry_roce=self._safe_float(row.get('Industry ROCE', 0)) if row.get('Industry ROCE') else None,
                            sector_roe=self._safe_float(row.get('Sector ROE', 0)) if row.get('Sector ROE') else None,
                            industry_roe=self._safe_float(row.get('Industry ROE', 0)) if row.get('Industry ROE') else None,
                            sector_peg_ttm=self._safe_float(row.get('Sector PEG TTM', 0)) if row.get('Sector PEG TTM') else None,
                            industry_peg_ttm=self._safe_float(row.get('Industry PEG TTM', 0)) if row.get('Industry PEG TTM') else None,
                            sector_pbv_ttm=self._safe_float(row.get('Sector PBV TTM', 0)) if row.get('Sector PBV TTM') else None,
                            industry_pbv_ttm=self._safe_float(row.get('Industry PBV TTM', 0)) if row.get('Industry PBV TTM') else None,
                            sector_net_profit_growth_qtr_qoq=self._safe_float(row.get('Sector Net Profit Growth Qtr QoQ %', 0)) if row.get('Sector Net Profit Growth Qtr QoQ %') else None,
                            sector_net_profit_growth_ann_yoy=self._safe_float(row.get('Sector Net Profit Growth Ann  YoY %', 0)) if row.get('Sector Net Profit Growth Ann  YoY %') else None,
                            industry_net_profit_growth_qtr_qoq=self._safe_float(row.get('Industry Net Profit Growth Qtr QoQ %', 0)) if row.get('Industry Net Profit Growth Qtr QoQ %') else None,
                            industry_net_profit_growth_ann_yoy=self._safe_float(row.get('Industry Net Profit Growth Ann  YoY %', 0)) if row.get('Industry Net Profit Growth Ann  YoY %') else None,
                            
                            # SWOT Analysis
                            swot_strengths=self._safe_int(row.get('SWOT Strengths', 0)) if row.get('SWOT Strengths') else None,
                            swot_weakness=self._safe_int(row.get('SWOT Weakness', 0)) if row.get('SWOT Weakness') else None,
                            swot_opportunities=self._safe_int(row.get('SWOT Opportunities', 0)) if row.get('SWOT Opportunities') else None,
                            swot_threats=self._safe_int(row.get('SWOT Threats', 0)) if row.get('SWOT Threats') else None,
                            
                            # Forward Estimates
                            fc_est_1q_forward_ebit_qtr=self._safe_float(row.get('FC Est  1Q forward EBIT Qtr', 0)) if row.get('FC Est  1Q forward EBIT Qtr') else None,
                            fc_est_1q_fwd_cash_eps_qtr=self._safe_float(row.get('FC Est  1Q fwd Cash EPS Qtr', 0)) if row.get('FC Est  1Q fwd Cash EPS Qtr') else None,
                            fc_est_1q_fwd_interest_expense_qtr=self._safe_float(row.get('FC Est  1Q fwd Interest Expense Qtr', 0)) if row.get('FC Est  1Q fwd Interest Expense Qtr') else None,
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
                            
                            # Use ISIN or NSE code as unique key
                            stock_key = stock.isin if stock.isin else stock.nse_code
                            
                            if stock_key:
                                # If stock already exists, keep the one with more complete data
                                if stock_key in stocks_by_key:
                                    existing = stocks_by_key[stock_key]
                                    # Prefer stock with both durability and valuation scores
                                    if (stock.durability_score is not None and stock.valuation_score is not None and
                                        (existing.durability_score is None or existing.valuation_score is None)):
                                        stocks_by_key[stock_key] = stock
                                else:
                                    stocks_by_key[stock_key] = stock
                        except Exception as e:
                            print(f"Error parsing row in {os.path.basename(csv_file)}: {e}")
                            continue
                            
            except FileNotFoundError:
                print(f"CSV file not found: {csv_file}")
            except Exception as e:
                print(f"Error loading CSV file {os.path.basename(csv_file)}: {e}")
                continue
        
        # Convert dict values to list
        stocks = list(stocks_by_key.values())
        print(f"Loaded {len(stocks)} unique stocks from {len(csv_files)} CSV files")
        
        self.stocks = stocks
        return stocks
    
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
        # Bonus for increasing promoter holding (using QoQ change instead of 1Y)
        if stock.promoter_holding_change_qoq > 0:
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
        
        # 8. Revenue Growth - REMOVED (operating_rev_growth_ttm not in CSV)
        # Using net profit growth metrics instead
        max_score += 0
        
        # 9. Profit Growth Consistency (0-8 points) - Using 3Y and 5Y growth from CSV
        if stock.net_profit_3y_growth > 20:
            score += 8
        elif stock.net_profit_3y_growth > 10:
            score += 5
        elif stock.net_profit_3y_growth > 0:
            score += 2
        max_score += 8
        
        # 10. Operating Margin Trend (0-5 points) - Using OPM Ann only (no 1Y ago in CSV)
        if stock.opm_ann > 15:
            score += 5
        elif stock.opm_ann > 10:
            score += 3
        elif stock.opm_ann > 5:
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
        
        # 13. PE vs Industry PE - REMOVED (pe_ttm and industry_pe_ttm not in CSV)
        max_score += 0
        
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
        
        # 22. Tobin Q Ratio - REMOVED (not in CSV)
        max_score += 0
        
        # 23. Graham Number - REMOVED (not in CSV)
        max_score += 0
        
        # 24. ROA - REMOVED (not in CSV)
        max_score += 0
        
        # 25. Cash Flow Quality - Using calculated field only
        if stock.cash_flow_quality == "Improving":
            score += 1
        max_score += 1
        
        # 26. Cash EPS Growth - REMOVED (not in CSV)
        max_score += 0
        
        # 27. Working Capital Efficiency - REMOVED (not in CSV)
        max_score += 0
        
        # 28. Operating Profit TTM Growth - REMOVED (not in CSV)
        max_score += 0
        
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
        # Trendlyne Checklist Score - REMOVED (not in CSV)
        max_score += 0
        
        # 37. Bank-specific metrics - REMOVED (gross_npa_ratio and capital_adequacy_ratio not in CSV)
        max_score += 0
        
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
    
    def get_durability_valuation_stats(self) -> dict:
        """
        Get statistics about durability and valuation scores in the dataset.
        Useful for understanding score distribution before filtering.
        
        Returns:
            Dictionary with statistics about scores
        """
        if not self.stocks:
            self.load_stocks()
        
        stocks_with_durability = [s for s in self.stocks if s.durability_score is not None]
        stocks_with_valuation = [s for s in self.stocks if s.valuation_score is not None]
        stocks_with_both = [s for s in self.stocks if s.durability_score is not None and s.valuation_score is not None]
        
        stats = {
            "total_stocks": len(self.stocks),
            "stocks_with_durability_score": len(stocks_with_durability),
            "stocks_with_valuation_score": len(stocks_with_valuation),
            "stocks_with_both_scores": len(stocks_with_both),
        }
        
        if stocks_with_durability:
            durability_scores = [s.durability_score for s in stocks_with_durability]
            stats["durability"] = {
                "min": min(durability_scores),
                "max": max(durability_scores),
                "avg": round(sum(durability_scores) / len(durability_scores), 2),
                "median": sorted(durability_scores)[len(durability_scores) // 2],
            }
        else:
            stats["durability"] = None
        
        if stocks_with_valuation:
            valuation_scores = [s.valuation_score for s in stocks_with_valuation]
            stats["valuation"] = {
                "min": min(valuation_scores),
                "max": max(valuation_scores),
                "avg": round(sum(valuation_scores) / len(valuation_scores), 2),
                "median": sorted(valuation_scores)[len(valuation_scores) // 2],
            }
        else:
            stats["valuation"] = None
        
        # Count by score ranges
        if stocks_with_both:
            ranges = {
                "durability_0_20": sum(1 for s in stocks_with_both if 0 <= s.durability_score < 20),
                "durability_20_40": sum(1 for s in stocks_with_both if 20 <= s.durability_score < 40),
                "durability_40_60": sum(1 for s in stocks_with_both if 40 <= s.durability_score < 60),
                "durability_60_80": sum(1 for s in stocks_with_both if 60 <= s.durability_score < 80),
                "durability_80_100": sum(1 for s in stocks_with_both if 80 <= s.durability_score <= 100),
                "valuation_0_20": sum(1 for s in stocks_with_both if 0 <= s.valuation_score < 20),
                "valuation_20_40": sum(1 for s in stocks_with_both if 20 <= s.valuation_score < 40),
                "valuation_40_60": sum(1 for s in stocks_with_both if 40 <= s.valuation_score < 60),
                "valuation_60_80": sum(1 for s in stocks_with_both if 60 <= s.valuation_score < 80),
                "valuation_80_100": sum(1 for s in stocks_with_both if 80 <= s.valuation_score <= 100),
            }
            stats["score_ranges"] = ranges
        
        return stats
    
    def filter_by_durability_valuation(
        self, 
        min_durability: Optional[int] = None,
        max_durability: Optional[int] = None,
        min_valuation: Optional[int] = None,
        max_valuation: Optional[int] = None
    ) -> List[QualityStock]:
        """
        Filter stocks based on durability and valuation scores with flexible criteria.
        Supports both minimum and maximum thresholds for each score.
        
        Args:
            min_durability: Minimum durability score (None = no minimum)
            max_durability: Maximum durability score (None = no maximum)
            min_valuation: Minimum valuation score (None = no minimum)
            max_valuation: Maximum valuation score (None = no maximum)
        
        Returns:
            List of stocks meeting the criteria
        """
        if not self.stocks:
            self.load_stocks()
        
        # Calculate scores for all stocks
        for stock in self.stocks:
            stock.quality_score = self.calculate_quality_score(stock)
        
        # Filter based on durability and valuation scores
        filtered_stocks = []
        stocks_with_both = 0
        stocks_with_durability = 0
        stocks_with_valuation = 0
        
        for stock in self.stocks:
            # Debug: Count stocks with scores
            if stock.durability_score is not None:
                stocks_with_durability += 1
            if stock.valuation_score is not None:
                stocks_with_valuation += 1
            if stock.durability_score is not None and stock.valuation_score is not None:
                stocks_with_both += 1
            
            # Check durability score criteria
            durability_ok = True
            if stock.durability_score is None:
                durability_ok = False
            else:
                if min_durability is not None and stock.durability_score < min_durability:
                    durability_ok = False
                if max_durability is not None and stock.durability_score > max_durability:
                    durability_ok = False
            
            # Check valuation score criteria
            valuation_ok = True
            if stock.valuation_score is None:
                valuation_ok = False
            else:
                if min_valuation is not None and stock.valuation_score < min_valuation:
                    valuation_ok = False
                if max_valuation is not None and stock.valuation_score > max_valuation:
                    valuation_ok = False
            
            # Both criteria must be met
            if durability_ok and valuation_ok:
                stock.quality_tier = "High Durability & Valuation"
                filtered_stocks.append(stock)
        
        # Debug output
        print(f"Filtering Debug:")
        print(f"   Total stocks: {len(self.stocks)}")
        print(f"   Stocks with durability_score: {stocks_with_durability}")
        print(f"   Stocks with valuation_score: {stocks_with_valuation}")
        print(f"   Stocks with both scores: {stocks_with_both}")
        print(f"   Filtered stocks: {len(filtered_stocks)}")
        if filtered_stocks:
            print(f"   Sample filtered stock: {filtered_stocks[0].stock_name} (D:{filtered_stocks[0].durability_score}, V:{filtered_stocks[0].valuation_score})")
        
        # Sort by combined durability + valuation score (descending)
        filtered_stocks.sort(
            key=lambda x: (x.durability_score or 0) + (x.valuation_score or 0),
            reverse=True
        )
        return filtered_stocks
    
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

