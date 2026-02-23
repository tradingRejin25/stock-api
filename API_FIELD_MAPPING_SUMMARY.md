# API Field Mapping Summary

## Overview
The API now uses **mapped variable names** (camelCase) instead of Excel field names in all responses. All fields are accessed through the `QualityStock` dataclass attributes, which use clean, standardized variable names.

## Mapping Strategy

### Excel CSV → Dataclass → API Response

1. **Excel CSV Fields** (e.g., `'ROE Ann  %'`, `'Promoter holding latest %'`)
   ↓
2. **Dataclass Attributes** (e.g., `stock.roe`, `stock.promoter_holding`)
   ↓
3. **API Response Fields** (e.g., `roe`, `promoterHolding`)

## Complete Field Mapping

### Basic Information
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `Stock` | `stock.stock_name` | `stockName` |
| `NSE Code` | `stock.nse_code` | `nseCode` |
| `BSE Code` | `stock.bse_code` | `bseCode` |
| `ISIN` | `stock.isin` | `isin` |
| `Market Cap` | `stock.market_cap` | `marketCap` |

### Core Quality Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `ROE Ann  %` | `stock.roe` | `roe` |
| `ROCE Ann  %` | `stock.roce` | `roce` |
| `Total Debt to Total Equity Ann ` | `stock.debt_to_equity` | `debtToEquity` |
| `Interest Coverage Ratio Ann ` | `stock.interest_coverage` | `interestCoverage` |
| `Current Ratio Ann ` | `stock.current_ratio` | `currentRatio` |
| `Current Ratio TTM` | `stock.current_ratio_ttm` | `currentRatioTtm` |
| `Promoter holding latest %` | `stock.promoter_holding` | `promoterHolding` |
| `Promoter holding change 1Y %` | `stock.promoter_holding_change_1y` | `promoterHoldingChange1Y` |
| `Promoter holding change QoQ %` | `stock.promoter_holding_change_qoq` | `promoterHoldingChangeQoq` |
| `Promoter holding change 2Y %` | `stock.promoter_holding_change_2y` | `promoterHoldingChange2Y` |

### Growth Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `EPS TTM Growth %` | `stock.eps_ttm_growth` | `epsTtmGrowth` |
| `EPS Qtr YoY Growth %` | `stock.eps_qtr_yoy_growth` | `epsQtrYoYGrowth` |
| `Basic EPS QoQ Growth %` | `stock.basic_eps_qoq_growth` | `basicEpsQoqGrowth` |
| `Operating Rev  growth TTM %` | `stock.operating_rev_growth_ttm` | `operatingRevGrowthTtm` |
| `Net Profit Ann ` | `stock.net_profit_ann` | `netProfitAnn` |
| `Net Profit Ann  1Y Ago` | `stock.net_profit_ann_1y_ago` | `netProfitAnn1YAgo` |
| `Net Profit 3Y Growth %` | `stock.net_profit_3y_growth` | `netProfit3YGrowth` |
| `Net Profit 5Y Growth %` | `stock.net_profit_5y_growth` | `netProfit5YGrowth` |
| `Net Profit QoQ Growth %` | `stock.net_profit_qoq_growth` | `netProfitQoqGrowth` |
| `Operating Profit Growth Qtr YoY %` | `stock.operating_profit_growth_qtr_yoy` | `operatingProfitGrowthQtrYoY` |

### Profitability Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `OPM Ann  %` | `stock.opm_ann` | `opmAnn` |
| `OPM Ann  1Y ago %` | `stock.opm_ann_1y_ago` | `opmAnn1YAgo` |
| `OPM TTM %` | `stock.opm_ttm` | `opmTtm` |
| `NPM Ann  %` | `stock.npm_ann` | `npmAnn` |
| `NPM TTM %` | `stock.npm_ttm` | `npmTtm` |
| `EBITDA Ann ` | `stock.ebitda_ann` | `ebitdaAnn` |
| `EBITDA TTM` | `stock.ebitda_ttm` | `ebitdaTtm` |
| `EBITDA Ann  margin %` | `stock.ebitda_ann_margin` | `ebitdaAnnMargin` |
| `EBIT Ann  Margin %` | `stock.ebit_ann_margin` | `ebitAnnMargin` |
| `EBITDA Qtr YoY Growth %` | `stock.ebitda_qtr_yoy_growth` | `ebitdaQtrYoYGrowth` |

