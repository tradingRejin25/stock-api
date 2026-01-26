# Quality Stocks API Endpoints

## Base URL
```
http://localhost:8000  (Local)
https://your-render-url.onrender.com  (Production)
```

## All Endpoints

### 1. Root Endpoint
**GET** `/`

Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Quality Stocks API Service",
  "version": "1.0.0",
  "endpoints": {
    "great_quality": "/api/quality-stocks/great",
    "aggressive_quality": "/api/quality-stocks/aggressive",
    "good_quality": "/api/quality-stocks/good",
    "all_quality": "/api/quality-stocks/all",
    "stock_by_code": "/api/quality-stocks/stock/{nse_code}",
    "search": "/api/quality-stocks/search?query={query}"
  }
}
```

---

### 2. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 3. Great Quality Stocks
**GET** `/api/quality-stocks/great`

Returns all stocks that meet **strict quality criteria**:
- ROE > 12%
- ROCE > 15%
- Debt/Equity < 1
- Interest Coverage > 3
- Current Ratio > 1.2
- Revenue Growth > 10%
- Quality Score >= 70
- Consistent profit growth
- Stable/expanding margins
- ROA > 5%
- Positive cash flow
- Promoter pledge < 30%
- Altman Z-Score > 1.8

**Response:**
```json
{
  "count": 25,
  "tier": "Great",
  "stocks": [
    {
      "stockName": "RELIANCE",
      "nseCode": "RELIANCE",
      "isin": "INE467B01029",
      "marketCap": 1500000.0,
      "roe": 15.5,
      "roce": 18.2,
      "debtToEquity": 0.8,
      "interestCoverage": 5.2,
      "currentRatio": 1.5,
      "qualityScore": 78.5,
      "qualityTier": "Great",
      // ... all other metrics
    }
  ]
}
```

---

### 4. Aggressive Quality Stocks
**GET** `/api/quality-stocks/aggressive`

Returns stocks with **higher growth potential** but slightly relaxed criteria:
- ROE > 10%
- ROCE > 12%
- Debt/Equity < 1.5
- Interest Coverage > 2
- High growth (EPS > 15% OR Revenue > 20%)
- Quality Score >= 60
- Consistent profit growth (not inconsistent)
- Stable margins (not volatile)
- ROA > 3%
- Positive cash flow
- Promoter pledge < 40%
- Altman Z-Score > 1.5

**Response:**
```json
{
  "count": 45,
  "tier": "Aggressive",
  "stocks": [
    {
      "stockName": "TATAMOTORS",
      "nseCode": "TATAMOTORS",
      // ... all metrics
    }
  ]
}
```

---

### 5. Good Quality Stocks
**GET** `/api/quality-stocks/good`

Returns stocks with **balanced risk-reward**:
- ROE > 8%
- ROCE > 10%
- Debt/Equity < 2.0
- Interest Coverage > 1.5
- Quality Score 55-70 (excludes great quality)
- Consistent profit growth
- Stable margins
- Some positive growth indicators
- Cash flow quality not negative
- Promoter pledge < 50%

**Response:**
```json
{
  "count": 80,
  "tier": "Good",
  "stocks": [
    {
      "stockName": "INFY",
      "nseCode": "INFY",
      // ... all metrics
    }
  ]
}
```

---

### 6. All Quality Stocks
**GET** `/api/quality-stocks/all`

Returns **all quality stocks** categorized by tier (Great, Aggressive, Good).
Stocks that don't meet quality thresholds are excluded.

**Response:**
```json
{
  "great": {
    "count": 25,
    "tier": "Great",
    "stocks": [...]
  },
  "aggressive": {
    "count": 45,
    "tier": "Aggressive",
    "stocks": [...]
  },
  "good": {
    "count": 80,
    "tier": "Good",
    "stocks": [...]
  }
}
```

---

### 7. Get Stock by NSE Code
**GET** `/api/quality-stocks/stock/{nse_code}`

Get detailed information about a specific stock by its NSE code.

**Parameters:**
- `nse_code` (path parameter): NSE code of the stock (e.g., "RELIANCE", "TCS")

**Example:**
```
GET /api/quality-stocks/stock/RELIANCE
```

**Response:**
```json
{
  "stockName": "RELIANCE",
  "nseCode": "RELIANCE",
  "isin": "INE467B01029",
  "marketCap": 1500000.0,
  "roe": 15.5,
  "roce": 18.2,
  // ... all metrics
}
```

**Error Response (404):**
```json
{
  "detail": "Stock with NSE code INVALID not found"
}
```

---

### 8. Search Stocks
**GET** `/api/quality-stocks/search?query={query}&limit={limit}`

Search stocks by name or NSE code.

**Query Parameters:**
- `query` (required): Search term (stock name or NSE code)
- `limit` (optional, default: 20, max: 100): Maximum number of results

**Examples:**
```
GET /api/quality-stocks/search?query=reliance
GET /api/quality-stocks/search?query=TCS&limit=10
```

**Response:**
```json
[
  {
    "stockName": "RELIANCE",
    "nseCode": "RELIANCE",
    // ... all metrics
  },
  {
    "stockName": "RELIANCE INFRASTRUCTURE",
    "nseCode": "RELINFRA",
    // ... all metrics
  }
]
```

---

## Response Model Fields

Each stock response includes **50+ metrics**:

### Basic Information
- `stockName`: Stock name
- `nseCode`: NSE code
- `isin`: ISIN code
- `marketCap`: Market capitalization

### Core Quality Metrics
- `roe`: Return on Equity (%)
- `roce`: Return on Capital Employed (%)
- `debtToEquity`: Debt to Equity ratio
- `interestCoverage`: Interest Coverage ratio
- `currentRatio`: Current Ratio
- `promoterHolding`: Promoter holding (%)
- `promoterHoldingChange1Y`: Promoter holding change (1Y)

### Growth Metrics
- `epsTtmGrowth`: EPS TTM Growth (%)
- `operatingRevGrowthTtm`: Operating Revenue Growth TTM (%)
- `netProfitAnn`: Net Profit Annual
- `netProfitAnn1YAgo`: Net Profit Annual (1Y ago)
- `profitGrowthYoY`: Profit Growth YoY (%)
- `opmAnn`: Operating Profit Margin Annual (%)
- `opmAnn1YAgo`: Operating Profit Margin Annual (1Y ago)
- `opmTrend`: Operating Margin Trend (Stable/Expanding/Declining)
- `basicEpsTtm`: Basic EPS TTM
- `basicEpsTtm1YAgo`: Basic EPS TTM (1Y ago)

### Valuation Metrics
- `peTtm`: PE Ratio TTM
- `industryPeTtm`: Industry PE TTM
- `peVsIndustry`: PE vs Industry (Lower/Similar/Higher)
- `pegTtm`: PEG Ratio TTM
- `priceToBook`: Price to Book ratio
- `evPerEbitdaAnn`: EV/EBITDA Annual

### Quality Scores
- `durabilityScore`: Trendlyne Durability Score
- `valuationScore`: Trendlyne Valuation Score
- `piotroskiScore`: Piotroski Score (0-9)
- `altmanZscore`: Altman Z-Score
- `tobinQRatio`: Tobin Q Ratio
- `grahamNumber`: Graham Number

### Additional Metrics
- `epsQtrYoYGrowth`: EPS Quarterly YoY Growth (%)
- `basicEpsQoqGrowth`: Basic EPS QoQ Growth (%)
- `npmAnn`: Net Profit Margin Annual (%)
- `npmTtm`: Net Profit Margin TTM (%)
- `qualityScore`: Calculated Quality Score (0-100)
- `qualityTier`: Quality Tier (Great/Aggressive/Good)

### Enhanced Insights
- `consecutivePositiveQuarters`: Number of consecutive positive quarters
- `profitGrowthConsistency`: Profit Growth Consistency (Very Consistent/Consistent/Moderate/Inconsistent)
- `marginStability`: Margin Stability (Stable/Expanding/Moderately Stable/Volatile)
- `promoterTrend`: Promoter Trend (Rising/Stable/Declining)
- `cashFlowQuality`: Cash Flow Quality (Excellent/Good/Moderate/Negative)
- `roeTrend`: ROE Trend (Consistently Rising/Rising/Stable/Declining)
- `roceConsistency`: ROCE Consistency (Very Consistent/Consistent/Improving/Volatile)

### Additional Valuation
- `sectorPeTtm`: Sector PE TTM
- `sectorPbvTtm`: Sector PBV TTM
- `industryPbvTtm`: Industry PBV TTM

### Cash Flow & Efficiency
- `roaAnn`: Return on Assets Annual (%)
- `cashFlowReturnOnAssets`: Cash Flow Return on Assets (%)
- `cashEpsAnn`: Cash EPS Annual
- `cashEps1YGrowth`: Cash EPS 1Y Growth (%)
- `workingCapitalTurnover`: Working Capital Turnover
- `bookValue`: Book Value

### Profitability
- `priceToSalesTtm`: Price to Sales TTM
- `priceToCashflow`: Price to Cashflow
- `operatingProfitTtm`: Operating Profit TTM
- `operatingProfitTtm1YAgo`: Operating Profit TTM (1Y ago)
- `operatingProfitGrowthQtrYoY`: Operating Profit Growth Qtr YoY (%)
- `ebitdaAnn`: EBITDA Annual
- `ebitdaTtm`: EBITDA TTM
- `ebitdaAnnMargin`: EBITDA Annual Margin (%)
- `ebitAnnMargin`: EBIT Annual Margin (%)
- `ebitdaQtrYoYGrowth`: EBITDA Qtr YoY Growth (%)

### Risk Indicators
- `promoterPledgePercentage`: Promoter Pledge Percentage (%)
- `grossNpaRatio`: Gross NPA Ratio (%) - for banks
- `capitalAdequacyRatio`: Capital Adequacy Ratio (%) - for banks

### Relative Performance
- `industryScore`: Industry Score
- `sectorScore`: Sector Score
- `tlChecklistPositiveScore`: Trendlyne Checklist Positive Score
- `tlChecklistNegativeScore`: Trendlyne Checklist Negative Score

---

## Usage Examples

### cURL Examples

```bash
# Get great quality stocks
curl http://localhost:8000/api/quality-stocks/great

