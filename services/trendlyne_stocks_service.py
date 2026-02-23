"""
Service to load and provide Trendlyne stocks data from multiple CSV files
Scans for files matching pattern: trendlyne-filtered (N).csv
"""
import csv
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TrendlyneStock(BaseModel):
    """Model for Trendlyne stock with all available information"""
    # Core identifiers
    stock: str = Field(..., description="Stock name")
    nse_code: Optional[str] = Field(None, alias="NSE Code", description="NSE Code")
    bse_code: Optional[str] = Field(None, alias="BSE Code", description="BSE Code")
    isin: Optional[str] = Field(None, alias="ISIN", description="ISIN")
    
    # All other fields stored as dictionary
    data: Dict[str, Any] = Field(default_factory=dict, description="All other stock data fields")
    
    # Metadata
    source_files: List[str] = Field(default_factory=list, description="CSV files containing this stock")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "stock": "Venus Remedies",
                "nse_code": "VENUSREM",
                "bse_code": "526953",
                "isin": "INE411B01019",
                "data": {
                    "SWOT Weakness": "3",
                    "SWOT Threats": "0",
                    "Piotroski Score": "7",
                    "ROCE Ann  %": "10.69"
                },
                "source_files": ["trendlyne-filtered (1).csv"],
                "last_updated": "2024-01-01T00:00:00"
            }
        }


