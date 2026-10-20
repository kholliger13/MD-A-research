# Costco historical beta calculation

```text
COST historical beta — 60 monthly raw returns, October 2020–September 2025
SPY dividend-adjusted proxy (main): beta=0.975320; monthly intercept=0.636493%; R-squared=0.4307; beta standard error=0.147233
S&P 500 price index (definition comparison): beta=0.977885; monthly intercept=0.749358%; R-squared=0.4310; beta standard error=0.147539
No post-September 2025 return observations used. Historical data retrieved October 19, 2026.
Limitations: raw rather than excess returns; provider adjustments retrieved later; beta depends on period/benchmark and is not a complete risk measure.
```

Method: ordinary least squares with an intercept; beta = covariance(COST monthly returns, SPY monthly returns) / variance(SPY monthly returns). 61 month-end levels produce 60 monthly returns. Source URLs and full retrieved provider payloads are preserved in costco_beta_sources.json. SPY is an ETF proxy, not the exact S&P 500 total-return index.

Verification: synthetic slope-2 fixture PASS; independent uncentered-sums slope formula PASS; contiguous months, matching trading dates and positive finite prices PASS. These checks do not replace the assignment training-case reconciliation or human AI-off locked test.

Provisional cost of equity: 4.13% + 0.975320 × 3.77% = approximately 7.81%. ERP public availability by October 8, 2025 still needs corroboration; WACC also needs debt costs, financing weights and tax-shield review. No final WACC is asserted.