# Get aggressive quality stocks
curl http://localhost:8000/api/quality-stocks/aggressive

# Get good quality stocks
curl http://localhost:8000/api/quality-stocks/good

# Get all quality stocks
curl http://localhost:8000/api/quality-stocks/all

# Get specific stock
curl http://localhost:8000/api/quality-stocks/stock/RELIANCE

# Search stocks
curl "http://localhost:8000/api/quality-stocks/search?query=tata&limit=10"
```

### JavaScript/Fetch Examples

```javascript
// Get great quality stocks
const response = await fetch('http://localhost:8000/api/quality-stocks/great');
const data = await response.json();
console.log(data.stocks);

// Search stocks
const searchResponse = await fetch(
  'http://localhost:8000/api/quality-stocks/search?query=reliance&limit=5'
);
const searchData = await searchResponse.json();
console.log(searchData);
```

### Python Examples

```python
import requests

# Get great quality stocks
response = requests.get('http://localhost:8000/api/quality-stocks/great')
data = response.json()
print(f"Found {data['count']} great quality stocks")

# Get specific stock
stock = requests.get('http://localhost:8000/api/quality-stocks/stock/RELIANCE')
stock_data = stock.json()
print(f"ROE: {stock_data['roe']}%")
print(f"Quality Score: {stock_data['qualityScore']}")
```

---

## Notes

1. **No Limits**: All endpoints return all matching stocks (no artificial limits)
2. **Quality Filtering**: Only stocks meeting quality thresholds are returned
3. **Comprehensive Metrics**: Each stock includes 50+ financial and quality metrics
4. **CORS Enabled**: API supports cross-origin requests
5. **Error Handling**: All endpoints return appropriate HTTP status codes (200, 404, 500)

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Stock with NSE code {nse_code} not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error fetching {endpoint}: {error_message}"
}
```

