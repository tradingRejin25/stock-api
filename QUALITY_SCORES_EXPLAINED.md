# Quality Scores Explained

This document explains the academic and research-based quality scores used in the stock analysis.

## Piotroski F-Score

**What it is**: A fundamental analysis score (0-9) developed by Joseph Piotroski to identify high-quality value stocks.

**How it works**: Evaluates 9 fundamental criteria:
1. Positive net income
2. Positive return on assets (ROA)
3. Positive operating cash flow
4. Cash flow from operations > net income
5. Lower long-term debt in current year
6. Higher current ratio
7. No new shares issued
8. Higher gross margin
9. Higher asset turnover

**Interpretation**:
- **8-9**: Excellent fundamentals
- **6-7**: Good fundamentals
- **4-5**: Average fundamentals
- **0-3**: Weak fundamentals

**In our scoring**: Direct use (0-9 points)

## Altman Z-Score

**What it is**: A bankruptcy prediction model developed by Edward Altman using multiple financial ratios.

**Formula**: Combines profitability, leverage, liquidity, solvency, and activity ratios.

**Interpretation**:
- **> 3.0**: Safe zone (low bankruptcy risk)
- **2.7 - 3.0**: Grey zone (safe side)
- **1.8 - 2.7**: Grey zone (caution)
- **< 1.8**: Distress zone (high bankruptcy risk)

**In our scoring**: 
- Safe zone: 6 points
- Grey zone (safe): 4 points
- Grey zone (caution): 2 points
- Distress: 0 points

## Tobin Q Ratio

**What it is**: Market value of a company relative to its replacement cost (book value).

**Formula**: Market Value / Replacement Cost

**Interpretation**:
- **0.6 - 0.8**: Undervalued (good buying opportunity)
- **0.8 - 1.2**: Fairly valued
- **1.2 - 1.5**: Slightly overvalued
- **> 1.5**: Overvalued
- **< 0.6**: May indicate distress or very undervalued

**In our scoring**:
- Fairly valued: 5 points
- Undervalued: 4 points
- Slightly overvalued: 2 points
- Overvalued: 1 point

## Graham Number

**What it is**: An intrinsic value calculation developed by Benjamin Graham (Warren Buffett's mentor).

**Formula**: √(22.5 × EPS × Book Value per Share)

**Interpretation**: 
- Represents the maximum price an investor should pay for a stock
- If current price < Graham Number: Potentially undervalued
- If current price > Graham Number: Potentially overvalued

**In our scoring**: 
- Base points for presence: 2 points
- Additional if suggests reasonable valuation: +2 points

## Why These Scores Matter

These scores provide:
1. **Fundamental Strength**: Piotroski F-Score
2. **Financial Health**: Altman Z-Score
3. **Valuation Perspective**: Tobin Q Ratio
4. **Intrinsic Value**: Graham Number

Together, they offer a comprehensive view of a company's quality beyond just financial ratios.

## Comparison to Momentum Score

**Removed**: Trendlyne Momentum Score (price/performance based)
**Added**: Academic quality scores (fundamental analysis based)

**Reason**: Fundamental quality scores are more reliable for long-term investment decisions as they focus on business fundamentals rather than short-term price movements.

