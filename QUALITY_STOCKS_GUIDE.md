# Quality Stocks API Guide

The `/stocks/quality` endpoint is optimized for finding high-quality stocks with emphasis on:
- **Trendlyne Scores** (Durability & Valuation, low momentum importance)
- **Piotroski Score** (Financial health indicator)
- **Growth Metrics** (Revenue & Profit growth)
- **Sector/Industry Comparison** (Outperforming peers)

## Default Configuration

The endpoint uses optimized weights:
- **Trendlyne Scores**: 35% weight (Durability + Valuation, momentum excluded)
- **Profitability**: 25% weight (includes Piotroski Score)
- **Growth**: 25% weight (Revenue & Profit growth)
- **Valuation**: 15% weight (PE ratios, sector comparisons)

## Basic Usage

### Simple Request (Default Criteria)
```bash
curl "http://localhost:8000/stocks/quality?limit=30"
```

This uses default thresholds:
- Trendlyne Durability ≥ 65
- Trendlyne Valuation ≥ 60
- Piotroski Score ≥ 6
- Revenue Growth ≥ 10%
- Profit Growth ≥ 12%
- Revenue Growth Qtr ≥ 8%
- PE vs Sector ≤ 120%
- PE vs Industry ≤ 120%
- Growth vs Sector ≥ 110%
- ROE ≥ 12%
- PE TTM ≤ 30
- Overall Score ≥ 70

### Customized Request
```bash
curl "http://localhost:8000/stocks/quality?min_trendlyne_durability=75&min_piotroski=7&min_revenue_growth=15&limit=20"
```

## Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_trendlyne_durability` | 65 | Minimum Trendlyne Durability Score (0-100) |
| `min_trendlyne_valuation` | 60 | Minimum Trendlyne Valuation Score (0-100) |
| `min_piotroski` | 6 | Minimum Piotroski Score (0-9, higher = better) |
| `min_revenue_growth` | 10 | Minimum Revenue Growth Annual YoY % |
| `min_profit_growth` | 12 | Minimum Profit Growth Annual YoY % |
| `min_revenue_growth_qtr` | 8 | Minimum Revenue Growth Qtr YoY % |
| `max_pe_vs_sector` | 1.2 | Maximum PE vs Sector (1.2 = 120% of sector PE) |
| `max_pe_vs_industry` | 1.2 | Maximum PE vs Industry (1.2 = 120% of industry PE) |
| `min_growth_vs_sector` | 1.1 | Minimum Growth vs Sector (1.1 = 110% of sector growth) |
| `min_market_cap` | None | Minimum market cap (optional) |
| `max_pe_ttm` | 30 | Maximum PE TTM |
| `min_roe` | 12 | Minimum ROE % |
| `min_score` | 70 | Minimum overall quality score (0-100) |
| `limit` | 30 | Maximum number of results |

## Example Use Cases

### 1. Conservative Quality Stocks
High durability, strong financials, moderate growth:
```bash
curl "http://localhost:8000/stocks/quality?min_trendlyne_durability=80&min_piotroski=7&min_revenue_growth=8&min_roe=15&limit=20"
```

### 2. Growth-Oriented Quality Stocks
Strong growth with quality fundamentals:
```bash
curl "http://localhost:8000/stocks/quality?min_revenue_growth=20&min_profit_growth=25&min_revenue_growth_qtr=15&min_trendlyne_durability=70&limit=25"
```

### 3. Undervalued Quality Stocks
Quality stocks trading at reasonable valuations:
```bash
curl "http://localhost:8000/stocks/quality?max_pe_ttm=20&max_pe_vs_sector=0.9&max_pe_vs_industry=0.9&min_trendlyne_valuation=70&limit=20"
```

### 4. Sector Outperformers
Quality stocks outperforming their sector:
```bash
curl "http://localhost:8000/stocks/quality?min_growth_vs_sector=1.3&max_pe_vs_sector=1.0&min_trendlyne_durability=70&limit=25"
```

### 5. High Piotroski Quality Stocks
Focus on financial health:
```bash
curl "http://localhost:8000/stocks/quality?min_piotroski=8&min_trendlyne_durability=75&min_roe=18&limit=15"
```

## Understanding the Scores

### Trendlyne Durability Score (0-100)
- Measures business quality, sustainability, and competitive advantages
- Higher score = more durable business model
- **Recommended**: ≥ 65 for quality stocks, ≥ 75 for high quality

### Trendlyne Valuation Score (0-100)
- Measures if stock is fairly valued or undervalued
- Higher score = better value proposition
- **Recommended**: ≥ 60 for quality stocks, ≥ 70 for high quality

### Piotroski Score (0-9)
- 9-point financial health check
- 7-9: Excellent financial health
- 5-6: Good financial health
- <5: Average or poor
- **Recommended**: ≥ 6 for quality stocks, ≥ 7 for high quality

### Growth Metrics
- **Annual YoY**: Year-over-year growth (long-term trend)
- **Qtr YoY**: Quarterly year-over-year growth (recent momentum)
- **vs Sector**: How stock growth compares to sector average

### Sector/Industry Comparison
- **PE vs Sector/Industry**: Stock's PE relative to sector/industry
  - < 1.0 = Trading at discount to peers
  - 1.0-1.2 = Trading in line with peers
  - > 1.2 = Trading at premium
- **Growth vs Sector**: Stock's growth relative to sector
  - > 1.0 = Outperforming sector
  - < 1.0 = Underperforming sector

## Response Format

The API returns a list of Stock objects sorted by quality score (highest first). Each stock includes:
- All basic stock information
- Trendlyne scores (Durability, Valuation, Momentum)
- Financial metrics (ROE, ROA, margins, etc.)
- Growth metrics (Annual, Quarterly, QoQ)
- Sector/Industry comparisons
- Piotroski Score
- And all other available fields

## Tips for Best Results

1. **Start with defaults**: The default criteria are well-balanced
2. **Adjust gradually**: Change one parameter at a time to see impact
3. **Focus on durability**: Higher durability scores = more sustainable businesses
4. **Check Piotroski**: High score (7+) indicates strong financials
5. **Compare to sector**: Stocks outperforming peers are often better investments
6. **Balance growth & quality**: Don't sacrifice quality for high growth
7. **Review multiple metrics**: No single metric tells the whole story

## Comparison with `/stocks/great`

| Feature | `/stocks/quality` | `/stocks/great` |
|---------|-------------------|-----------------|
| **Purpose** | Quality-focused stocks | Fully customizable |
| **Weights** | Pre-optimized for quality | User-configurable |
| **Trendlyne Momentum** | Low importance | User-configurable |
| **Ease of Use** | Simple query parameters | Requires JSON body |
| **Flexibility** | Limited to quality focus | Unlimited customization |

Use `/stocks/quality` for quick quality stock screening.
Use `/stocks/great` for custom strategies and advanced filtering.

