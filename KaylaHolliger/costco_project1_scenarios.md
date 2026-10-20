# Costco operating scenarios — provisional continuity DCF

Calculated October 19, 2026; valuation date October 8, 2025. USD millions except per-share amounts.
These are analyst scenarios, not forecasts with assigned probabilities or a final valuation recommendation.

## Common assumptions

- WACC 7.9630%, terminal growth 3%, capex 2% of net sales, tax 26.1%, required cash 2% of sales.
- Continuity terminal convention: terminal FCFF = final-year FCFF × 1.03. Each case retains its own final-year reinvestment share; implied terminal ROIC is derived, not measured Costco ROIC.
- All prior DCF source/definition limits still apply: corporate yield proxy, financing weights, valuation-date diluted shares, expense/D&A allocation, and interpolated balance-sheet amounts.
- Values span only the 0–63 historical finance-lease-interest allocation endpoints; there is no averaging or probability weighting.
- Uniform first-year FCFF proration excludes 38/364 of FY2026; cash and lease liabilities are estimated at October 8 separately in each run.
- Operating assumptions are simultaneous causal scenarios; these runs do not replace a human AI-off prediction, locked changed-input test, or fresh-environment cold run.

## Scenario inputs

| Case | Sales growth FY2026–30 | Fee growth FY2026–30 | Gross margin | SG&A / net sales |
|---|---|---|---:|---:|
| downside | 5%, 4%, 3%, 3%, 3% | 7%, 6%, 5%, 4%, 3% | 10.8744% | 9.3497% |
| base | 8%, 7%, 6%, 5%, 5% | 9%, 8%, 7%, 6%, 5% | 11.1244% | 9.2497% |
| upside | 9%, 8%, 7%, 6%, 6% | 10%, 9%, 8%, 7%, 6% | 11.2744% | 9.1497% |

## Scenario outputs

| Case | Value/share: allocation 0–63 | FY2030 EBIT (allocation 0) | FY2030 FCFF (allocation 0) | Terminal share of EV | Implied terminal ROIC | Statement checks | Cash floor |
|---|---:|---:|---:|---:|---:|---|---|
| downside | $209.59–$211.84 | 11,710.18 | 5,019.09 | 79.54% | 7.14% | PASS | PASS |
| base | $267.53–$270.05 | 14,318.35 | 6,505.23 | 80.17% | 7.79% | PASS | PASS |
| upside | $308.16–$310.79 | 15,962.24 | 7,546.96 | 80.47% | 8.33% | PASS | PASS |

## WACC–growth grid — base case, zero embedded-interest allocation

| WACC | g=2% | g=3% | g=4% |
|---|---:|---:|---:|
| 6.9630% | $276.55 | $333.74 | $429.52 |
| 7.9630% | $230.88 | $267.53 | $322.67 |
| 8.9630% | $198.34 | $223.54 | $258.89 |

## Interpretation and outstanding work

- These results replace neither peer valuation nor reverse DCF. Test separate capital-spending/working-capital stresses before finalizing the recommendation.
- Continuity avoids the original terminal reinvestment cliff but does not prove the retained reinvestment share is sustainable. A five-year fade or measured long-term return assumption could produce different results.
- Original --dcf output retains the 20% ROIC convention explicitly as an alternative; --scenarios uses continuity. Label both outputs to prevent mixing conventions.
- Full scenario inputs, statement traces, bridges and check gaps are in costco_project1_scenario_runs.json.
- Sources and other limitations are documented in costco_project1_provisional_dcf.md and costco_beta_results.md.

