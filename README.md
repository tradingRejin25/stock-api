# Quality Stocks API Service

A FastAPI service that analyzes stocks from Trendlyne CSV exports and categorizes them into quality tiers based on comprehensive financial metrics.

## Features

- **Great Quality Stocks**: Strict criteria for high-quality, low-risk investments
- **Aggressive Quality Stocks**: Higher growth potential with moderate risk
- **Medium Quality Stocks**: Balanced risk-reward profile
- **Comprehensive Analysis**: ROE, ROCE, Debt/Equity, Interest Coverage, Growth metrics, and more
- **Trendlyne Integration**: Uses Durability, Valuation, and Momentum scores

## Quality Criteria

### Great Quality Stocks
- ROE > 12%
- ROCE > 15%
- Debt/Equity < 1
- Interest Coverage > 3
- Current Ratio > 1.2
- Revenue Growth > 10%
- Quality Score >= 70

### Aggressive Quality Stocks
- ROE > 10%
- ROCE > 12%
- Debt/Equity < 1.5
- Interest Coverage > 2
- High growth (EPS > 15% or Revenue > 20%)
- Quality Score >= 60

### Medium Quality Stocks
- ROE > 8%
- ROCE > 10%
- Debt/Equity < 2.0
- Interest Coverage > 1.5
- Quality Score 50-70

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your `filtered_stocks.csv` file in the `data/` directory

3. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Get Great Quality Stocks
```
GET /api/quality-stocks/great?limit=50
```

### Get Aggressive Quality Stocks
```
GET /api/quality-stocks/aggressive?limit=50
```

### Get Medium Quality Stocks
```
GET /api/quality-stocks/medium?limit=50
```

### Get All Quality Stocks
```
GET /api/quality-stocks/all?limit=50
```

### Get Stock by NSE Code
```
GET /api/quality-stocks/stock/{nse_code}
```

### Search Stocks
```
GET /api/quality-stocks/search?query=RELIANCE&limit=20
```

## Response Format

Each stock includes:
- Basic Info: stockName, nseCode, isin, marketCap
- Quality Metrics: roe, roce, debtToEquity, interestCoverage, currentRatio
- Growth Metrics: epsTtmGrowth, operatingRevGrowthTtm, profitGrowthYoY
- Valuation: peTtm, pegTtm, priceToBook, evPerEbitdaAnn
- Trendlyne Scores: durabilityScore, valuationScore, momentumScore
- Quality Score: Calculated quality score (0-100)
- Quality Tier: Great/Aggressive/Medium

## CSV File Format

The service expects a CSV file with columns matching Trendlyne export format, including:
- Stock, NSE Code, ISIN
- ROE Ann %, ROCE Ann %
- Total Debt to Total Equity Ann
- Interest Coverage Ratio Ann
- Current Ratio Ann
- Promoter holding latest %
- EPS TTM Growth %
- Operating Rev growth TTM %
- And other financial metrics

## Deployment

For Render deployment, ensure:
- `requirements.txt` is present
- `runtime.txt` specifies Python version (e.g., `python-3.11.7`)
- CSV file is in `data/` directory or path is configured

