# Detailed Logic: Finding Great Quality Stocks

This document explains the comprehensive algorithm used to identify great quality stocks through the `/stocks/quality` endpoint.

## Overview

The system uses a **multi-stage filtering and weighted scoring approach** to identify stocks that meet quality investment criteria. The process involves:

1. **Hard Filters** - Eliminate stocks that don't meet minimum requirements
2. **Component Scoring** - Calculate scores for different aspects (Valuation, Profitability, Growth, Trendlyne)
3. **Weighted Combination** - Combine component scores with configurable weights
4. **Final Ranking** - Sort by overall score and return top stocks

---

## Stage 1: Hard Filters (Pre-Screening)

Before scoring, stocks must pass these mandatory filters:

### 1.1 Market Cap Filter
```python
if min_market_cap and stock.market_cap < min_market_cap:
    EXCLUDE stock
```
- **Purpose**: Filter out very small companies (optional)
- **Default**: None (no filter)

### 1.2 Valuation Filters

#### PE TTM Filter
```python
if max_pe_ttm and stock.pe_ttm > max_pe_ttm:
    EXCLUDE stock
```
- **Purpose**: Exclude overvalued stocks
- **Default**: 30
- **Logic**: PE > 30 is considered expensive

#### PE vs Sector/Industry
```python
if stock.pe_ttm / stock.sector_pe_ttm > max_pe_vs_sector:
    EXCLUDE stock
```
- **Purpose**: Exclude stocks trading at premium vs peers
- **Default**: 1.2 (120% of sector PE)
- **Logic**: Stock should not be >20% more expensive than sector average

### 1.3 Profitability Filters

#### ROE Filter
```python
if stock.roe < min_roe:
    EXCLUDE stock
```
- **Purpose**: Ensure minimum return on equity
- **Default**: 12%
- **Logic**: ROE < 12% indicates poor profitability

#### Piotroski Score Filter
```python
if stock.piotroski_score < min_piotroski:
    EXCLUDE stock
```
- **Purpose**: Ensure financial health
- **Default**: 6 (out of 9)
- **Logic**: Piotroski < 6 indicates weak financials

### 1.4 Growth Filters

#### Revenue Growth (Annual YoY)
```python
if stock.revenue_growth < min_revenue_growth:
    EXCLUDE stock
```
- **Purpose**: Ensure positive revenue growth
- **Default**: 10%
- **Logic**: Revenue should grow at least 10% annually

#### Profit Growth (Annual YoY)
```python
if stock.profit_growth < min_profit_growth:
    EXCLUDE stock
```
- **Purpose**: Ensure profit growth
- **Default**: 12%
- **Logic**: Profit should grow faster than revenue

#### Revenue Growth (Quarterly YoY)
```python
if stock.revenue_growth_qtr_yoy < min_revenue_growth_qtr:
    EXCLUDE stock
```
- **Purpose**: Ensure recent momentum
- **Default**: 8%
- **Logic**: Recent quarters should show growth

#### Growth vs Sector
```python
if stock.revenue_growth / sector_revenue_growth < min_growth_vs_sector:
    EXCLUDE stock
```
- **Purpose**: Outperform sector peers
- **Default**: 1.1 (110% of sector growth)
- **Logic**: Stock should grow at least 10% faster than sector

### 1.5 Trendlyne Score Filters

#### Durability Score
```python
if stock.trendlyne_durability_score < min_trendlyne_durability:
    EXCLUDE stock
```
- **Purpose**: Ensure business quality
- **Default**: 65 (out of 100)
- **Logic**: Durability < 65 indicates weak business model

#### Valuation Score
```python
if stock.trendlyne_valuation_score < min_trendlyne_valuation:
    EXCLUDE stock
```
- **Purpose**: Ensure fair valuation
- **Default**: 60 (out of 100)
- **Logic**: Valuation < 60 indicates overvaluation

**Note**: Momentum score is NOT filtered (low importance for quality stocks)

---

## Stage 2: Component Scoring

After passing filters, each stock gets scored in 4 components:

### 2.1 Valuation Component (15% weight)

**Purpose**: Measure if stock is reasonably priced

#### Scoring Metrics:

1. **PE Ratio** (lower is better)
   ```
   if pe_ratio <= max_pe_ratio:
       score = 1 - (pe_ratio / max_pe_ratio)
   ```
   - Example: PE=20, max=30 → score = 1 - (20/30) = 0.33

2. **PE TTM** (lower is better)
   ```
   if pe_ttm <= max_pe_ttm:
       score = 1 - (pe_ttm / max_pe_ttm)
   ```
   - Example: PE TTM=25, max=30 → score = 1 - (25/30) = 0.17

3. **PEG TTM** (lower is better, <1 is ideal)
   ```
   if peg_ttm <= max_peg_ttm:
       score = 1 - min(1.0, peg_ttm / max_peg_ttm)
   ```
   - Example: PEG=0.8, max=1.5 → score = 1 - (0.8/1.5) = 0.47

4. **PB Ratio** (lower is better)
   ```
   if pb_ratio <= max_pb_ratio:
       score = 1 - (pb_ratio / max_pb_ratio)
   ```

