# ERP source review and current valuation update — October 19, 2026

## Source decision

- Previous working ERP: 3.77%, located in a later-captured October webpage variant; publication before October 8 had not been established.
- New working ERP: 4.01%, explicitly described in Damodaran’s dated October 6, 2025 article as the end-September implied premium (8.17% expected market return minus 4.16% Treasury). This is not claimed to be the same payout/model variant as the old snapshot.
- Source: https://aswathdamodaran.blogspot.com/2025/10/a-fairly-highly-valued-market-fed-chair.html ; section 3, The Investing Alternatives, implied-premium discussion.
- Retain October 8 Treasury input 4.13% and raw beta 0.975320. This combines the latest identified monthly premium with valuation-date risk-free yield; no US default adjustment applied to either nominal-Treasury convention.
- Cost of equity: 8.041033%. WACC: 7.732851% → 7.963039%. Only ERP changed as an independent input.

## Scenario update

| Case | Previous value/share | Current value/share |
|---|---:|---:|
| downside | $219.44–$221.80 | $209.59–$211.84 |
| base | $280.29–$282.93 | $267.53–$270.05 |
| upside | $322.96–$325.72 | $308.16–$310.79 |

## Verification and provenance

- PASS: all six operating runs reconcile balance sheets, cash and leases; cash-floor checks pass.
- PASS: continuity terminal growth, equity-to-share conversion, WACC/growth directional checks and reverse-target matching.
- PASS: SHA256 checks confirm the locked prediction, frozen model, actual results and reconciliation were unchanged.
- Previous code and outputs preserved under before_erp_source_update_2026_10_19/. Current generated reports use the new ERP.
- Historical lab reports, beta calculation report and capex locked record describe earlier runs; do not rewrite them or mix their valuation results with the current model.
- Remaining limitations: borrowing-cost proxy, dated financing values, diluted-share proxy, stub balance estimates, lease/D&A allocation, terminal reinvestment, and peer-period differences.
- Recommendation remains provisional watch/defer; this source update alone does not settle investment judgment.

