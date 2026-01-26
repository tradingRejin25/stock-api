# Quick Start Guide

## Setup

1. **Install Dependencies**
   ```bash
   cd stock_api_service
   pip install -r requirements.txt
   ```

2. **Place CSV File**
   - Copy your `filtered_stocks.csv` file to `stock_api_service/data/` directory
   - Or update the path in the service initialization

3. **Test the Service** (Optional)
   ```bash
   python test_service.py
   ```

4. **Run the API Server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access API Documentation**
   - Open browser: http://localhost:8000/docs
   - Interactive API documentation with Swagger UI

## API Usage Examples

### Get Great Quality Stocks
```bash
curl http://localhost:8000/api/quality-stocks/great?limit=10
```

### Get Aggressive Quality Stocks
```bash
curl http://localhost:8000/api/quality-stocks/aggressive?limit=10
```

### Get Medium Quality Stocks
```bash
curl http://localhost:8000/api/quality-stocks/medium?limit=10
```

### Get All Quality Stocks
```bash
curl http://localhost:8000/api/quality-stocks/all?limit=10
```

### Search Stocks
```bash
curl "http://localhost:8000/api/quality-stocks/search?query=RELIANCE&limit=5"
```

### Get Specific Stock
```bash
curl http://localhost:8000/api/quality-stocks/stock/RELIANCE
```

## Quality Scoring

The service calculates a quality score (0-100) based on:

1. **ROE** (20 points): Return on Equity
2. **ROCE** (20 points): Return on Capital Employed
3. **Debt/Equity** (15 points): Lower is better
4. **Interest Coverage** (10 points): Ability to service debt
5. **Current Ratio** (10 points): Liquidity measure
6. **Promoter Holding** (7 points): Skin in the game
7. **EPS Growth** (10 points): Earnings growth
8. **Revenue Growth** (10 points): Sales growth
9. **Profit Growth** (8 points): Consistent profitability
10. **Operating Margin Trend** (5 points): Margin expansion
11. **PEG Ratio** (5 points): Growth-adjusted valuation
12. **Trendlyne Scores** (20 points): Durability, Valuation, Momentum

## Response Format

Each stock response includes:

- **Basic Info**: stockName, nseCode, isin, marketCap
- **Quality Metrics**: roe, roce, debtToEquity, interestCoverage, currentRatio
- **Growth Metrics**: epsTtmGrowth, operatingRevGrowthTtm, profitGrowthYoY
- **Valuation**: peTtm, pegTtm, priceToBook, evPerEbitdaAnn
- **Trendlyne Scores**: durabilityScore, valuationScore, momentumScore
- **Quality Score**: Calculated score (0-100)
- **Quality Tier**: Great/Aggressive/Medium

## Deployment

For Render.com deployment:

1. Push code to GitHub
2. Connect repository to Render
3. Render will automatically detect `render.yaml` and deploy
4. Ensure CSV file is in the repository or configure path

## Troubleshooting

**Issue**: No stocks loaded
- Check CSV file path
- Verify CSV file format matches Trendlyne export
- Check file encoding (should be UTF-8)

**Issue**: Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.11.7 recommended)

**Issue**: API not responding
- Check if server is running: `uvicorn main:app --reload`
- Verify port is not in use
- Check logs for errors