5. **Price to Sales** (lower is better)
   ```
   if price_to_sales <= max_price_to_sales:
       score = 1 - (price_to_sales / max_price_to_sales)
   ```

6. **%Days Below Current PE** (higher is better)
   ```
   if pct_days_below_pe <= max_pct:
       score = pct_days_below_pe / max_pct
   ```
   - Higher % = stock trading at lower valuation historically

**Final Valuation Score**: Average of all applicable metrics, normalized to 0-100

### 2.2 Profitability Component (25% weight)

**Purpose**: Measure financial health and efficiency

#### Scoring Metrics:

1. **ROE** (higher is better)
   ```
   if roe >= min_roe:
       score = min(1.0, roe / (min_roe * 2))
   ```
   - Example: ROE=18%, min=12% → score = min(1.0, 18/24) = 0.75
   - Caps at 2x minimum for fairness

2. **ROA** (higher is better)
   ```
   if roa >= min_roa:
       score = min(1.0, roa / (min_roa * 2))
   ```

3. **Profit Margin** (higher is better)
   ```
   if profit_margin >= min_margin:
       score = min(1.0, profit_margin / (min_margin * 2))
   ```

4. **Operating Margin** (higher is better)
   ```
   if operating_margin >= min_margin:
       score = min(1.0, operating_margin / (min_margin * 2))
   ```

5. **Operating Profit Margin Qtr** (higher is better)
   ```
   if op_margin_qtr >= min_margin:
       score = min(1.0, op_margin_qtr / (min_margin * 2))
   ```

6. **Piotroski Score** (0-9, higher is better)
   ```
   if piotroski >= min_piotroski:
       score = min(1.0, piotroski / 9.0)
   ```
   - Example: Piotroski=7 → score = 7/9 = 0.78

**Final Profitability Score**: Average of all applicable metrics, normalized to 0-100

### 2.3 Growth Component (25% weight)

**Purpose**: Measure growth momentum

#### Scoring Metrics:

1. **Revenue Growth Annual YoY** (higher is better)
   ```
   if revenue_growth >= min_growth:
       score = min(1.0, revenue_growth / (min_growth * 2))
   ```
   - Example: Growth=20%, min=10% → score = min(1.0, 20/20) = 1.0

2. **Profit Growth Annual YoY** (higher is better)
   ```
   if profit_growth >= min_growth:
       score = min(1.0, profit_growth / (min_growth * 2))
   ```

3. **Revenue Growth Qtr YoY** (higher is better)
   ```
   if revenue_growth_qtr >= min_growth:
       score = min(1.0, revenue_growth_qtr / (min_growth * 2))
   ```

4. **Net Profit Qtr Growth YoY** (higher is better)
   ```
   if profit_qtr_growth >= min_growth:
       score = min(1.0, profit_qtr_growth / (min_growth * 2))
   ```

5. **Revenue QoQ Growth** (higher is better)
   ```
   if revenue_qoq >= min_growth:
       score = min(1.0, revenue_qoq / (min_growth * 2))
   ```

6. **EPS TTM Growth** (higher is better)
   ```
   if eps_growth >= min_growth:
       score = min(1.0, eps_growth / (min_growth * 2))
   ```

**Final Growth Score**: Average of all applicable metrics, normalized to 0-100

### 2.4 Trendlyne Component (35% weight)

**Purpose**: Leverage Trendlyne's proprietary analysis

#### Scoring Metrics:

1. **Durability Score** (0-100, higher is better)
   ```
   if durability >= min_durability:
       score = durability / 100.0
   ```
   - Example: Durability=75 → score = 0.75

2. **Valuation Score** (0-100, higher is better)
   ```
   if valuation >= min_valuation:
       score = valuation / 100.0
   ```

3. **Momentum Score** (0-100, higher is better)
   ```
   score = momentum / 100.0
   ```
   - **Note**: Momentum is included in scoring but NOT filtered (low importance)

**Final Trendlyne Score**: Average of all 3 scores, normalized to 0-100

---

## Stage 3: Weighted Combination

### 3.1 Component Normalization

Each component score is normalized to 0-100:
```python
component_normalized = (component_score / component_max) * 100
```

### 3.2 Weighted Average

Final score combines all components with weights:

```python
final_score = (
    valuation_normalized * valuation_weight +
    profitability_normalized * profitability_weight +
    growth_normalized * growth_weight +
    trendlyne_normalized * trendlyne_weight
) / total_weight
```

### 3.3 Default Weights (Quality Focus)

For `/stocks/quality` endpoint:

- **Trendlyne**: 35% (highest - emphasizes quality scores)
- **Profitability**: 25% (high - financial health)
- **Growth**: 25% (high - growth momentum)
- **Valuation**: 15% (lower - Trendlyne covers this)

**Total**: 100%

### 3.4 Why These Weights?

1. **Trendlyne (35%)**: 
   - Comprehensive analysis from experts
   - Durability = business quality
   - Valuation = fair pricing
   - Most reliable indicator

2. **Profitability (25%)**:
   - ROE/ROA = efficiency
   - Margins = pricing power
   - Piotroski = financial health
   - Critical for long-term success

