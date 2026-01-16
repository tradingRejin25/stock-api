# Examples: Finding Great Stocks with Trendlyne Scores

This guide shows you how to utilize all the Trendlyne scores and comprehensive metrics to find great stocks.

## Basic Example: Using Trendlyne Scores

```json
{
  "min_trendlyne_durability_score": 70,
  "min_trendlyne_valuation_score": 60,
  "min_trendlyne_momentum_score": 50,
  "min_score": 65,
  "limit": 20,
  "sort_by": "trendlyne_durability_score"
}
```

## Comprehensive Example: Value + Growth + Quality

```json
{
  "min_market_cap": 1000,
  "max_pe_ttm": 25,
  "max_peg_ttm": 1.5,
  "min_roe": 15,
  "min_revenue_growth_qtr_yoy": 10,
  "min_net_profit_qtr_growth_yoy": 15,
  "min_trendlyne_durability_score": 65,
  "min_trendlyne_valuation_score": 60,
  "min_piotroski_score": 6,
  "min_cash_from_operating_annual": 100,
  "min_score": 70,
  "limit": 30,
  "sort_by": "score",
  "use_trendlyne_scores": true,
  "trendlyne_weight": 0.3,
  "valuation_weight": 0.25,
  "profitability_weight": 0.25,
  "growth_weight": 0.2
}
```

## Example: Momentum Investing

Focus on stocks with strong momentum and growth:

```json
{
  "min_trendlyne_momentum_score": 70,
  "min_normalized_momentum_score": 0.7,
  "min_revenue_qoq_growth": 5,
  "min_net_profit_qoq_growth": 10,
  "min_revenue_growth_qtr_yoy": 15,
  "min_eps_ttm_growth": 10,
  "min_score": 60,
  "limit": 25,
  "sort_by": "trendlyne_momentum_score"
}
```

## Example: Value Investing with Sector Comparison

Find undervalued stocks compared to their sector:

```json
{
  "max_pe_vs_sector": 0.8,
  "max_pe_ttm": 20,
  "min_revenue_growth_vs_sector": 1.2,
  "min_profit_growth_vs_sector": 1.2,
  "min_trendlyne_valuation_score": 70,
  "max_price_to_52w_high": 0.85,
  "min_pct_days_below_pe": 60,
  "min_score": 65,
  "limit": 20,
  "sort_by": "trendlyne_valuation_score"
}
```

## Example: Quality + Growth (Piotroski + Trendlyne)

Combine Piotroski Score with Trendlyne Durability:

```json
{
  "min_piotroski_score": 7,
  "min_trendlyne_durability_score": 75,
  "min_roe": 18,
  "min_operating_profit_margin_qtr": 15,
  "min_revenue_growth_annual_yoy": 12,
  "min_net_profit_annual_yoy_growth": 15,
  "min_cash_from_operating_annual": 200,
  "min_score": 75,
  "limit": 15,
  "sort_by": "piotroski_score"
}
```

## Example: Cash Flow Focus

Stocks with strong cash generation:

```json
{
  "min_cash_from_operating_annual": 500,
  "min_net_cash_flow_annual": 100,
  "min_operating_profit_margin_qtr": 12,
  "min_trendlyne_durability_score": 65,
  "max_debt_to_equity": 0.5,
  "min_score": 60,
  "limit": 20,
  "sort_by": "score"
}
```

## Example: Quarterly Growth Focus

Stocks showing strong quarterly momentum:

```json
{
  "min_revenue_qoq_growth": 8,
  "min_net_profit_qoq_growth": 12,
  "min_revenue_growth_qtr_yoy": 20,
  "min_net_profit_qtr_growth_yoy": 25,
  "min_operating_profit_margin_qtr": 10,
  "min_trendlyne_momentum_score": 60,
  "min_score": 65,
  "limit": 25,
  "sort_by": "revenue_growth"
}
```

## Custom Weighted Scoring

Adjust the importance of different factors:

```json
{
  "min_trendlyne_durability_score": 70,
  "min_trendlyne_valuation_score": 65,
  "max_pe_ttm": 22,
  "min_roe": 15,
  "min_revenue_growth_annual_yoy": 10,
  "use_trendlyne_scores": true,
  "trendlyne_weight": 0.4,
  "valuation_weight": 0.2,
  "profitability_weight": 0.2,
  "growth_weight": 0.2,
  "min_score": 70,
  "limit": 20,
  "sort_by": "score"
}
```

## Understanding the Scores

### Trendlyne Scores (0-100)
- **Durability Score**: Measures business quality and sustainability
- **Valuation Score**: Measures if stock is fairly/undervalued
- **Momentum Score**: Measures price and earnings momentum

### Piotroski Score (0-9)
- 9 = Excellent financial health
- 7-8 = Good
- 5-6 = Average
- <5 = Poor

### Growth Metrics
- **QoQ Growth**: Quarter-over-quarter (shows recent momentum)
- **YoY Growth**: Year-over-year (shows annual trend)
- **TTM Growth**: Trailing twelve months

### Sector/Industry Comparisons
- Compare stock metrics vs sector/industry averages
- Find stocks outperforming their peers

## API Usage

```bash
curl -X POST http://localhost:8000/stocks/great \
  -H "Content-Type: application/json" \
  -d '{
    "min_trendlyne_durability_score": 70,
    "min_trendlyne_valuation_score": 60,
    "min_trendlyne_momentum_score": 50,
    "min_score": 65,
    "limit": 20,
    "sort_by": "trendlyne_durability_score"
  }'
```

## Tips

1. **Start with Trendlyne Scores**: They're comprehensive indicators
2. **Combine Multiple Metrics**: Don't rely on just one score
3. **Use Sector Comparisons**: Find stocks outperforming peers
4. **Check Quarterly Trends**: QoQ growth shows recent momentum
5. **Verify with Piotroski**: High score = strong financials
6. **Monitor Cash Flow**: Positive operating cash flow is crucial
7. **Adjust Weights**: Customize scoring based on your strategy

