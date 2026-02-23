"""Test script to check filtering criteria"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.quality_stocks_service import QualityStocksService

def test_filtering():
    print("=" * 60)
    print("Testing Quality Stocks Filtering")
    print("=" * 60)
    
    service = QualityStocksService()
    
    # Load stocks
    print("\n1. Loading stocks...")
    stocks = service.load_stocks()
    print(f"   Total stocks loaded: {len(stocks)}")
    
    if len(stocks) == 0:
        print("\n   ERROR: No stocks loaded!")
        print(f"   Excel path: {service.excel_path}")
        print(f"   File exists: {os.path.exists(service.excel_path)}")
        return
    
    # Calculate scores
    print("\n2. Calculating quality scores...")
    for stock in stocks:
        stock.quality_score = service.calculate_quality_score(stock)
    
    # Check criteria breakdown
    print("\n3. Checking criteria breakdown...")
    
    criteria_checks = {
        "roe > 12": 0,
        "roce > 15": 0,
        "debt_to_equity < 1.0": 0,
        "interest_coverage > 3": 0,
        "current_ratio > 1.2": 0,
        "eps_ttm_growth > 0": 0,
        "operating_rev_growth_ttm > 10": 0,
        "quality_score >= 70": 0,
        "roa_ann > 5": 0,
        "cash_flow_return_on_assets > 0": 0,
        "quick_ratio > 1.0": 0,
        "net_profit_ttm > 0": 0,
    }
    
    for stock in stocks:
        if stock.roe > 12:
            criteria_checks["roe > 12"] += 1
        if stock.roce > 15:
            criteria_checks["roce > 15"] += 1
        if stock.debt_to_equity < 1.0:
            criteria_checks["debt_to_equity < 1.0"] += 1
        if stock.interest_coverage > 3:
            criteria_checks["interest_coverage > 3"] += 1
        if stock.current_ratio > 1.2:
            criteria_checks["current_ratio > 1.2"] += 1
        if stock.eps_ttm_growth > 0:
            criteria_checks["eps_ttm_growth > 0"] += 1
        if stock.operating_rev_growth_ttm > 10:
            criteria_checks["operating_rev_growth_ttm > 10"] += 1
        if stock.quality_score >= 70:
            criteria_checks["quality_score >= 70"] += 1
        if stock.roa_ann > 5:
            criteria_checks["roa_ann > 5"] += 1
        if stock.cash_flow_return_on_assets > 0:
            criteria_checks["cash_flow_return_on_assets > 0"] += 1
        if stock.quick_ratio > 1.0:
            criteria_checks["quick_ratio > 1.0"] += 1
        if stock.net_profit_ttm > 0:
            criteria_checks["net_profit_ttm > 0"] += 1
    
    print("\n   Criteria breakdown:")
    for criterion, count in criteria_checks.items():
        percentage = (count / len(stocks)) * 100 if stocks else 0
        print(f"   {criterion:40s}: {count:4d} ({percentage:5.1f}%)")
    
    # Check how many meet ALL criteria
    print("\n4. Checking stocks meeting ALL great quality criteria...")
    great_count = 0
    for stock in stocks:
        meets_all = (
            stock.roe > 12 and
            stock.roce > 15 and
            stock.debt_to_equity < 1.0 and
            stock.interest_coverage > 3 and
            stock.current_ratio > 1.2 and
            stock.eps_ttm_growth > 0 and
            stock.operating_rev_growth_ttm > 10 and
            stock.quality_score >= 70 and
            stock.roa_ann > 5 and
            stock.cash_flow_return_on_assets > 0 and
            stock.quick_ratio > 1.0 and
            stock.net_profit_ttm > 0
        )
        if meets_all:
            great_count += 1
    
    print(f"   Stocks meeting ALL criteria: {great_count}")
    
    # Show sample stocks
    print("\n5. Sample stocks (first 5):")
    for i, stock in enumerate(stocks[:5], 1):
        print(f"\n   Stock {i}: {stock.stock_name} ({stock.nse_code})")
        print(f"      ROE: {stock.roe:.2f}%, ROCE: {stock.roce:.2f}%")
        print(f"      Debt/Equity: {stock.debt_to_equity:.2f}")
        print(f"      Interest Coverage: {stock.interest_coverage:.2f}")
        print(f"      Current Ratio: {stock.current_ratio:.2f}")
        print(f"      EPS Growth: {stock.eps_ttm_growth:.2f}%")
        print(f"      Rev Growth: {stock.operating_rev_growth_ttm:.2f}%")
        print(f"      Quality Score: {stock.quality_score:.2f}")
        print(f"      ROA: {stock.roa_ann:.2f}%")
        print(f"      Quick Ratio: {stock.quick_ratio:.2f}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_filtering()