3. **Growth (25%)**:
   - Revenue growth = market expansion
   - Profit growth = efficiency improvement
   - Quarterly trends = recent momentum
   - Important for returns

4. **Valuation (15%)**:
   - Lower weight because Trendlyne Valuation Score already covers this
   - Still important to avoid overpaying
   - PE/PB ratios provide additional validation

---

## Stage 4: Final Filtering & Ranking

### 4.1 Minimum Score Filter

```python
if final_score < min_score:
    EXCLUDE stock
```
- **Default**: 70 (out of 100)
- **Purpose**: Only include stocks with overall quality score ≥ 70

### 4.2 Sorting

Stocks are sorted by:
1. **Overall Score** (descending) - Best quality first
2. If scores are equal, by market cap (descending)

### 4.3 Limiting Results

```python
return stocks[:limit]
```
- **Default**: 30 stocks
- **Purpose**: Return top N stocks

---

## Example Calculation

Let's calculate the score for a hypothetical stock:

### Stock Data:
- PE TTM: 22 (max allowed: 30)
- ROE: 18% (min required: 12%)
- Revenue Growth: 20% (min required: 10%)
- Trendlyne Durability: 75 (min required: 65)
- Trendlyne Valuation: 70 (min required: 60)
- Trendlyne Momentum: 60
- Piotroski: 7 (min required: 6)

### Component Scores:

**Valuation Component:**
- PE TTM score: 1 - (22/30) = 0.27
- Normalized: 0.27 * 100 = 27

**Profitability Component:**
- ROE score: min(1.0, 18/(12*2)) = min(1.0, 0.75) = 0.75
- Piotroski score: 7/9 = 0.78
- Average: (0.75 + 0.78) / 2 = 0.765
- Normalized: 0.765 * 100 = 76.5

**Growth Component:**
- Revenue Growth score: min(1.0, 20/(10*2)) = min(1.0, 1.0) = 1.0
- Normalized: 1.0 * 100 = 100

**Trendlyne Component:**
- Durability: 75/100 = 0.75
- Valuation: 70/100 = 0.70
- Momentum: 60/100 = 0.60
- Average: (0.75 + 0.70 + 0.60) / 3 = 0.683
- Normalized: 0.683 * 100 = 68.3

### Final Score:

```
Final Score = (27 * 0.15) + (76.5 * 0.25) + (100 * 0.25) + (68.3 * 0.35)
            = 4.05 + 19.125 + 25 + 23.905
            = 72.08
```

**Result**: Stock passes (score 72.08 ≥ 70) and is included in results.

---

## Key Design Principles

### 1. Multi-Factor Analysis
- No single metric determines quality
- Combines valuation, profitability, growth, and expert scores
- Reduces risk of false positives

### 2. Sector/Industry Comparison
- Stocks compared to peers, not absolute values
- Identifies relative outperformance
- Accounts for sector-specific characteristics

### 3. Weighted Scoring
- Configurable weights allow strategy customization
- Quality focus: Higher weight on Trendlyne & Profitability
- Growth focus: Can increase growth weight

### 4. Hard Filters First
- Eliminates clearly poor stocks early
- Reduces computation for scoring
- Ensures minimum quality standards

### 5. Normalization
- All scores normalized to 0-100 scale
- Fair comparison across different metrics
- Easy to understand and interpret

---

## Customization Options

### Adjusting Weights

You can customize weights via `/stocks/great` endpoint:

```json
{
  "trendlyne_weight": 0.4,
  "profitability_weight": 0.3,
  "growth_weight": 0.2,
  "valuation_weight": 0.1
}
```

### Adjusting Filters

Modify thresholds via query parameters:

```bash
/stocks/quality?min_trendlyne_durability=75&min_piotroski=7&min_score=75
```

### Different Strategies

- **Conservative**: Higher durability, higher Piotroski, lower growth
- **Growth**: Lower durability threshold, higher growth weight
- **Value**: Higher valuation weight, lower growth weight
- **Balanced**: Equal weights across all components

---

## Performance Considerations

1. **Filtering First**: Hard filters eliminate ~70-80% of stocks early
2. **Scoring Only Passed Stocks**: Reduces computation
3. **Normalized Scores**: Efficient comparison
4. **Caching**: Consider caching results for frequently accessed queries

---

## Limitations & Considerations

1. **Data Quality**: Results depend on Trendlyne data accuracy
2. **Historical Data**: Based on past performance, not future guarantees
3. **Market Conditions**: May not account for market cycles
4. **Sector Bias**: Some sectors may score systematically higher/lower
5. **Missing Data**: Stocks with missing metrics may score lower

---

## Conclusion

The great stocks algorithm combines:
- **Hard filters** for minimum quality
- **Component scoring** for multi-dimensional analysis
- **Weighted combination** for balanced evaluation
- **Final ranking** for best opportunities

This approach identifies stocks that are:
- ✅ Reasonably valued
- ✅ Financially healthy
- ✅ Growing consistently
- ✅ High quality (per Trendlyne analysis)
- ✅ Outperforming peers

The result is a curated list of quality investment opportunities ranked by overall score.

