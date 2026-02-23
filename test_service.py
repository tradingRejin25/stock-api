"""
Test script for Quality Stocks Service
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from services.quality_stocks_service import QualityStocksService

def test_service():
    """Test the quality stocks service"""
    print("Testing Quality Stocks Service...")
    print("=" * 50)
    
    # Initialize service
    # Try to use the actual CSV path
    csv_path = r'c:\Work\Trading\stock_api_service\data\filtered_stocks.csv'
    if not os.path.exists(csv_path):
        csv_path = None  # Will use default path
    
    service = QualityStocksService(csv_path=csv_path)
    
    # Load stocks
    print("\n1. Loading stocks from CSV...")
    stocks = service.load_stocks()
    print(f"   Loaded {len(stocks)} stocks")
    
    if len(stocks) == 0:
        print("   ERROR: No stocks loaded. Check CSV path.")
        return
    
    # Test great quality stocks
    print("\n2. Filtering Great Quality Stocks...")
    great_stocks = service.filter_great_quality_stocks()
    print(f"   Found {len(great_stocks)} great quality stocks")
    if great_stocks:
        print(f"   Top 5:")
        for i, stock in enumerate(great_stocks[:5], 1):
            print(f"   {i}. {stock.stock_name} ({stock.nse_code}) - Score: {stock.quality_score:.2f}")
    
    # Test aggressive quality stocks
    print("\n3. Filtering Aggressive Quality Stocks...")
    aggressive_stocks = service.filter_aggressive_quality_stocks()
    print(f"   Found {len(aggressive_stocks)} aggressive quality stocks")
    if aggressive_stocks:
        print(f"   Top 5:")
        for i, stock in enumerate(aggressive_stocks[:5], 1):
            print(f"   {i}. {stock.stock_name} ({stock.nse_code}) - Score: {stock.quality_score:.2f}")
    
    # Test medium quality stocks
    print("\n4. Filtering Medium Quality Stocks...")
    medium_stocks = service.filter_medium_quality_stocks()
    print(f"   Found {len(medium_stocks)} medium quality stocks")
    if medium_stocks:
        print(f"   Top 5:")
        for i, stock in enumerate(medium_stocks[:5], 1):
            print(f"   {i}. {stock.stock_name} ({stock.nse_code}) - Score: {stock.quality_score:.2f}")
    
    # Test individual stock lookup
    if stocks:
        print("\n5. Testing individual stock lookup...")
        test_nse = stocks[0].nse_code
        stock = service.get_stock_by_nse_code(test_nse)
        if stock:
            print(f"   Found: {stock.stock_name} ({stock.nse_code})")
            print(f"   ROE: {stock.roe}%, ROCE: {stock.roce}%, Quality Score: {stock.quality_score:.2f}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_service()

