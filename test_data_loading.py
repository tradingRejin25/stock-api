"""
Test script to debug data loading issues
Run this to see detailed information about data loading
"""

import sys
import logging
from pathlib import Path

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from services.data_loader import TrendlyneDataLoader

def main():
    print("=" * 60)
    print("Trendlyne Data Loader Test")
    print("=" * 60)
    print()
    
    # Create data loader
    loader = TrendlyneDataLoader()
    
    # Try to find data file
    print("Searching for data file...")
    data_file = loader.find_data_file()
    
    if data_file:
        print(f"✓ Found data file: {data_file}")
    else:
        print("✗ Data file not found!")
        print()
        print("Please place your Trendlyne export file in one of these locations:")
        print("  - Project root directory")
        print("  - data/ subdirectory")
        print()
        print("Supported file names:")
        for name in loader.common_file_names:
            print(f"  - {name}")
        return
    
    print()
    print("Loading data...")
    print("-" * 60)
    
    try:
        stocks = loader.load_data()
        print()
        print("=" * 60)
        print(f"Results: {len(stocks)} stocks loaded")
        print("=" * 60)
        
        if len(stocks) > 0:
            print()
            print("Sample stock (first one):")
            print("-" * 60)
            sample = stocks[0]
            print(f"Symbol: {sample.symbol}")
            print(f"Name: {sample.name}")
            print(f"Sector: {sample.sector}")
            print(f"Industry: {sample.industry}")
            print(f"Market Cap: {sample.market_cap}")
            print(f"Current Price: {sample.current_price}")
            print(f"PE Ratio: {sample.pe_ratio}")
            print(f"ROE: {sample.roe}")
        else:
            print()
            print("WARNING: No stocks were loaded!")
            print("Check the logs above for details.")
            
    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR loading data:")
        print("=" * 60)
        print(str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