class TrendlyneStocksService:
    """Service to load and query Trendlyne stocks from multiple CSV files"""
    
    def __init__(self, data_folder: Optional[str] = None):
        """
        Initialize the service
        
        Args:
            data_folder: Optional path to data folder. If not provided, 
                        looks for data folder relative to project root
        """
        self.data_folder = self._find_data_folder(data_folder)
        self._stocks: Dict[str, TrendlyneStock] = {}  # Key: ISIN or NSE Code or BSE Code
        self._file_pattern = re.compile(r'trendlyne-filtered\s*\((\d+)\)\.csv', re.IGNORECASE)
        self._loaded_files: set = set()
    
    def _find_data_folder(self, data_folder: Optional[str]) -> Path:
        """Find the data folder"""
        if data_folder:
            folder = Path(data_folder)
            if folder.exists():
                return folder
            raise FileNotFoundError(f"Data folder not found: {data_folder}")
        
        # Try data folder relative to project root
        project_root = Path(__file__).parent.parent
        data_path = project_root / "data"
        
        if data_path.exists():
            return data_path
        
        # Try relative to current directory
        data_path = Path("data")
        if data_path.exists():
            return data_path
        
        raise FileNotFoundError(
            f"Data folder not found. Expected at: {project_root / 'data'} "
            f"or {Path('data')}"
        )
    
    def _find_csv_files(self) -> List[Path]:
        """Find all CSV files matching the pattern trendlyne-filtered (N).csv"""
        csv_files = []
        
        for file_path in self.data_folder.glob("trendlyne-filtered*.csv"):
            if self._file_pattern.match(file_path.name):
                csv_files.append(file_path)
        
        # Sort by file number
        def extract_number(file_path: Path) -> int:
            match = self._file_pattern.match(file_path.name)
            return int(match.group(1)) if match else 0
        
        csv_files.sort(key=extract_number)
        return csv_files
    
    def _get_stock_key(self, row: Dict[str, str]) -> Optional[str]:
        """Get unique key for stock (prefer ISIN, then NSE Code, then BSE Code)"""
        isin = row.get("ISIN", "").strip()
        nse_code = row.get("NSE Code", "").strip()
        bse_code = row.get("BSE Code", "").strip()
        
        if isin:
            return f"ISIN:{isin.upper()}"
        elif nse_code:
            return f"NSE:{nse_code.upper()}"
        elif bse_code:
            return f"BSE:{bse_code.upper()}"
        return None
    
    def _clean_value(self, value: Any) -> Any:
        """Clean CSV value - remove quotes, strip whitespace, handle empty values"""
        if value is None:
            return None
        value_str = str(value).strip()
        # Remove surrounding quotes if present
        if value_str.startswith('"') and value_str.endswith('"'):
            value_str = value_str[1:-1]
        if value_str == '' or value_str == '-':
            return None
        return value_str
    
    def load_all_files(self, force_reload: bool = False) -> int:
        """
        Load all CSV files matching the pattern
        
        Args:
            force_reload: If True, reload all files even if already loaded
            
        Returns:
            Number of files loaded
        """
        csv_files = self._find_csv_files()
        files_loaded = 0
        
        for file_path in csv_files:
            file_name = file_path.name
            
            # Skip if already loaded and not forcing reload
            if not force_reload and file_name in self._loaded_files:
                continue
            
            try:
                self._load_csv_file(file_path)
                self._loaded_files.add(file_name)
                files_loaded += 1
            except Exception as e:
                print(f"Warning: Failed to load {file_name}: {str(e)}")
                continue
        
        return files_loaded
    
    def _load_csv_file(self, file_path: Path):
        """Load a single CSV file and update/merge stock data"""
        file_name = file_path.name
        
        # Try utf-8-sig to handle BOM, fallback to utf-8
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                self._process_csv_rows(reader, file_name)
        except Exception:
            # Fallback to regular utf-8
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self._process_csv_rows(reader, file_name)
    
    def _process_csv_rows(self, reader: csv.DictReader, file_name: str):
        """Process rows from CSV reader"""
        # Clean fieldnames to remove BOM and quotes
        if reader.fieldnames:
            cleaned_fieldnames = []
            for field in reader.fieldnames:
                cleaned = field.strip().strip('\ufeff').strip('"').strip("'")
                cleaned_fieldnames.append(cleaned)
            reader.fieldnames = cleaned_fieldnames
        
        for row in reader:
            # Clean row keys (remove BOM, quotes, etc.)
            cleaned_row = {}
            for key, value in row.items():
                cleaned_key = key.strip().strip('\ufeff').strip('"').strip("'")
                cleaned_row[cleaned_key] = value
            
            # Get stock identifier
            stock_key = self._get_stock_key(cleaned_row)
            if not stock_key:
                continue  # Skip rows without valid identifier
            
            # Extract core fields
            stock_name = self._clean_value(cleaned_row.get("Stock", ""))
            if not stock_name:
                continue
            
            nse_code = self._clean_value(cleaned_row.get("NSE Code", ""))
            bse_code = self._clean_value(cleaned_row.get("BSE Code", ""))
            isin = self._clean_value(cleaned_row.get("ISIN", ""))
            
            # Prepare data dictionary with all other fields
            data = {}
            for key, value in cleaned_row.items():
                # Skip core fields and Sl No
                if key not in ["Stock", "NSE Code", "BSE Code", "ISIN", "Sl No"]:
                    cleaned_value = self._clean_value(value)
                    if cleaned_value is not None:
                        data[key] = cleaned_value
            
            # Check if stock already exists
            if stock_key in self._stocks:
                # Update existing stock - merge data, prefer non-empty values
                existing_stock = self._stocks[stock_key]
                
                # Update core fields if missing
                if not existing_stock.nse_code and nse_code:
                    existing_stock.nse_code = nse_code
                if not existing_stock.bse_code and bse_code:
                    existing_stock.bse_code = bse_code
                if not existing_stock.isin and isin:
                    existing_stock.isin = isin
                
                # Merge data - new values override old ones
                existing_stock.data.update(data)
                
                # Add source file if not already present
                if file_name not in existing_stock.source_files:
                    existing_stock.source_files.append(file_name)
                
                existing_stock.last_updated = datetime.now()
            else:
                # Create new stock
                new_stock = TrendlyneStock(
                    stock=stock_name,
                    nse_code=nse_code if nse_code else None,
                    bse_code=bse_code if bse_code else None,
                    isin=isin if isin else None,
                    data=data,
                    source_files=[file_name],
                    last_updated=datetime.now()
                )
                self._stocks[stock_key] = new_stock
    
    def get_all_stocks(self) -> List[TrendlyneStock]:
        """Get all stocks"""
        # Auto-load files if not loaded
        if not self._loaded_files:
            self.load_all_files()
        return list(self._stocks.values())
    
    def get_stock_by_nse_code(self, nse_code: str) -> Optional[TrendlyneStock]:
        """Get stock by NSE code"""
        stocks = self.get_all_stocks()
        nse_code_upper = nse_code.upper()
        for stock in stocks:
            if stock.nse_code and stock.nse_code.upper() == nse_code_upper:
                return stock
        return None
    
    def get_stock_by_bse_code(self, bse_code: str) -> Optional[TrendlyneStock]:
        """Get stock by BSE code"""
        stocks = self.get_all_stocks()
        bse_code_upper = bse_code.upper()
        for stock in stocks:
            if stock.bse_code and stock.bse_code.upper() == bse_code_upper:
                return stock
        return None
    
    def get_stock_by_isin(self, isin: str) -> Optional[TrendlyneStock]:
        """Get stock by ISIN"""
        stocks = self.get_all_stocks()
        isin_upper = isin.upper()
        for stock in stocks:
            if stock.isin and stock.isin.upper() == isin_upper:
                return stock
        return None
    
    def search_by_name(self, query: str) -> List[TrendlyneStock]:
        """Search stocks by name (case-insensitive partial match)"""
        stocks = self.get_all_stocks()
        query_lower = query.lower()
        return [
            s for s in stocks 
            if query_lower in s.stock.lower()
        ]
    
    def refresh_data(self) -> Dict[str, Any]:
        """
        Refresh data by reloading all CSV files
        Returns statistics about the refresh
        """
        old_count = len(self._stocks)
        files_loaded = self.load_all_files(force_reload=True)
        new_count = len(self._stocks)
        
        return {
            "files_loaded": files_loaded,
            "stocks_before": old_count,
            "stocks_after": new_count,
            "stocks_added": new_count - old_count,
            "total_files_processed": len(self._loaded_files)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded stocks and files"""
        return {
            "total_stocks": len(self._stocks),
            "loaded_files": list(self._loaded_files),
            "total_files": len(self._loaded_files),
            "data_folder": str(self.data_folder)
        }


# Singleton instance
_trendlyne_stocks_service: Optional[TrendlyneStocksService] = None


def get_trendlyne_stocks_service() -> TrendlyneStocksService:
    """Get the singleton TrendlyneStocksService instance"""
    global _trendlyne_stocks_service
    if _trendlyne_stocks_service is None:
        _trendlyne_stocks_service = TrendlyneStocksService()
        # Auto-load files on first access
        _trendlyne_stocks_service.load_all_files()
    return _trendlyne_stocks_service

