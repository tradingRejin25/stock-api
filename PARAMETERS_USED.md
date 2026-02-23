# All Parameters Used in Quality Stock Analysis

This document lists all parameters from your requirements that are now integrated into the quality stocks API service.

## ✅ Core Quality Parameters (All Implemented)

### 1. ROE (Return on Equity)
- **Ideal Range**: > 12%
- **Usage**: Primary quality metric (20 points in scoring)
- **Scoring**: 
  - > 20%: 20 points
  - > 15%: 15 points
  - > 12%: 10 points
  - > 8%: 5 points

### 2. ROCE (Return on Capital Employed)
- **Ideal Range**: > 15%
- **Usage**: Business quality indicator (20 points)
- **Scoring**:
  - > 25%: 20 points
  - > 20%: 15 points
  - > 15%: 10 points
  - > 10%: 5 points

### 3. Debt/Equity Ratio
- **Ideal Range**: < 1
- **Usage**: Safety metric (15 points)
- **Scoring**:
  - 0: 15 points
  - < 0.3: 12 points
  - < 0.5: 10 points
  - < 1.0: 7 points
  - < 1.5: 3 points

### 4. Interest Coverage Ratio
- **Ideal Range**: > 3
- **Usage**: Debt comfort indicator (10 points)
- **Scoring**:
  - > 10: 10 points
  - > 5: 8 points
  - > 3: 5 points
  - > 1.5: 2 points

### 5. Current Ratio
- **Ideal Range**: > 1.2
- **Usage**: Liquidity measure (10 points)
- **Scoring**:
  - > 2.0: 10 points
  - > 1.5: 8 points
  - > 1.2: 5 points
  - > 1.0: 2 points

### 6. Promoter Holding
- **Ideal**: Stable or rising
- **Usage**: Skin in the game indicator (7 points + 3 bonus)
- **Scoring**:
  - > 50%: 5 points
  - > 30%: 3 points
  - > 20%: 1 point
  - Rising trend: +3 bonus points
  - Stable: +1 point

## ✅ Growth Parameters (All Implemented)

### 7. Quarterly EPS Growth
- **Ideal**: Positive, preferably 2 consecutive quarters
- **Usage**: Growth momentum (8 points)
- **Implementation**: 
  - Counts consecutive positive quarters
  - 2+ quarters: 8 points
  - 1 quarter: 4 points
  - QoQ growth: 2 points

### 8. Sales Growth (YoY)
- **Ideal Range**: > 10-15%
- **Usage**: Revenue growth indicator (10 points)
- **Scoring**:
  - > 20%: 10 points
  - > 15%: 8 points
  - > 10%: 5 points
  - > 5%: 2 points

### 9. Profit Growth (YoY)
- **Ideal**: Consistent, not one-time
- **Usage**: Profitability consistency (8 points + 4 bonus)
- **Implementation**:
  - Checks YoY growth
  - Analyzes quarterly consistency
  - Categorizes as: Very Consistent, Consistent, Moderate, Inconsistent
  - Bonus points for consistency

### 10. Operating Margin
- **Ideal**: Stable or expanding
- **Usage**: Margin trend analysis (5 points + 3 bonus)
- **Implementation**:
  - Compares current vs 1Y ago
  - Checks quarterly trends
  - Categorizes as: Expanding, Stable, Moderately Stable, Volatile
  - Bonus for stability/expansion

### 11. EPS Trend (TTM)
- **Ideal**: Rising
- **Usage**: Earnings momentum (10 points)
- **Scoring**: Based on EPS TTM Growth %

## ✅ Valuation Parameters (All Implemented)

### 12. PEG Ratio
- **Ideal Range**: 0.7-1.5 (if positive)
- **Usage**: Growth-adjusted valuation (5 points)
- **Implementation**:
  - Only used if positive (ignores negative)
  - 0.7-1.5: 5 points
  - 0.5-2.0: 3 points
  - < 0.5: 1 point

### 13. PE vs Industry PE
- **Ideal**: Lower or similar
- **Usage**: Relative valuation (5 points)
- **Implementation**:
  - Compares stock PE to industry PE
  - Lower (< 0.9x): 5 points
  - Similar (0.9-1.1x): 3 points
  - Slightly higher (1.1-1.3x): 1 point
  - Falls back to sector PE if industry PE unavailable

### 14. Price to Book
- **Ideal**: Depends on sector (lower generally better)
- **Usage**: Asset valuation (5 points)
- **Implementation**:
  - < 1.0: 5 points (undervalued)
  - < 2.0: 3 points
  - < 3.0: 1 point
  - Also compares to industry average

### 15. EV/EBITDA
- **Ideal**: Lower is better (especially for capital-heavy stocks)
- **Usage**: Enterprise value analysis (5 points)
- **Implementation**:
  - < 8: 5 points (very attractive)
  - < 12: 3 points (reasonable)
  - < 15: 1 point (acceptable)

## ✅ Trendlyne Scores (Implemented)

### 16. Durability Score
- **Usage**: Business durability (7 points max)
- **Scoring**: Score / 2 (capped at 7)

### 17. Valuation Score
- **Usage**: Valuation attractiveness (7 points max)
- **Scoring**: Score / 2 (capped at 7)

## ✅ Academic/Research-Based Quality Scores (All Implemented)

### 18. Piotroski Score (F-Score)
- **Usage**: Fundamental strength indicator (9 points max)
- **Range**: 0-9 (higher is better)
- **Scoring**: Direct use of score (max 9 points)
- **What it measures**: 9 fundamental criteria including profitability, leverage, liquidity, and operating efficiency

