"""
Trendlyne data loader service
Handles loading and parsing of Trendlyne data files (CSV/Excel)
"""

import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Optional
import logging

from models.stock import Stock

logger = logging.getLogger(__name__)

class TrendlyneDataLoader:
    """Loads and parses Trendlyne data files"""
    
    def __init__(self, data_file_path: Optional[str] = None):
        """
        Initialize data loader
        
        Args:
            data_file_path: Path to Trendlyne data file. If None, looks for common file names.
        """
        self.data_file_path = data_file_path
        self.stocks: List[Stock] = []
        self._data_loaded = False
        
        # Common Trendlyne file names
        self.common_file_names = [
            "trendlyne_data.csv",
            "trendlyne_data.xlsx",
            "trendlyne_export.csv",
            "trendlyne_export.xlsx",
            "stock_data.csv",
            "stock_data.xlsx"
        ]
    
    def find_data_file(self) -> Optional[str]:
        """Find Trendlyne data file in current directory or data subdirectory"""
        # Check current directory
        current_dir = Path(".")
        data_dir = Path("data")
        
        # Search in current directory
        for file_name in self.common_file_names:
            file_path = current_dir / file_name
            if file_path.exists():
                logger.info(f"Found data file: {file_path}")
                return str(file_path)
        
        # Search in data directory
        if data_dir.exists():
            for file_name in self.common_file_names:
                file_path = data_dir / file_name
                if file_path.exists():
                    logger.info(f"Found data file: {file_path}")
                    return str(file_path)
        
        return None
    
    def load_data(self, file_path: Optional[str] = None) -> List[Stock]:
        """
        Load stock data from Trendlyne file
        
        Args:
            file_path: Path to data file. If None, uses instance file_path or searches for file.
        
        Returns:
            List of Stock objects
        """
        # Determine file path
        if file_path:
            data_file = file_path
        elif self.data_file_path:
            data_file = self.data_file_path
        else:
            data_file = self.find_data_file()
        
        if not data_file or not os.path.exists(data_file):
            raise FileNotFoundError(
                f"Trendlyne data file not found. "
                f"Please place your Trendlyne export file (CSV or Excel) in the project directory "
                f"or in a 'data' subdirectory. Supported names: {', '.join(self.common_file_names)}"
            )
        
        logger.info(f"Loading data from: {data_file}")
        
        # Load based on file extension
        file_ext = Path(data_file).suffix.lower()
        
        if file_ext == '.csv':
            df = pd.read_csv(data_file)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(data_file)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: CSV, Excel")
        
        logger.info(f"Loaded {len(df)} rows from data file")
        logger.info(f"Columns ({len(df.columns)}): {list(df.columns)[:10]}...")  # Show first 10 columns
        
        # Parse DataFrame to Stock objects
        self.stocks = self._parse_dataframe(df)
        self._data_loaded = True
        
        if len(self.stocks) == 0:
            logger.warning(f"WARNING: No stocks were parsed from {len(df)} rows!")
            logger.warning("This might indicate:")
            logger.warning("1. Column names don't match expected format")
            logger.warning("2. All rows are missing required 'symbol' field")
            logger.warning("3. Data parsing errors occurred")
            logger.warning(f"First few column names: {list(df.columns)[:5]}")
        else:
            logger.info(f"Successfully parsed {len(self.stocks)} stocks")
        
        return self.stocks
    
    def _parse_dataframe(self, df: pd.DataFrame) -> List[Stock]:
        """
        Parse DataFrame to list of Stock objects
        
        Handles various column name variations from Trendlyne exports
        """
        stocks = []
        
        # Column name mapping (Trendlyne column names)
        column_mapping = {
            'symbol': ['NSE Code', 'BSE Code', 'Stock Code', 'Symbol', 'SYMBOL', 'symbol', 'Stock Symbol', 'Ticker'],
            'isin': ['ISIN', 'isin', 'Isin', 'ISIN Code'],
            'name': ['Stock Name', 'Name', 'NAME', 'name', 'Company Name', 'Company'],
            'sector': ['sector_name', 'Sector', 'SECTOR', 'sector', 'Industry Sector'],
            'industry': ['Industry Name', 'Industry', 'INDUSTRY', 'industry'],
            'market_cap': ['Market Capitalization', 'Market Cap', 'MARKET CAP', 'market_cap', 'Mkt Cap'],
            'current_price': ['Current Price', 'CURRENT PRICE', 'current_price', 'Price', 'Last Price', 'Close'],
            'pe_ratio': ['PE TTM Price to Earnings', 'PE Ratio', 'PE RATIO', 'pe_ratio', 'P/E', 'P/E Ratio', 'PE'],
            'pb_ratio': ['Price to Book Value Adjusted', 'PB Ratio', 'PB RATIO', 'pb_ratio', 'P/B', 'P/B Ratio', 'PB'],
            'dividend_yield': ['Dividend Yield', 'DIVIDEND YIELD', 'dividend_yield', 'Div Yield', 'Dividend %'],
            'roe': ['ROE Annual %', 'ROE', 'roe', 'Return on Equity', 'Return on Equity %'],
            'roa': ['RoA Annual %', 'ROA', 'roa', 'Return on Assets', 'Return on Assets %'],
            'debt_to_equity': ['Debt to Equity', 'DEBT TO EQUITY', 'debt_to_equity', 'D/E', 'Debt/Equity'],
            'current_ratio': ['Current Ratio', 'CURRENT RATIO', 'current_ratio', 'Current'],
            'quick_ratio': ['Quick Ratio', 'QUICK RATIO', 'quick_ratio', 'Quick'],
            'eps': ['Basic EPS TTM', 'EPS', 'eps', 'Earnings per Share', 'Earnings Per Share'],
            'book_value': ['Book Value', 'BOOK VALUE', 'book_value', 'BV', 'Book Value/Share'],
            'face_value': ['Face Value', 'FACE VALUE', 'face_value', 'FV'],
            'price_to_sales': ['Price to Sales', 'PRICE TO SALES', 'price_to_sales', 'P/S', 'P/S Ratio'],
            'ev_to_ebitda': ['EV/EBITDA', 'EV TO EBITDA', 'ev_to_ebitda', 'EV EBITDA'],
            'profit_margin': ['Profit Margin', 'PROFIT MARGIN', 'profit_margin', 'Net Margin', 'Net Profit Margin %'],
            'operating_margin': ['Operating Profit Margin Qtr %', 'Operating Margin', 'OPERATING MARGIN', 'operating_margin', 'OP Margin', 'Operating Margin %'],
            'revenue_growth': ['Revenue Growth Annual YoY %', 'Revenue Growth', 'REVENUE GROWTH', 'revenue_growth', 'Rev Growth', 'Revenue Growth %'],
            'profit_growth': ['Net Profit Annual YoY Growth %', 'Profit Growth', 'PROFIT GROWTH', 'profit_growth', 'Profit Growth %', 'Net Profit Growth'],
            'fii_holding': ['FII Holding', 'FII HOLDING', 'fii_holding', 'FII %', 'Foreign Institutional'],
            'dii_holding': ['DII Holding', 'DII HOLDING', 'dii_holding', 'DII %', 'Domestic Institutional'],
            'promoter_holding': ['Promoter Holding', 'PROMOTER HOLDING', 'promoter_holding', 'Promoter %', 'Promoters'],
            'public_holding': ['Public Holding', 'PUBLIC HOLDING', 'public_holding', 'Public %'],
            'week_52_high': ['52 Week High', '52W High', '52 Week H', '52W H', '52_week_high', '52 Week High', 'week_52_high'],
            'week_52_low': ['52 Week Low', '52W Low', '52 Week L', '52W L', '52_week_low', '52 Week Low', 'week_52_low'],
            
            # Trendlyne Scores
            'trendlyne_durability_score': ['Trendlyne Durability Score'],
            'trendlyne_valuation_score': ['Trendlyne Valuation Score'],
            'trendlyne_momentum_score': ['Trendlyne Momentum Score'],
            'dvm_classification': ['DVM_classification_text', 'DVM Classification Text'],
            'prev_day_durability_score': ['Prev Day Trendlyne Durability Score'],
            'prev_day_valuation_score': ['Prev Day Trendlyne Valuation Score'],
            'prev_day_momentum_score': ['Prev Day Trendlyne Momentum Score'],
            'prev_week_durability_score': ['Prev Week Trendlyne Durability Score'],
            'prev_week_valuation_score': ['Prev Week Trendlyne Valuation Score'],
            'prev_week_momentum_score': ['Prev Week Trendlyne Momentum Score'],
            'prev_month_durability_score': ['Prev Month Trendlyne Durability Score'],
            'prev_month_valuation_score': ['Prev Month Trendlyne Valuation Score'],
            'prev_month_momentum_score': ['Prev Month Trendlyne Momentum Score'],
            'normalized_momentum_score': ['Normalized Momentum Score'],
            
            # Quarterly Financials
            'operating_revenue_qtr': ['Operating Revenue Qtr'],
            'net_profit_qtr': ['Net Profit Qtr'],
            'revenue_qoq_growth': ['Revenue QoQ Growth %'],
            'revenue_growth_qtr_yoy': ['Revenue Growth Qtr YoY %'],
            'net_profit_qtr_growth_yoy': ['Net Profit Qtr Growth YoY %'],
            'net_profit_qoq_growth': ['Net Profit QoQ Growth %'],
            'operating_profit_margin_qtr': ['Operating Profit Margin Qtr %'],
            'operating_profit_margin_qtr_4q_ago': ['Operating Profit Margin Qtr 4Qtr ago %'],
            
            # TTM Financials
            'operating_revenue_ttm': ['Operating Revenue TTM'],
            'net_profit_ttm': ['Net profit TTM', 'Net Profit TTM'],
            
            # Annual Financials
            'operating_revenue_annual': ['Operating Revenue Annual'],
            'net_profit_annual': ['Net Profit Annual'],
            'revenue_growth_annual_yoy': ['Revenue Growth Annual YoY %'],
            'net_profit_annual_yoy_growth': ['Net Profit Annual YoY Growth %'],
            
            # Cash Flow
            'cash_from_financing_annual': ['Cash from Financing Annual Activity'],
            'cash_from_investing_annual': ['Cash from Investing Activity Annual'],
            'cash_from_operating_annual': ['Cash from Operating Activity Annual'],
            'net_cash_flow_annual': ['Net Cash Flow Annual'],
            
            # Sector Comparisons
            'sector_revenue_growth_qtr_yoy': ['Sector Revenue Growth Qtr YoY %'],
            'sector_net_profit_growth_qtr_yoy': ['Sector Net Profit Growth Qtr YoY %'],
            'sector_revenue_growth_qtr_qoq': ['Sector Revenue Growth Qtr QoQ %'],
            'sector_net_profit_growth_qtr_qoq': ['Sector Net Profit Growth Qtr QoQ %'],
            'sector_revenue_growth_annual_yoy': ['Sector Revenue Growth Annual YoY %'],
            'sector_pe_ttm': ['Sector PE TTM'],
            'sector_peg_ttm': ['Sector PEG TTM'],
            'sector_price_to_book_ttm': ['Sector Price to Book TTM'],
            'sector_roe': ['Sector Return on Equity ROE'],
            'sector_roa': ['Sector Return on Assets'],
            
            # Industry Comparisons
            'industry_pe_ttm': ['Industry PE TTM'],
            'industry_peg_ttm': ['Industry PEG TTM'],
            'industry_price_to_book_ttm': ['Industry Price to Book TTM'],
            'industry_roe': ['Industry Return on Equity ROE'],
            'industry_roa': ['Industry Return on Assets'],
            
            # PE Ratios
            'pe_ttm': ['PE TTM Price to Earnings'],
            'forecaster_pe_1y_forward': ['Forecaster Estimates 1Y forward PE'],
            'pe_3yr_avg': ['PE 3Yr Average'],
            'pe_5yr_avg': ['PE 5Yr Average'],
            'pct_days_below_current_pe': ['%Days traded below current PE Price to Earnings'],
            
            # PEG Ratios
            'peg_ttm': ['PEG TTM PE to Growth'],
            'forecaster_peg_1y_forward': ['Forecaster Estimates 1Y forward PEG'],
            
            # Price to Book
            'pct_days_below_current_pb': ['%Days traded below current Price to Book Value'],
            
            # EPS
            'eps_ttm_growth': ['EPS TTM Growth %'],
            
            # Piotroski Score
            'piotroski_score': ['Piotroski Score'],
            
            # Financial Results
            'latest_financial_result': ['Latest financial result', 'Latest financial result.1'],
            'result_announced_date': ['Result Announced Date', 'Result Announced Date.1'],
        }
        
        # Find actual column names in DataFrame
        actual_columns = {}
        for key, possible_names in column_mapping.items():
            for name in possible_names:
                if name in df.columns:
                    actual_columns[key] = name
                    break
        
        logger.info(f"Matched columns ({len(actual_columns)}): {actual_columns}")
        
        if len(actual_columns) == 0:
            logger.error("ERROR: No columns matched! Available columns:")
            for col in df.columns:
                logger.error(f"  - {col}")
            return []
        
        # Parse each row
        skipped_count = 0
        error_count = 0
        for idx, row in df.iterrows():
            try:
                stock_data = {}
                
                # Map columns to stock fields
                for field, col_name in actual_columns.items():
                    value = row[col_name]
                    
                    # Handle NaN and empty values
                    if pd.isna(value) or value == '' or value == '-' or value == 'N/A' or value == 'NA':
                        stock_data[field] = None
                    else:
                        # Text fields (keep as string, no conversion)
                        if field in ['symbol', 'isin', 'name', 'sector', 'industry', 'dvm_classification', 'latest_financial_result', 'result_announced_date']:
                            stock_data[field] = str(value).strip() if value else None
                        else:
                            # Numeric fields - convert to float
                            if isinstance(value, (int, float)):
                                stock_data[field] = float(value) if not pd.isna(value) else None
                            else:
                                # Try to convert string numbers
                                try:
                                    # Remove commas, percentage signs, and convert
                                    if isinstance(value, str):
                                        value_clean = value.replace(',', '').replace('%', '').strip()
                                        if value_clean and value_clean not in ['-', 'N/A', 'NA', '']:
                                            # Try to convert to float
                                            stock_data[field] = float(value_clean)
                                        else:
                                            stock_data[field] = None
                                    else:
                                        stock_data[field] = None
                                except (ValueError, AttributeError):
                                    stock_data[field] = None
                
                # Ensure symbol is present (try NSE Code, BSE Code, or Stock Code if not found)
                if 'symbol' not in stock_data or not stock_data['symbol']:
                    # Try to get symbol from other code fields
                    for code_field in ['NSE Code', 'BSE Code', 'Stock Code']:
                        if code_field in row and pd.notna(row[code_field]) and str(row[code_field]).strip():
                            stock_data['symbol'] = str(row[code_field]).strip().upper()
                            break
                    
                    if 'symbol' not in stock_data or not stock_data['symbol']:
                        skipped_count += 1
                        if skipped_count <= 3:  # Log first 3 skipped rows
                            logger.warning(f"Row {idx} missing symbol, skipping. Available code fields: NSE={row.get('NSE Code', 'N/A')}, BSE={row.get('BSE Code', 'N/A')}, Stock={row.get('Stock Code', 'N/A')}")
                        continue
                
                # Create Stock object
                stock = Stock(**stock_data)
                stocks.append(stock)
                
            except Exception as e:
                error_count += 1
                if error_count <= 3:  # Log first 3 errors
                    logger.warning(f"Error parsing row {idx}: {e}")
                continue
        
        if skipped_count > 0:
            logger.warning(f"Skipped {skipped_count} rows due to missing symbol")
        if error_count > 0:
            logger.warning(f"Encountered {error_count} parsing errors")
        
        logger.info(f"Successfully parsed {len(stocks)} stocks from {len(df)} rows")
        return stocks
    
    def get_all_stocks(self) -> List[Stock]:
        """Get all loaded stocks"""
        if not self._data_loaded:
            raise RuntimeError("Data not loaded. Call load_data() first.")
        return self.stocks
    
    def is_data_loaded(self) -> bool:
        """Check if data is loaded"""
        return self._data_loaded

