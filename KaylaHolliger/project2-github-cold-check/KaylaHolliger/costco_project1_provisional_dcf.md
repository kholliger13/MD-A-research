# Costco provisional DCF — October 8, 2025

Calculated October 19, 2026. USD millions except per-share values. This is a conditional model result, not a final recommendation.

## Inputs and qualifications

- WACC uses 4.13% risk-free rate, raw monthly beta 0.975320 and ERP 4.01%, explicitly reported in Damodaran’s October 6, 2025 article. This replaces the previously provisional 3.77% variant; it is a source/method choice, not a claim that every implied ERP method agrees.
- Financing weights: $914.80 close × 443.179176 million outstanding shares; debt fair-value proxy 5,370 and finance-lease liability 1,479, both from August 31. Borrowing cost: AA index proxy 4.50% (October 7), lease rate proxy 4.63%, tax shield proxy 26.1%. Proxy suitability and deductibility remain open.
- DCF denominator: historical weighted-average diluted shares 444.803 million, not a fully reconciled valuation-date diluted count.
- 38 days of FY2026 precede the valuation date. Assume uniform annual FCFF: exclude 38/364 of FY2026 and discount the remaining flow to its fiscal year end, August 30, 2026. Later fiscal dates use the Sunday nearest August 31; actual/365 discounting.
- Cash, required operating cash and finance-lease debt at October 8 are linear estimates from opening and FY2026 forecast amounts; investments and borrowing fair value are stale-date proxies. No actual October 8 balances are asserted.
- Required cash is 2% of sales; only excess cash enters the bridge. Future accumulated cash is not added again.
- FCFF deducts new finance-lease assets as reinvestment. Finance-lease principal is excluded from FCFF; lease obligations are subtracted once in the equity bridge. Operating leases retain operating treatment.
- Finance-lease interest embedded in merchandise costs is unquantified. Compare historical allocation endpoints 0 and 63 (the full disclosed finance-lease interest expense), each scaled with sales and removed from operating costs. This brackets only allocation uncertainty, not overall business risk.
- Terminal growth 3% and incremental ROIC 20% are analyst assumptions. Terminal reinvestment g/ROIC includes total operating reinvestment, including lease investment and operating cash, rather than adding further terminal deductions.
- Year-end discounting plus uniform first-year cash-flow proration is an approximation. Original historical reconciliation and forecast expense/D&A classifications still need review.

## Conditional allocation endpoints

| Metric | No interest embedded | All 63 embedded |
|---|---:|---:|
| WACC (%) | 7.9630 | 7.9630 |
| PV explicit FCFF | 22,934.4841 | 23,156.3169 |
| PV terminal value | 128,218.9480 | 128,980.8372 |
| Enterprise value | 151,153.4320 | 152,137.1542 |
| Estimated October 8 cash | 14,492.0829 | 14,495.7573 |
| Required cash reserve | 5,443.3242 | 5,443.3242 |
| Excess cash added | 9,048.7587 | 9,052.4331 |
| Investments added | 1,123.0000 | 1,123.0000 |
| Borrowing value subtracted | 5,370.0000 | 5,370.0000 |
| Estimated finance leases subtracted | 1,478.4237 | 1,478.4237 |
| Equity value | 154,476.7670 | 155,464.1636 |
| Diluted share proxy | 444.8030 | 444.8030 |
| Value per share | 347.2925 | 349.5124 |
| Terminal share of EV (%) | 84.8270 | 84.7793 |
| Terminal FCFF step vs FY2030 (%) | 42.4069 | 41.8818 |

## FCFF trace — zero embedded-interest endpoint

| Fiscal year | NOPAT | D&A | Cash capex | Lease investment | Change WC | Operating cash investment | Full-year FCFF | Included FCFF | Discount years | PV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026 | 8,332.2472 | 2,611.9200 | 5,830.0992 | 141.4800 | -622.3800 | 431.8592 | 5,163.1088 | 4,624.1029 | 0.8932 | 4,318.2503 |
| 2027 | 8,961.6583 | 2,790.3207 | 6,238.2061 | 151.3836 | -594.2852 | 408.1069 | 5,548.5675 | 5,548.5675 | 1.8904 | 4,800.3981 |
| 2028 | 9,547.9434 | 2,954.6572 | 6,612.4985 | 160.4666 | -551.9772 | 374.2924 | 5,907.3203 | 5,907.3203 | 2.9068 | 4,727.8623 |
| 2029 | 10,076.2141 | 3,100.5977 | 6,943.1234 | 168.4899 | -495.5312 | 330.6249 | 6,230.1047 | 6,230.1047 | 3.9041 | 4,619.4015 |
| 2030 | 10,581.2586 | 3,253.9581 | 7,290.2796 | 176.9144 | -484.3587 | 347.1562 | 6,505.2251 | 6,505.2251 | 4.9014 | 4,468.5719 |

## WACC–growth sensitivity — zero embedded-interest endpoint

| WACC | g=2% | g=3% | g=4% |
|---|---:|---:|---:|
| 6.9630% | $376.81 | $438.29 | $540.70 |
| 7.9630% | $310.60 | $347.29 | $402.09 |
| 8.9630% | $263.59 | $286.99 | $319.51 |

Sources:
- Filing: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm (cover, pp. 37, 39, 41, 52–54).
- Treasury: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2025
- Borrowing proxy: https://fred.stlouisfed.org/data/BAMLC0A2CAAEY
- Price: https://www.financecharts.com/compare/VOO%2CCOST/summary/price
- ERP source (published October 6, 2025): https://aswathdamodaran.blogspot.com/2025/10/a-fairly-highly-valued-market-fed-chair.html
- Beta data, method and retrieval record: costco_beta_results.md and costco_beta_sources.json.

