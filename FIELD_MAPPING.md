# CSV Field to API Variable Mapping

This document shows the complete mapping between Excel/CSV column names and API variable names.

## Summary
- **Total fields in CSV**: 57
- **Mapped fields**: 47
- **Unmapped fields**: 10
- **Coverage**: 82.5%

---

## Complete Field Mapping

### Basic Information
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `Stock` | `stock_name` | str | Stock name |
| `NSE Code` | `nse_code` | str | NSE stock code |
| `ISIN` | `isin` | str | ISIN identifier |
| `BSE Code` | `bse_code` | str | **UNMAPPED** - BSE stock code |
| `Sl No` | - | int | Serial number (not needed) |

### Core Quality Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `ROE Ann  %` | `roe` | float | Return on Equity (Annual %) |
| `ROCE Ann  %` | `roce` | float | Return on Capital Employed (Annual %) |
| `Total Debt to Total Equity Ann ` | `debt_to_equity` | float | Debt to Equity Ratio |
| `Interest Coverage Ratio Ann ` | `interest_coverage` | float | Interest Coverage Ratio |
| `Current Ratio Ann ` | `current_ratio` | float | Current Ratio (Annual) |
| `Current Ratio TTM` | `current_ratio_ttm` | float | **UNMAPPED** - Current Ratio (TTM) |
| `Promoter holding latest %` | `promoter_holding` | float | Promoter holding percentage |
| `Promoter holding change 1Y %` | `promoter_holding_change_1y` | float | Promoter holding change (1 Year) |
| `Promoter holding change QoQ %` | `promoter_holding_change_qoq` | float | Promoter holding change (QoQ) |
| `Promoter holding pledge percentage % Qtr` | `promoter_pledge_percentage` | float | Promoter pledge percentage |

### Growth Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `EPS TTM Growth %` | `eps_ttm_growth` | float | EPS TTM Growth % |
| `EPS Qtr YoY Growth %` | `eps_qtr_yoy_growth` | float | EPS Quarter YoY Growth % |
| `Basic EPS QoQ Growth %` | `basic_eps_qoq_growth` | float | Basic EPS QoQ Growth % |
| `Basic EPS TTM` | `basic_eps_ttm` | float | Basic EPS TTM |
| `Operating Rev  growth TTM %` | `operating_rev_growth_ttm` | float | Operating Revenue Growth TTM % |
| `Net Profit Ann ` | `net_profit_ann` | float | Net Profit (Annual) |
| `Net Profit Ann  1Y Ago` | `net_profit_ann_1y_ago` | float | Net Profit (Annual, 1Y Ago) |
| `Net Profit 3Y Growth %` | `net_profit_3y_growth` | float | **UNMAPPED** - Net Profit 3Y Growth % |
| `Net Profit 5Y Growth %` | `net_profit_5y_growth` | float | **UNMAPPED** - Net Profit 5Y Growth % |
| `Net Profit QoQ Growth %` | `net_profit_qoq_growth` | float | **UNMAPPED** - Net Profit QoQ Growth % |
| `Operating Profit Growth Qtr YoY %` | `operating_profit_growth_qtr_yoy` | float | Operating Profit Growth Qtr YoY % |

### Profitability Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `OPM Ann  %` | `opm_ann` | float | Operating Profit Margin (Annual %) |
| `OPM Ann  1Y ago %` | `opm_ann_1y_ago` | float | OPM (Annual, 1Y Ago %) |
| `OPM TTM %` | `opm_ttm` | float | **UNMAPPED** - Operating Profit Margin (TTM %) |
| `NPM Ann  %` | `npm_ann` | float | Net Profit Margin (Annual %) |
| `NPM TTM %` | `npm_ttm` | float | Net Profit Margin (TTM %) |
| `EBITDA Ann ` | `ebitda_ann` | float | EBITDA (Annual) |
| `EBITDA TTM` | `ebitda_ttm` | float | EBITDA (TTM) |
| `EBITDA Ann  margin %` | `ebitda_ann_margin` | float | EBITDA Margin (Annual %) |
| `EBITDA Ann  Margin %` | `ebitda_ann_margin` | float | **UNMAPPED** - Alternative spelling |
| `EBIT Ann  Margin %` | `ebit_ann_margin` | float | EBIT Margin (Annual %) |
| `EBITDA Qtr YoY Growth %` | `ebitda_qtr_yoy_growth` | float | EBITDA Qtr YoY Growth % |

