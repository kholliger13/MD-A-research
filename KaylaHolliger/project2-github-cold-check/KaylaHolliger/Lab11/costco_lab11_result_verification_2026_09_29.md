# Lab 11 result verification

Base before/after: PASS — independent inputs, opening balances, every forecast field, and all three reported outputs match exactly (zero difference).

Lower/higher input isolation: PASS — only fee_growth or gross_margin changes, at the specified shifts in FY2026–2030. Opening balances and every other independent assumption stay at base.

Linked recalculation: PASS — all seven saved forecasts and valuations exactly match fresh runs of the linked model; EBIT and FCFF change in each lower/higher case.

Accounting checks: PASS on all six scenario runs and restored base. Maximum absolute balance-sheet gap = 2.91038304567e-11 USD million; maximum cash-reconciliation gap = 1.81898940355e-12 USD million; minimum cash headroom = 11,387.05099068 USD million. No failed saved runs require investigation.

Change from base: PASS — every signed change equals scenario output minus its driver’s base output. Maximum difference = 0.

Output spans: PASS — each equals maximum minus minimum across the three valid cases for its driver.

Tolerance: numerical comparisons allow 1e-7 in each output’s units (USD millions for EBIT/FCFF; USD/share for valuation); saved base forecasts and reruns actually match exactly. Accounting-gap tolerance is the model’s 1e-7 USD million. Displayed values round to two decimals (±0.005 output units); subtracting two displayed rounded outputs may differ from the displayed full-precision change by 0.01. Changes and spans are calculated before rounding.
