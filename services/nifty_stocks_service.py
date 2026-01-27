"""
Service to load and provide Nifty stocks data from CSV file
"""
import csv
from pathlib import Path
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
    """Service to load and query Nifty stocks from CSV"""
    
    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize the service
        
        Args:
            csv_path: Optional path to CSV file. If not provided, 
                     looks for data/nifty_stocks.csv
        """
        self.csv_path = csv_path or self._find_csv_file()
        self._cached_stocks: Optional[List[NiftyStock]] = None
    
    def _find_csv_file(self) -> Path:
        """Find the nifty_stocks.csv file"""
        # Try data folder relative to project root
        project_root = Path(__file__).parent.parent
        csv_path = project_root / "data" / "nifty_stocks.csv"
        
        if csv_path.exists():
            return csv_path
        
        # Try relative to current directory
        csv_path = Path("data") / "nifty_stocks.csv"
        if csv_path.exists():
            return csv_path
        
        raise FileNotFoundError(
            f"CSV file not found. Expected at: {project_root / 'data' / 'nifty_stocks.csv'} "
            f"or {Path('data') / 'nifty_stocks.csv'}"
        )
    
    def load_stocks(self) -> List[NiftyStock]:
        """Load and parse Nifty stocks from CSV file"""
        if self._cached_stocks is not None:
            return self._cached_stocks
        
        stocks = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Find column mappings (case-insensitive, flexible)
                headers = [h.strip().lower() for h in reader.fieldnames or []]
                fieldnames = list(reader.fieldnames)
                
                stock_name_col = None
                nse_code_col = None
                isin_col = None
                
                for i, header in enumerate(headers):
                    if stock_name_col is None and ('name' in header or 'stock' in header):
                        stock_name_col = fieldnames[i]
                    if nse_code_col is None and ('nse' in header or 'code' in header or 'symbol' in header):
                        nse_code_col = fieldnames[i]
                    if isin_col is None and 'isin' in header:
                        isin_col = fieldnames[i]
                
                if not all([stock_name_col, nse_code_col, isin_col]):
                    raise ValueError(
                        f"CSV must contain columns for stock name, NSE code, and ISIN. "
                        f"Found columns: {fieldnames}"
                    )
                
                # Read data rows
                for row in reader:
                    stock_name = row.get(stock_name_col, '').strip()
                    nse_code = row.get(nse_code_col, '').strip()
                    isin = row.get(isin_col, '').strip()
                    
                    if stock_name and nse_code and isin:
                        stocks.append(NiftyStock(
                            stockName=stock_name,
                            nseCode=nse_code,
                            isin=isin
                        ))
            
            self._cached_stocks = stocks
            return stocks
            
        except Exception as e:
            raise Exception(f"Failed to load CSV file: {str(e)}")
    
    def get_all_stocks(self) -> List[NiftyStock]:
        """Get all Nifty stocks"""
        return self.load_stocks()
    
    def get_stock_by_nse_code(self, nse_code: str) -> Optional[NiftyStock]:
        """Get stock by NSE code"""
        stocks = self.load_stocks()
        for stock in stocks:
            if stock.nseCode.upper() == nse_code.upper():
                return stock
        return None
    
    def get_stock_by_isin(self, isin: str) -> Optional[NiftyStock]:
        """Get stock by ISIN"""
        stocks = self.load_stocks()
        for stock in stocks:
            if stock.isin.upper() == isin.upper():
                return stock
        return None
    
    def search_by_name(self, query: str) -> List[NiftyStock]:
        """Search stocks by name (case-insensitive partial match)"""
        stocks = self.load_stocks()
        query_lower = query.lower()
        return [
            s for s in stocks 
            if query_lower in s.stockName.lower()
        ]
    
    def clear_cache(self):
        """Clear the cache to reload from CSV"""
        self._cached_stocks = None


# Singleton instance
_nifty_stocks_service: Optional[NiftyStocksService] = None


def get_nifty_stocks_service() -> NiftyStocksService:
    """Get the singleton NiftyStocksService instance"""
    global _nifty_stocks_service
    if _nifty_stocks_service is None:
        _nifty_stocks_service = NiftyStocksService()
    return _nifty_stocks_service