### Valuation Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `Industry PE TTM` | `industry_pe_ttm` | float | Industry PE (TTM) |
| `PEG TTM` | `peg_ttm` | float | PEG Ratio (TTM) |
| `Industry PBV TTM` | `price_to_book` | float | Industry Price to Book Value (TTM) |
| `PBV Adjusted` | `price_to_book_adjusted` | float | Price to Book Value (Adjusted) |
| `EV Per EBITDA Ann ` | `ev_per_ebitda_ann` | float | EV per EBITDA (Annual) |
| `Price To Sales Ann ` | `price_to_sales_ann` | float | Price to Sales (Annual) |
| `Price to Sales TTM` | `price_to_sales_ttm` | float | Price to Sales (TTM) |
| `Price to Cashflow from Operations` | `price_to_cashflow` | float | Price to Cashflow |

### Trendlyne Scores
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `Durability Score` | `durability_score` | int | Durability Score (0-100) |
| `Valuation Score` | `valuation_score` | int | Valuation Score (0-100) |
| `Industry Score` | `industry_score` | int | Industry Score |
| `Sector Score` | `sector_score` | int | Sector Score |
| `TL Checklist Positive Score` | `tl_checklist_positive_score` | int | Trendlyne Checklist Positive Score |
| `TL Checklist Negative Score` | `tl_checklist_negative_score` | int | Trendlyne Checklist Negative Score |

### Quality Scores (Academic/Research-based)
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `Piotroski Score` | `piotroski_score` | int | Piotroski F-Score (0-9) |
| `Altman Zscore` | `altman_zscore` | float | Altman Z-Score |
| `Tobin Q Ratio` | `tobin_q_ratio` | float | Tobin's Q Ratio |
| `Graham No ` | `graham_number` | float | Graham's Number |

### Additional Quality Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `RoA Ann  %` | `roa_ann` | float | Return on Assets (Annual %) |
| `RoA Ann  1Y Ago %` | `roa_ann_1y_ago` | float | ROA (Annual, 1Y Ago %) |
| `ROE Ann  1Y Ago %` | `roe_1y_ago` | float | ROE (Annual, 1Y Ago %) |
| `ROE Ann  2Y Ago %` | `roe_2y_ago` | float | ROE (Annual, 2Y Ago %) |
| `ROE Ann  3Y Ago %` | `roe_3y_ago` | float | ROE (Annual, 3Y Ago %) |
| `ROCE Ann  3Y Avg %` | `roce_3y_avg` | float | ROCE (3Y Average %) |
| `ROCE Ann  5Y Avg %` | `roce_5y_avg` | float | ROCE (5Y Average %) |
| `Cash Flow Return on Assets Ann ` | `cash_flow_return_on_assets` | float | Cash Flow Return on Assets |
| `Cash Flow Return on Assets Ann  1Y ago` | `cash_flow_return_on_assets_1y_ago` | float | Cash Flow Return on Assets (1Y Ago) |
| `Cash EPS Ann ` | `cash_eps_ann` | float | Cash EPS (Annual) |
| `Cash EPS Ann  1Y Ago` | `cash_eps_ann_1y_ago` | float | Cash EPS (Annual, 1Y Ago) |
| `Cash EPS 1Y Growth %` | `cash_eps_1y_growth` | float | Cash EPS 1Y Growth % |
| `Working Capital Turnover Ann ` | `working_capital_turnover` | float | Working Capital Turnover |
| `Book Value Inc Reval Reserve Ann ` | `book_value` | float | Book Value |
| `Operating Profit TTM` | `operating_profit_ttm` | float | Operating Profit (TTM) |
| `Operating Profit TTM 1Y Ago` | `operating_profit_ttm_1y_ago` | float | Operating Profit (TTM, 1Y Ago) |

