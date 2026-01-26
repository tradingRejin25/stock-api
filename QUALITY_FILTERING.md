# Quality Stock Filtering Philosophy

## Overview

The API service is designed to **only return quality stocks** and **exclude all non-significant stocks**. There are **no limits** on results - all stocks that meet quality criteria are returned.

## Filtering Strategy

### Three Quality Tiers

1. **Great Quality** - Highest standards, strictest criteria
2. **Aggressive Quality** - High growth potential with quality fundamentals
3. **Good Quality** - Balanced risk-reward, still significant quality

### What Gets Excluded

Stocks are **automatically excluded** if they have:
- Inconsistent profit growth
- Volatile margins
- Quality score below minimum thresholds
- Negative or poor growth indicators
- Missing critical quality metrics

## Quality Criteria by Tier

### Great Quality Stocks
**Strict Criteria (ALL must be met):**
- ROE > 12%
- ROCE > 15%
- Debt/Equity < 1.0
- Interest Coverage > 3
- Current Ratio > 1.2
- EPS TTM Growth > 0%
- Revenue Growth > 10%
- Quality Score ≥ 70
- At least 1 consecutive positive quarter
- Consistent profit growth (not inconsistent)
- Stable/expanding margins (not volatile)
- Valid market cap

**Result**: Only the highest quality stocks pass this filter.

### Aggressive Quality Stocks
**Growth-Focused Criteria:**
- ROE > 10%
- ROCE > 12%
- Debt/Equity < 1.5
- Interest Coverage > 2
- High growth: EPS > 15% OR Revenue > 20%
- Quality Score ≥ 60
- Consistent profit growth (not inconsistent)
- Stable margins (not volatile)
- Valid market cap

**Result**: High-growth stocks with solid fundamentals.

### Good Quality Stocks
**Balanced Criteria:**
- ROE > 8%
- ROCE > 10%
- Debt/Equity < 2.0
- Interest Coverage > 1.5
- Quality Score 55-70 (excludes great quality)
- Consistent profit growth (not inconsistent)
- Stable margins (not volatile)
- Some positive growth (EPS > -5% OR Revenue > 5%)
- Valid market cap
- **Excludes stocks already in Great or Aggressive tiers**

**Result**: Good quality stocks that don't meet great/aggressive criteria but are still significant.

## No Limits Applied

- All endpoints return **all stocks** that meet quality criteria
- No pagination or limit parameters
- Focus is on **quality over quantity**
- Non-quality stocks are filtered out at the source

## API Endpoints (Updated)

### Get All Great Quality Stocks
```
GET /api/quality-stocks/great
```
Returns all stocks meeting great quality criteria (no limit).

### Get All Aggressive Quality Stocks
```
GET /api/quality-stocks/aggressive
```
Returns all stocks meeting aggressive quality criteria (no limit).

### Get All Good Quality Stocks
```
GET /api/quality-stocks/good
```
Returns all stocks meeting good quality criteria (no limit, excludes great/aggressive).

### Get All Quality Stocks
```
GET /api/quality-stocks/all
```
Returns all quality stocks in all three tiers (no limits).

## Benefits

1. **Quality Focus**: Only significant, quality stocks are returned
2. **No Noise**: Poor quality stocks are automatically excluded
3. **Complete Data**: All quality stocks are returned (no artificial limits)
4. **Clear Tiers**: Stocks are properly categorized by quality level
5. **No Duplicates**: Stocks appear in only one tier (best fit)

## Example Response

```json
{
  "count": 25,
  "tier": "Great",
  "stocks": [
    {
      "stockName": "TCS",
      "nseCode": "TCS",
      "qualityScore": 85.2,
      "qualityTier": "Great",
      ...
    }
  ]
}
```

All returned stocks have passed strict quality filters and are considered significant for investment consideration.

