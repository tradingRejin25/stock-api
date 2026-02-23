"""Quick script to check if data is loading and show sample"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.quality_stocks_service import QualityStocksService

print("=" * 70)
print("Checking Stock Data Loading")
print("=" * 70)

service = QualityStocksService()
print(f"\nExcel path: {service.excel_path}")
print(f"File exists: {os.path.exists(service.excel_path)}")

print("\nLoading stocks...")
stocks = service.load_stocks()
print(f"Total stocks loaded: {len(stocks)}")

if len(stocks) == 0:
    print("\n❌ ERROR: No stocks loaded!")
    print("\nPossible issues:")
    print("1. Excel file not found")
    print("2. Excel file is empty")
    print("3. Column names don't match")
    print("4. All rows were skipped due to missing NSE codes")
else:
    print(f"\n✅ Successfully loaded {len(stocks)} stocks")
    
    # Show first 3 stocks
    print("\n" + "=" * 70)
    print("Sample Stocks (First 3):")
    print("=" * 70)
    
    for i, stock in enumerate(stocks[:3], 1):
        print(f"\n{i}. {stock.stock_name} ({stock.nse_code})")
        print(f"   ROE: {stock.roe:.2f}%")
        print(f"   ROCE: {stock.roce:.2f}%")
        print(f"   Debt/Equity: {stock.debt_to_equity:.2f}")
        print(f"   Interest Coverage: {stock.interest_coverage:.2f}")
        print(f"   Current Ratio: {stock.current_ratio:.2f}")
        print(f"   EPS Growth: {stock.eps_ttm_growth:.2f}%")
        print(f"   Rev Growth: {stock.operating_rev_growth_ttm:.2f}%")
        print(f"   Market Cap: {stock.market_cap:,.0f}")
        
        # Calculate quality score
        try:
            stock.quality_score = service.calculate_quality_score(stock)
            print(f"   Quality Score: {stock.quality_score:.2f}")
        except Exception as e:
            print(f"   Quality Score: Error - {e}")
    
    # Check how many meet great criteria
    print("\n" + "=" * 70)
    print("Checking Great Quality Criteria:")
    print("=" * 70)
    
    criteria_count = {
        "roe > 12": 0,
        "roce > 15": 0,
        "debt_to_equity < 1.0": 0,
        "interest_coverage > 3": 0,
        "current_ratio > 1.2": 0,
        "eps_ttm_growth > 0": 0,
        "operating_rev_growth_ttm > 10": 0,
        "quality_score >= 70": 0,
    }
    
    for stock in stocks:
        stock.quality_score = service.calculate_quality_score(stock)
        if stock.roe > 12:
            criteria_count["roe > 12"] += 1
        if stock.roce > 15:
            criteria_count["roce > 15"] += 1
        if stock.debt_to_equity < 1.0:
            criteria_count["debt_to_equity < 1.0"] += 1
        if stock.interest_coverage > 3:
            criteria_count["interest_coverage > 3"] += 1
        if stock.current_ratio > 1.2:
            criteria_count["current_ratio > 1.2"] += 1
        if stock.eps_ttm_growth > 0:
            criteria_count["eps_ttm_growth > 0"] += 1
        if stock.operating_rev_growth_ttm > 10:
            criteria_count["operating_rev_growth_ttm > 10"] += 1
        if stock.quality_score >= 70:
            criteria_count["quality_score >= 70"] += 1
    
    print("\nCriteria breakdown:")
    for criterion, count in criteria_count.items():
        pct = (count / len(stocks)) * 100 if stocks else 0
        print(f"  {criterion:35s}: {count:4d} ({pct:5.1f}%)")
    
    # Check how many meet ALL criteria
    great_count = 0
    for stock in stocks:
        if (stock.roe > 12 and stock.roce > 15 and stock.debt_to_equity < 1.0 and
            stock.interest_coverage > 3 and stock.current_ratio > 1.2 and
            stock.eps_ttm_growth > 0 and stock.operating_rev_growth_ttm > 10 and
            stock.quality_score >= 70):
            great_count += 1
    
    print(f"\n📊 Stocks meeting ALL core criteria: {great_count}")

print("\n" + "=" * 70)