### Sector/Industry Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `Sector ROCE` | `sector_roce` | float | Sector ROCE |
| `Industry ROCE` | `industry_roce` | float | Industry ROCE |
| `Sector ROE` | `sector_roe` | float | Sector ROE |
| `Industry ROE` | `industry_roe` | float | Industry ROE |
| `Sector PEG TTM` | `sector_peg_ttm` | float | Sector PEG (TTM) |
| `Industry PEG TTM` | `industry_peg_ttm` | float | Industry PEG (TTM) |
| `Sector PBV TTM` | `sector_pbv_ttm` | float | Sector PBV (TTM) |
| `Sector Net Profit Growth Qtr QoQ %` | `sector_net_profit_growth_qtr_qoq` | float | Sector Net Profit Growth (Qtr QoQ %) |
| `Sector Net Profit Growth Ann  YoY %` | `sector_net_profit_growth_ann_yoy` | float | Sector Net Profit Growth (Ann YoY %) |
| `Industry Net Profit Growth Qtr QoQ %` | `industry_net_profit_growth_qtr_qoq` | float | Industry Net Profit Growth (Qtr QoQ %) |
| `Industry Net Profit Growth Ann  YoY %` | `industry_net_profit_growth_ann_yoy` | float | Industry Net Profit Growth (Ann YoY %) |

### SWOT Analysis
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `SWOT Strengths` | `swot_strengths` | int | SWOT Strengths count |
| `SWOT Weakness` | `swot_weakness` | int | SWOT Weakness count |
| `SWOT Opportunities` | `swot_opportunities` | int | SWOT Opportunities count |
| `SWOT Threats` | `swot_threats` | int | SWOT Threats count |

### Forward Estimates
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `FC Est  1Q forward EBIT Qtr` | `fc_est_1q_forward_ebit_qtr` | float | Forward Estimate: 1Q forward EBIT Qtr |
| `FC Est  1Q fwd Cash EPS Qtr` | `fc_est_1q_fwd_cash_eps_qtr` | float | **UNMAPPED** - Forward Estimate: 1Q fwd Cash EPS Qtr |
| `FC Est  1Q fwd Interest Expense Qtr` | `fc_est_1q_fwd_interest_expense_qtr` | float | **UNMAPPED** - Forward Estimate: 1Q fwd Interest Expense Qtr |

### Bank-Specific Metrics
| Excel Column Name | API Variable Name | Type | Notes |
|-------------------|-------------------|------|-------|
| `Gross NPA ratio Qtr %` | `gross_npa_ratio` | float | Gross NPA Ratio (Qtr %) |
| `Capital Adequacy Ratios Ann  %` | `capital_adequacy_ratio` | float | Capital Adequacy Ratio (Ann %) |

---

## Unmapped Fields (Need to be Added)

1. **`BSE Code`** → `bse_code` (str)
2. **`Current Ratio TTM`** → `current_ratio_ttm` (float)
3. **`EBITDA Ann  Margin %`** → `ebitda_ann_margin` (float) - Alternative spelling, already mapped
4. **`Net Profit 3Y Growth %`** → `net_profit_3y_growth` (float)
5. **`Net Profit 5Y Growth %`** → `net_profit_5y_growth` (float)
6. **`Net Profit QoQ Growth %`** → `net_profit_qoq_growth` (float)
7. **`OPM TTM %`** → `opm_ttm` (float)
8. **`FC Est  1Q fwd Cash EPS Qtr`** → `fc_est_1q_fwd_cash_eps_qtr` (float)
9. **`FC Est  1Q fwd Interest Expense Qtr`** → `fc_est_1q_fwd_interest_expense_qtr` (float)
10. **`Sl No`** - Serial number (can be ignored)

---

## Notes

- All field names are case-sensitive and include exact spacing as in CSV
- Some fields have trailing spaces (e.g., `'Total Debt to Total Equity Ann '`)
- Some fields have alternative spellings (e.g., `'EBITDA Ann  margin %'` vs `'EBITDA Ann  Margin %'`)
- The mapping should handle both variations where applicable