### 19. Altman Z-Score
- **Usage**: Financial distress predictor (6 points max)
- **Scoring**:
  - > 3.0 (Safe zone): 6 points
  - > 2.7 (Grey zone - safe): 4 points
  - > 1.8 (Grey zone - caution): 2 points
  - < 1.8 (Distress zone): 0 points
- **What it measures**: Probability of bankruptcy using financial ratios

### 20. Tobin Q Ratio
- **Usage**: Market vs Book value indicator (5 points max)
- **Scoring**:
  - 0.8-1.2 (Fairly valued): 5 points
  - 0.6-0.8 (Undervalued): 4 points
  - 1.2-1.5 (Slightly overvalued): 2 points
  - > 1.5 (Overvalued): 1 point
- **What it measures**: Market value relative to replacement cost

### 21. Graham Number
- **Usage**: Intrinsic value indicator (4 points max)
- **Scoring**: 
  - Base points for presence: 2 points
  - Additional if suggests reasonable valuation: +2 points
- **What it measures**: Maximum price to pay based on earnings and book value

## 📊 Enhanced Insights (Calculated)

The service now provides additional calculated insights:

1. **Consecutive Positive Quarters**: Count of consecutive quarters with positive EPS growth
2. **Profit Growth Consistency**: Assessment of whether growth is consistent or one-time
3. **Margin Stability**: Analysis of operating margin trends (Expanding/Stable/Volatile)
4. **Promoter Trend**: Analysis of promoter holding changes (Rising/Stable/Declining)

## 🎯 Quality Tiers

### Great Quality Stocks
- **Criteria**: All core parameters met + Quality Score ≥ 70
- **Additional**: At least 1 positive quarter, consistent profit growth, stable/expanding margins

### Aggressive Quality Stocks
- **Criteria**: Slightly relaxed parameters + Quality Score ≥ 60
- **Focus**: High growth potential (EPS > 15% or Revenue > 20%)

### Medium Quality Stocks
- **Criteria**: Balanced parameters + Quality Score 50-70
- **Focus**: Moderate risk-reward profile

## ✅ Additional Quality Metrics (Newly Added)

### 24. ROA (Return on Assets)
- **Usage**: Asset efficiency indicator (6 points)
- **Scoring**: > 10%: 5 points, > 7%: 4 points, > 5%: 3 points, > 3%: 1 point
- **Bonus**: +1 point for improving ROA

### 25. Cash Flow Return on Assets
- **Usage**: Cash generation quality (6 points)
- **Scoring**: > 10%: 5 points, > 7%: 4 points, > 5%: 3 points, > 0%: 1 point
- **Bonus**: +1 point for improving cash flow

### 26. Cash EPS Growth
- **Usage**: Quality earnings indicator (4 points)
- **Scoring**: > 20%: 4 points, > 10%: 3 points, > 5%: 2 points, > 0%: 1 point

### 27. Working Capital Turnover
- **Usage**: Asset utilization efficiency (3 points)
- **Scoring**: > 10: 3 points, > 5: 2 points, > 2: 1 point

### 28. Operating Profit TTM Growth
- **Usage**: Better growth metric than annual (4 points)
- **Scoring**: Based on TTM vs 1Y ago comparison

### 29. EBITDA Quality
- **Usage**: Operational efficiency (5 points)
- **Scoring**: Margin > 25%: 4 points, > 20%: 3 points, > 15%: 2 points, > 10%: 1 point
- **Bonus**: +1 point for EBITDA growth > 15%

### 30. Price to Sales
- **Usage**: Revenue-based valuation (3 points)
- **Scoring**: < 1.0: 3 points, < 2.0: 2 points, < 3.0: 1 point

### 31. Price to Cashflow
- **Usage**: Cash-based valuation (3 points)
- **Scoring**: < 10: 3 points, < 15: 2 points, < 20: 1 point

### 32. ROCE Consistency
- **Usage**: Long-term consistency using 3Y/5Y averages (3 points)
- **Scoring**: Very Consistent: 3 points, Consistent: 2 points, Improving: 1 point

### 33. ROE Trend
- **Usage**: Multi-year ROE trend analysis (2 points)
- **Scoring**: Consistently Rising: 2 points, Rising: 1 point

### 34. Promoter Pledge
- **Usage**: Risk indicator (2 points)
- **Scoring**: 0%: 2 points, < 10%: 1 point (lower is better)

### 35. Industry/Sector Scores
- **Usage**: Relative performance indicators (3 points)
- **Scoring**: Based on Industry Score and Sector Score

### 36. TL Checklist
- **Usage**: Quality checklist (2 points)
- **Scoring**: Net positive score > 10: 2 points, > 5: 1 point

### 37. Bank-Specific Metrics
- **Usage**: For financial stocks (3 points)
- **NPA Ratio**: < 1%: 2 points, < 2%: 1 point
- **Capital Adequacy**: > 15%: 1 point

## 📈 Total Scoring System

The quality score (0-100) is calculated from:
- Core Quality Metrics: 82 points
- Growth Metrics: 28 points
- Valuation Metrics: 15 points
- Trendlyne Scores: 14 points (Durability + Valuation)
- Academic Quality Scores: 24 points (Piotroski + Altman + Tobin Q + Graham)
- **Additional Quality Metrics**: 57 points (ROA, Cash Flow, Working Capital, EBITDA, etc.)
- **Total**: 220+ points (normalized to 100)

**Note**: Momentum Score has been removed as requested. Replaced with academic/research-based quality scores and additional fundamental metrics from CSV for more comprehensive analysis.

All parameters you mentioned are now fully integrated and used in the analysis!