### Valuation Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `Industry PE TTM` | `stock.industry_pe_ttm` | `industryPeTtm` |
| `PEG TTM` | `stock.peg_ttm` | `pegTtm` |
| `Industry PBV TTM` | `stock.price_to_book` | `priceToBook` |
| `PBV Adjusted` | `stock.price_to_book_adjusted` | `priceToBookAdjusted` |
| `EV Per EBITDA Ann ` | `stock.ev_per_ebitda_ann` | `evPerEbitdaAnn` |
| `Price To Sales Ann ` | `stock.price_to_sales_ann` | `priceToSalesAnn` |
| `Price to Sales TTM` | `stock.price_to_sales_ttm` | `priceToSalesTtm` |
| `Price to Cashflow from Operations` | `stock.price_to_cashflow` | `priceToCashflow` |
| `Graham Ratio` | `stock.graham_ratio` | `grahamRatio` |

### Trendlyne Scores
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `Durability Score` | `stock.durability_score` | `durabilityScore` |
| `Valuation Score` | `stock.valuation_score` | `valuationScore` |
| `Industry Score` | `stock.industry_score` | `industryScore` |
| `Sector Score` | `stock.sector_score` | `sectorScore` |
| `TL Checklist Positive Score` | `stock.tl_checklist_positive_score` | `tlChecklistPositiveScore` |
| `TL Checklist Negative Score` | `stock.tl_checklist_negative_score` | `tlChecklistNegativeScore` |

### Quality Scores
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `Piotroski Score` | `stock.piotroski_score` | `piotroskiScore` |
| `Altman Zscore` | `stock.altman_zscore` | `altmanZscore` |
| `Tobin Q Ratio` | `stock.tobin_q_ratio` | `tobinQRatio` |
| `Graham No ` | `stock.graham_number` | `grahamNumber` |

### Additional Quality Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `RoA Ann  %` | `stock.roa_ann` | `roaAnn` |
| `RoA Ann  1Y Ago %` | `stock.roa_ann_1y_ago` | `roaAnn1YAgo` |
| `ROE Ann  1Y Ago %` | `stock.roe_1y_ago` | `roe1YAgo` |
| `ROE Ann  2Y Ago %` | `stock.roe_2y_ago` | `roe2YAgo` |
| `ROE Ann  3Y Ago %` | `stock.roe_3y_ago` | `roe3YAgo` |
| `ROCE Ann  3Y Avg %` | `stock.roce_3y_avg` | `roce3YAvg` |
| `ROCE Ann  5Y Avg %` | `stock.roce_5y_avg` | `roce5YAvg` |
| `Cash Flow Return on Assets Ann ` | `stock.cash_flow_return_on_assets` | `cashFlowReturnOnAssets` |
| `Cash Flow Return on Assets Ann  1Y ago` | `stock.cash_flow_return_on_assets_1y_ago` | `cashFlowReturnOnAssets1YAgo` |
| `Cash EPS Ann ` | `stock.cash_eps_ann` | `cashEpsAnn` |
| `Cash EPS Ann  1Y Ago` | `stock.cash_eps_ann_1y_ago` | `cashEpsAnn1YAgo` |
| `Cash EPS 1Y Growth %` | `stock.cash_eps_1y_growth` | `cashEps1YGrowth` |
| `Working Capital Turnover Ann ` | `stock.working_capital_turnover` | `workingCapitalTurnover` |
| `Book Value Inc Reval Reserve Ann ` | `stock.book_value` | `bookValue` |
| `Operating Profit TTM` | `stock.operating_profit_ttm` | `operatingProfitTtm` |
| `Operating Profit TTM 1Y Ago` | `stock.operating_profit_ttm_1y_ago` | `operatingProfitTtm1YAgo` |
| `Promoter holding pledge percentage % Qtr` | `stock.promoter_pledge_percentage` | `promoterPledgePercentage` |

