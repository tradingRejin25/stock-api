# Trendlyne Quality Stock Filtering Criteria

## Overview

The API service now includes quality filtering that categorizes stocks into three tiers: **Great**, **Medium**, and **Good** quality based on comprehensive financial metrics.

## Quality Tiers

### Great Quality Stocks
**Strict Criteria - ALL must be met:**

| Parameter | Criteria | Why |
|-----------|----------|-----|
| ROE | > 12% | Capital efficiency |
| ROCE | > 15% | Business quality |
| Debt/Equity | < 1 | Safety |
| Interest Coverage | > 3 | Debt comfort |
| Current Ratio | > 1.2 | Liquidity |
| Promoter Holding | Stable or rising | Skin in the game |
| Quarterly EPS Growth | Positive (at least 1 quarter) | Growth momentum |
| Sales Growth | > 10-15% | Revenue growth |
| Profit Growth | Consistent | Not one-time spikes |
| Operating Margin | Stable or expanding | Margin quality |
| EPS Trend (TTM) | Rising | Earnings momentum |

**Additional Considerations:**
- Durability Score (if available) - Included in quality score
- Valuation Score (if available) - Included in quality score
- PEG Ratio: 0.7-1.5 acceptable (if positive)
- Price to Book: Sector-dependent
- EV/EBITDA: < 20 for capital-heavy stocks

**Result:** Only the highest quality stocks pass this filter.

### Medium Quality Stocks
**Flexible Criteria - Most parameters should pass:**

| Parameter | Criteria | Notes |
|-----------|----------|-------|
| ROE | > 10% | Slightly relaxed |
| ROCE | > 12% | Slightly relaxed |
| Debt/Equity | < 1.5 | Slightly relaxed |
| Interest Coverage | > 2 | Slightly relaxed |
| Current Ratio | > 1.0 | Slightly relaxed |
| Promoter Holding | Stable or rising | Same as Great |
| Growth Indicators | At least one positive | More lenient |

**Requirements:**
- At least 5 out of 6 core criteria must pass
- Must have some positive growth indicators
- Excludes stocks already in Great tier

**Result:** High-quality stocks with solid fundamentals but slightly relaxed criteria.

### Good Quality Stocks
**Balanced Criteria - More flexibility:**

| Parameter | Criteria | Notes |
|-----------|----------|-------|
| ROE | > 8% | More lenient |
| ROCE | > 10% | More lenient |
| Debt/Equity | < 2.0 | More lenient |
| Interest Coverage | > 1.5 | More lenient |
| Current Ratio | > 1.0 | More lenient |
| Promoter Holding | Stable or rising OR ROE > 6% | Very lenient |

**Requirements:**
- At least 4 out of 6 core criteria must pass
- Must have ROE > 6% OR ROCE > 8%
- Excludes stocks already in Great or Medium tiers

**Result:** Good quality stocks that don't meet higher tier criteria but are still significant.

## Quality Score Calculation

The quality score (0-100) is calculated based on:

1. **Core Quality Parameters (60 points)**
   - ROE: Up to 15 points
   - ROCE: Up to 15 points
   - Debt/Equity: Up to 10 points
   - Interest Coverage: Up to 8 points
   - Current Ratio: Up to 7 points

2. **Durability and Valuation Scores (20 points)**
   - Durability Score: Up to 10 points (if available)
   - Valuation Score: Up to 10 points (if available)

3. **Growth Indicators (20 points)**
   - EPS TTM Growth: Up to 10 points
   - Net Profit 3Y Growth: Up to 10 points

## API Endpoints

### Get All Quality Stocks
```
GET /api/trendlyne-quality
```
Query Parameters:
- `tier`: Filter by tier (great, medium, good) - optional
- `nseCode`: Filter by NSE code - optional
- `bseCode`: Filter by BSE code - optional
- `isin`: Filter by ISIN - optional
- `search`: Search by stock name - optional
- `minScore`: Minimum quality score (0-100) - optional

### Get Great Quality Stocks
```
GET /api/trendlyne-quality/great
```
Query Parameters:
- `minScore`: Minimum quality score - optional

### Get Medium Quality Stocks
```
GET /api/trendlyne-quality/medium
```
Query Parameters:
- `minScore`: Minimum quality score - optional

### Get Good Quality Stocks
```
GET /api/trendlyne-quality/good
```
Query Parameters:
- `minScore`: Minimum quality score - optional

### Get Quality Statistics
```
GET /api/trendlyne-quality/statistics
```
Returns counts for each tier.

### Get Stock by Identifier
```
GET /api/trendlyne-quality/{identifier}
```
Returns quality stock information if the stock passes quality filters.

## Example Usage

### Get all great quality stocks
```bash
curl http://localhost:8000/api/trendlyne-quality/great
```

### Get medium quality stocks with minimum score of 70
```bash
curl http://localhost:8000/api/trendlyne-quality/medium?minScore=70
```

### Search for quality stocks by name
```bash
curl http://localhost:8000/api/trendlyne-quality?search=Venus&tier=great
```

### Get quality statistics
```bash
curl http://localhost:8000/api/trendlyne-quality/statistics
```

## Response Format

Each quality stock includes:
- All original stock data
- `quality_tier`: "great", "medium", or "good"
- `quality_score`: Numerical score (0-100)
- `passed_criteria`: Object showing which criteria passed
- `source_files`: CSV files containing this stock
- `last_updated`: Timestamp of last update

## Notes

- **No Momentum Values**: Trendlyne momentum values are not considered in filtering
- **Durability & Valuation**: Included in quality score calculation if available
- **Exclusive Tiers**: Stocks are assigned to only one tier (highest applicable)
- **Automatic Updates**: When CSV files are refreshed, quality filters are automatically recalculated

## Current Statistics

Based on the loaded CSV files:
- **Great Quality**: 223 stocks (most strict - all criteria must pass)
- **Medium Quality**: 291 stocks (moderate - strong fundamentals + growth)
- **Good Quality**: 934 stocks (most lenient - any quality indicators)
- **Total Quality Stocks**: 1,448 out of 1,448 total stocks (100% coverage)

The hierarchy is: **Good > Medium > Great**, which makes logical sense as the most lenient tier should have the most stocks.

