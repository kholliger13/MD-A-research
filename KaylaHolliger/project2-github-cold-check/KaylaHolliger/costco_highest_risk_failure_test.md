# Highest-risk failure test — Costco

Risk: an arithmetically linked model could still report misleading value from an invalid terminal denominator or an unfunded, loss-making business.
Command: python3 -B costco_highest_risk_test.py
Run UTC: 2026-10-19T16:58:07.946388+00:00
Model SHA256: 71d866e8466e8cae66e1045fecf1766a291e78bea668919df4d0e7cacd6d64a0

| Test | Result | Observed behavior |
|---|---|---|
| Terminal growth equals WACC | PASS | Require WACC > growth >= 0 and terminal ROIC > growth. |
| Terminal growth exceeds WACC | PASS | Require WACC > growth >= 0 and terminal ROIC > growth. |
| Terminal ROIC cannot fund assumed growth | PASS | Require WACC > growth >= 0 and terminal ROIC > growth. |
| Nonfinite WACC | PASS | DCF rates must be finite. |
| 6% merchandise-margin loss stress | PASS | All five statement years retained; accounting reconciles; no dividends or immediate tax credits in loss years; cash shortfalls exposed. |
| No unsupported going-concern value for loss stress | PASS | Continuity requires positive NOPAT and reinvestment share between zero and one. |
| Opening-equity mismatch of 1 million | PASS | 2026 balance_gap failed: -1.000000000007276 |
| Restore original base and source integrity | PASS | Source hash unchanged; restored forecast equals fresh module reload. |

Loss-stress minimum forecast cash: -22,733.04 USD million.
Largest required-cash shortfall: 30,023.32 USD million.
Negative cash is an unfunded financing need, not an executable cash balance. No borrowing plug or positive valuation is inserted.
The 6% margin is a deliberate failure probe, not a calibrated downside case or company forecast.

## Model correction recorded

- DCF NOPAT now taxes only positive EBIT, matching the existing no-immediate-loss-tax-benefit policy. Current positive-profit base/scenario outputs are unchanged. Locked capex-test model and records were not modified.

## Limits

- Passing these tests validates specific failure behavior, not forecasts, source completeness or overall valuation accuracy.
- This AI-assisted failure test is distinct from the student’s locked capex prediction and the still-required recorded clean run in a fresh environment.

