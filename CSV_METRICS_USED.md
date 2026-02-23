# CSV Metrics Used in Quality Stock Analysis

This document lists all CSV columns that are now being used in the filtering and scoring process.

## ✅ Currently Used Metrics

### Basic Information
- Stock Name
- NSE Code
- ISIN
- Market Cap

### Core Quality Metrics
- ROE Ann % (and historical: 1Y, 2Y, 3Y ago)
- ROCE Ann % (and 3Y Avg, 5Y Avg, 1Y ago)
- Total Debt to Total Equity Ann
- Interest Coverage Ratio Ann
- Current Ratio Ann
- Promoter holding latest %
- Promoter holding change (QoQ, 1Y, 2Y)
- Promoter holding pledge percentage % Qtr

### Growth Metrics
- EPS TTM Growth %
- Operating Rev growth TTM %
- Net Profit Ann (and 1Y Ago, 2Y, 3Y, 4Y, 5Y ago)
- Operating Profit TTM (and 1Y Ago)
- Operating Profit Growth Qtr YoY %
- Basic EPS TTM (and 1Y Ago)
- Basic EPS Qtr, 1Q Ago, 2Q Ago, 3Q Ago, 4Q Ago
- Basic EPS QoQ Growth %
- EPS Qtr YoY Growth %
- Net Profit Qtr, 1Q Ago, 2Q Ago

### Profitability Metrics
- OPM Ann % (and 1Y ago)
- OPM Qtr %, 1Q ago, 4Qtr ago
- OPM TTM %
- NPM Ann %
- NPM TTM %
- EBITDA Ann, TTM
- EBITDA Ann margin %
- EBITDA Qtr YoY Growth %
- EBIT Ann Margin %
- Operating Profit Margin Qtr %

### Cash Flow Metrics
- Cash Flow Return on Assets Ann (and 1Y ago)
- Cash EPS Ann (and 1Y Ago)
- Cash EPS 1Y Growth %
- Cash EPS 3Y Growth %
- Cash EPS 5Y Growth %

### Efficiency Metrics
- Working Capital Turnover Ann
- RoA Ann % (and 1Y Ago, 2Y, 3Y, 4Y, 5Y ago)

### Valuation Metrics
- Industry PE TTM
- Sector PE TTM
- PEG TTM
- Industry PBV TTM
- Sector PBV TTM
- EV Per EBITDA Ann
- Price To Sales Ann
- Price to Sales TTM
- Price to Cashflow from Operations
- Graham Ratio
- Graham No (Graham Number)

### Book Value
- Book Value Inc Reval Reserve Ann

### Quality Scores
- Piotroski Score
- Altman Zscore
- Tobin Q Ratio
- Durability Score (Trendlyne)
- Valuation Score (Trendlyne)
- Industry Score
- Sector Score
- TL Checklist Positive Score
- TL Checklist Negative Score

### Bank-Specific Metrics (for financial stocks)
- Gross NPA ratio Qtr %
- Capital Adequacy Ratios Ann %

## 📊 Enhanced Scoring with New Metrics

### Additional Scoring Components (37 total):

1-19. **Original metrics** (ROE, ROCE, Debt/Equity, etc.)

20-23. **Academic Quality Scores** (Piotroski, Altman, Tobin Q, Graham)

24. **ROA** (6 points) - Asset efficiency indicator
25. **Cash Flow Quality** (6 points) - Cash generation ability
26. **Cash EPS Growth** (4 points) - Quality earnings
27. **Working Capital Efficiency** (3 points) - Asset utilization
28. **Operating Profit TTM Growth** (4 points) - Better than annual
29. **EBITDA Quality** (5 points) - Operational efficiency
30. **Price to Sales** (3 points) - Revenue valuation
31. **Price to Cashflow** (3 points) - Cash valuation
32. **ROCE Consistency** (3 points) - Long-term consistency
33. **ROE Trend** (2 points) - Multi-year trend
34. **Promoter Pledge** (2 points) - Risk indicator
35. **Industry/Sector Performance** (3 points) - Relative performance
36. **TL Checklist** (2 points) - Quality checklist
37. **Bank Metrics** (3 points) - NPA and Capital Adequacy

**Total Scoring Points**: 163 → 220+ points (normalized to 100)

## 🎯 Enhanced Filtering Criteria

### Great Quality Stocks Now Also Check:
- ROA > 5% (asset efficiency)
- Positive cash flow return on assets
- Cash flow quality not negative
- Promoter pledge < 30% (low risk)
- Altman Z-Score > 1.8 (not in distress)

### Aggressive Quality Stocks Now Also Check:
- ROA > 3% (minimum asset efficiency)
- Positive cash flow quality
- Promoter pledge < 40%
- Altman Z-Score > 1.5 (not in severe distress)

### Good Quality Stocks Now Also Check:
- Cash flow quality not negative
- Promoter pledge < 50%

## 📈 Benefits

1. **More Comprehensive Analysis**: Uses 50+ metrics from CSV
2. **Better Quality Assessment**: Cash flow, ROA, and efficiency metrics
3. **Risk Assessment**: Promoter pledge, Altman Z-Score, NPA ratios
4. **Trend Analysis**: Multi-year ROE/ROCE trends
5. **Relative Performance**: Industry/Sector scores
6. **Bank-Specific**: NPA and Capital Adequacy for financial stocks

All useful information from the CSV is now integrated into the analysis!