### Sector/Industry Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `Sector ROCE` | `stock.sector_roce` | `sectorRoce` |
| `Industry ROCE` | `stock.industry_roce` | `industryRoce` |
| `Sector ROE` | `stock.sector_roe` | `sectorRoe` |
| `Industry ROE` | `stock.industry_roe` | `industryRoe` |
| `Sector PEG TTM` | `stock.sector_peg_ttm` | `sectorPegTtm` |
| `Industry PEG TTM` | `stock.industry_peg_ttm` | `industryPegTtm` |
| `Sector PBV TTM` | `stock.sector_pbv_ttm` | `sectorPbvTtm` |
| `Sector PE TTM` | `stock.sector_pe_ttm` | `sectorPeTtm` |
| `Sector Net Profit Growth Qtr QoQ %` | `stock.sector_net_profit_growth_qtr_qoq` | `sectorNetProfitGrowthQtrQoq` |
| `Sector Net Profit Growth Ann  YoY %` | `stock.sector_net_profit_growth_ann_yoy` | `sectorNetProfitGrowthAnnYoy` |
| `Industry Net Profit Growth Qtr QoQ %` | `stock.industry_net_profit_growth_qtr_qoq` | `industryNetProfitGrowthQtrQoq` |
| `Industry Net Profit Growth Ann  YoY %` | `stock.industry_net_profit_growth_ann_yoy` | `industryNetProfitGrowthAnnYoy` |

### SWOT Analysis
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `SWOT Strengths` | `stock.swot_strengths` | `swotStrengths` |
| `SWOT Weakness` | `stock.swot_weakness` | `swotWeakness` |
| `SWOT Opportunities` | `stock.swot_opportunities` | `swotOpportunities` |
| `SWOT Threats` | `stock.swot_threats` | `swotThreats` |

### Forward Estimates
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `FC Est  1Q forward EBIT Qtr` | `stock.fc_est_1q_forward_ebit_qtr` | `fcEst1QForwardEbitQtr` |
| `FC Est  1Q fwd Cash EPS Qtr` | `stock.fc_est_1q_fwd_cash_eps_qtr` | `fcEst1QFwdCashEpsQtr` |
| `FC Est  1Q fwd Interest Expense Qtr` | `stock.fc_est_1q_fwd_interest_expense_qtr` | `fcEst1QFwdInterestExpenseQtr` |

### Bank-Specific Metrics
| Excel Field | Dataclass Attribute | API Response Field |
|-------------|---------------------|-------------------|
| `Gross NPA ratio Qtr %` | `stock.gross_npa_ratio` | `grossNpaRatio` |
| `Capital Adequacy Ratios Ann  %` | `stock.capital_adequacy_ratio` | `capitalAdequacyRatio` |

## Implementation Details

### Service Layer (`quality_stocks_service.py`)
- Reads CSV files and maps Excel field names to dataclass attributes
- Uses `_safe_float()` and `_safe_int()` for safe type conversion
- Handles empty strings, '-', 'N/A', 'NA', 'None' as missing values
- Stores all data in `QualityStock` dataclass with clean variable names

### API Layer (`quality_stocks_routes.py`)
- `_stock_to_response()` function converts `QualityStock` dataclass to `StockResponse` Pydantic model
- **All fields use dataclass attributes** (e.g., `stock.roe`, `stock.promoter_holding`)
- **No Excel field names are used** in the API response
- API response uses camelCase naming convention (e.g., `roe`, `promoterHolding`, `netProfit3YGrowth`)

## Benefits

1. **Clean API Response**: No more Excel field names with spaces, special characters, or inconsistent formatting
2. **Consistent Naming**: All fields use camelCase convention
3. **Type Safety**: Pydantic models ensure proper data types
4. **Maintainability**: Changes to Excel field names only require updates in the service layer
5. **Documentation**: Clear mapping between Excel → Dataclass → API

## Coverage

- **Total CSV Fields**: 57
- **Mapped Fields**: 56 (98.2% coverage)
- **Unmapped Fields**: 1 (`Sl No` - serial number, not needed)

All important fields are now properly mapped and accessible through clean API variable names!

