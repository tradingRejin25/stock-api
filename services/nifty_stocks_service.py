"""
Service to load and provide Nifty stocks data from CSV file
"""
import csv
import os
from typing import List, Optional
from pydantic import BaseModel


class NiftyStock(BaseModel):
    """Model for Nifty stock details"""
    stockName: str
    nseCode: str
    isin: str

    class Config:
        json_schema_extra = {
            "example": {
                "stockName": "Reliance Industries Ltd",
                "nseCode": "RELIANCE",
                "isin": "INE467B01029"
            }
        }


class NiftyStocksService:
    """Service to load and query Nifty stocks from CSV file"""
    
    def __init__(self, csv_path: Optional[str] = None):
        """Initialize the service with CSV file"""
        self._init_error = None
        self._csv_stocks: List[NiftyStock] = []
        self._csv_path = csv_path
        
        # Load from CSV
        self._load_from_csv()
        if self._csv_stocks:
            print(f"✅ Loaded {len(self._csv_stocks)} Nifty stocks from CSV")
        elif self._init_error:
            print(f"❌ Failed to load CSV: {self._init_error}")
    
    def _load_from_csv(self):
        """Load Nifty stocks from CSV file"""
        if self._csv_path is None:
            # Try multiple possible paths
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            
            possible_paths = [
                os.path.join(project_root, 'data', 'nifty_stocks.csv'),
                os.path.join('data', 'nifty_stocks.csv'),
                os.path.join(os.getcwd(), 'data', 'nifty_stocks.csv'),
            ]
            
            for path in possible_paths:
                abs_path = os.path.abspath(path)
                if os.path.exists(abs_path):
                    self._csv_path = abs_path
                    break
            
            if self._csv_path is None:
                # Use first path as default (will show error if file not found)
                self._csv_path = os.path.abspath(possible_paths[0])
        
        try:
            if not os.path.exists(self._csv_path):
                self._init_error = f"CSV file not found at: {self._csv_path}"
                return
            
            with open(self._csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                stocks_loaded = 0
                for row in reader:
                    # Handle various column name formats
                    stock_name = (row.get('Stock') or row.get('stockName') or 
                                 row.get('Stock Name') or row.get('Name') or '').strip()
                    nse_code = (row.get('NSE Code') or row.get('nseCode') or 
                               row.get('NSE') or row.get('Code') or '').strip().upper()
                    isin = (row.get('ISIN') or row.get('isin') or '').strip().upper()
                    
                    if stock_name and nse_code and isin:
                        self._csv_stocks.append(NiftyStock(
                            stockName=stock_name,
                            nseCode=nse_code,
                            isin=isin
                        ))
                        stocks_loaded += 1
                
                if stocks_loaded == 0:
                    self._init_error = f"No valid stocks found in CSV file: {self._csv_path}"
                else:
                    # Clear any previous error if loading succeeded
                    self._init_error = None
        except FileNotFoundError:
            self._init_error = f"CSV file not found at: {self._csv_path}"
        except Exception as e:
            self._init_error = f"Error loading CSV: {str(e)}"
    
    def get_all_stocks(self) -> List[NiftyStock]:
        """Get all Nifty stocks from CSV"""
        if not self._csv_stocks:
            self._load_from_csv()
        if self._csv_stocks:
            return self._csv_stocks
        error_msg = getattr(self, '_init_error', 'CSV file not available')
        raise Exception(
            f"Nifty stocks service unavailable. "
            f"CSV file is not available. "
            f"Error: {error_msg}"
        )
    
    def get_stock_by_nse_code(self, nse_code: str) -> Optional[NiftyStock]:
        """Get stock by NSE code from CSV"""
        nse_code_upper = nse_code.upper()
        
        if not self._csv_stocks:
            self._load_from_csv()
        for stock in self._csv_stocks:
            if stock.nseCode.upper() == nse_code_upper:
                return stock
        return None
    
    def get_stock_by_isin(self, isin: str) -> Optional[NiftyStock]:
        """Get stock by ISIN from CSV"""
        isin_upper = isin.upper()
        
        if not self._csv_stocks:
            self._load_from_csv()
        for stock in self._csv_stocks:
            if stock.isin.upper() == isin_upper:
                return stock
        return None
    
    def search_by_name(self, query: str) -> List[NiftyStock]:
        """Search stocks by name (case-insensitive partial match) from CSV"""
        try:
            all_stocks = self.get_all_stocks()
            query_lower = query.lower()
            return [
                s for s in all_stocks 
                if query_lower in s.stockName.lower()
            ]
        except Exception as e:
            raise Exception(f"Failed to search stocks: {str(e)}")


# Singleton instance
_nifty_stocks_service: Optional[NiftyStocksService] = None


def get_nifty_stocks_service() -> NiftyStocksService:
    """Get the singleton NiftyStocksService instance"""
    global _nifty_stocks_service
    if _nifty_stocks_service is None:
        _nifty_stocks_service = NiftyStocksService()
    return _nifty_stocks_service
