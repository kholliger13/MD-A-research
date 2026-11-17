# Lab 11 — Costco sensitivity analysis

Individual submission: Kayla Holliger  
Company: Costco (COST)  
Partner company: Deere & Company (DE / John Deere)

Status: Draft awaiting the previously locked prediction and the actual partner exchange/analysis. Costco calculations and verification are complete.

## Two operating drivers and visible results

The two independent inputs are membership-fee revenue growth (`fee_growth`) and merchandise gross margin (`gross_margin`) in the existing Costco model. Ranges are labelled judgments: ±2 percentage points of membership growth and ±0.25 percentage points of merchandise margin, each applied in FY2026–2030. The separate saved base is copied afresh for each run. All other independent inputs and opening balances remain at base; the linked statements recalculate.

## fee_growth

Input units: annual membership-fee revenue growth (%) by FY2026, 2027, 2028, 2029, 2030.

| Run | Actual input (%) | FY2030 EBIT | Δ EBIT | FY2030 FCFF | Δ FCFF | Value/share | Δ value/share | Checks |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Lower | 7.000000, 6.000000, 5.000000, 4.000000, 3.000000 | 13,558.97 | -671.96 | 6,243.30 | -587.78 | 333.07 | -16.51 | PASS |
| Base | 9.000000, 8.000000, 7.000000, 6.000000, 5.000000 | 14,230.93 | +0.00 | 6,831.08 | +0.00 | 349.58 | +0.00 | PASS |
| Higher | 11.000000, 10.000000, 9.000000, 8.000000, 7.000000 | 14,955.06 | +724.13 | 7,470.07 | +639.00 | 367.31 | +17.73 | PASS |

| Output | Span (maximum − minimum) | Valid cases |
|---|---:|---:|
| operating_profit | 1,396.08 | 3/3 |
| fcff | 1,226.78 | 3/3 |
| value_per_share | 34.24 | 3/3 |

## gross_margin

Input units: merchandise gross margin (% of net sales), same value in each FY2026–2030 year.

| Run | Actual input (%) | FY2030 EBIT | Δ EBIT | FY2030 FCFF | Δ FCFF | Value/share | Δ value/share | Checks |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Lower | 10.874366 | 13,328.32 | -902.61 | 6,155.03 | -676.05 | 325.99 | -23.59 | PASS |
| Base | 11.124366 | 14,230.93 | +0.00 | 6,831.08 | +0.00 | 349.58 | +0.00 | PASS |
| Higher | 11.374366 | 15,133.54 | +902.61 | 7,507.13 | +676.05 | 373.17 | +23.59 | PASS |

| Output | Span (maximum − minimum) | Valid cases |
|---|---:|---:|
| operating_profit | 1,805.21 | 3/3 |
| fcff | 1,352.10 | 3/3 |
| value_per_share | 47.18 | 3/3 |

Operating profit is EBIT; free cash flow is FCFF after operating-cash investment. EBIT, FCFF, their changes and spans are USD millions. Value per share, its change and span are USD/share. Changes are scenario minus the corresponding base. All signed annual cash flows are retained. The existing FCFF valuation is available for every tested case, with WACC 8%, terminal growth 3%, and terminal incremental ROIC 20% unchanged.

## Restored-base and calculation checks

Base before/after: PASS — independent inputs, opening balances, every forecast field, and all three reported outputs match exactly (zero difference).

Lower/higher input isolation: PASS — only fee_growth or gross_margin changes, at the specified shifts in FY2026–2030. Opening balances and every other independent assumption stay at base.

Linked recalculation: PASS — all seven saved forecasts and valuations exactly match fresh runs of the linked model; EBIT and FCFF change in each lower/higher case.

Accounting checks: PASS on all six scenario runs and restored base. Maximum absolute balance-sheet gap = 2.91038304567e-11 USD million; maximum cash-reconciliation gap = 1.81898940355e-12 USD million; minimum cash headroom = 11,387.05099068 USD million. No failed saved runs require investigation.

Change from base: PASS — every signed change equals scenario output minus its driver’s base output. Maximum difference = 0.

Output spans: PASS — each equals maximum minus minimum across the three valid cases for its driver.

Tolerance: numerical comparisons allow 1e-7 in each output’s units (USD millions for EBIT/FCFF; USD/share for valuation); saved base forecasts and reruns actually match exactly. Accounting-gap tolerance is the model’s 1e-7 USD million. Displayed values round to two decimals (±0.005 output units); subtracting two displayed rounded outputs may differ from the displayed full-precision change by 0.01. Changes and spans are calculated before rounding.

Visible restored-base outputs: FY2030 EBIT **14,230.93 USD million**; FY2030 FCFF **6,831.08 USD million**; value **349.58 USD/share**. Inputs and the complete forecast match the first base run exactly. All seven runs pass opening-balance, forecast balance-sheet, cash-reconciliation, and minimum-cash checks.

## Main driver over the tested ranges

Over these ranges, merchandise gross margin produces the larger span for FY2030 operating profit, FY2030 FCFF, and value per share. Higher margin reduces merchandise costs at unchanged sales and SG&A, increasing operating profit and after-tax cash flow; FY2030 profit also affects terminal value. A bigger span can reflect the chosen input range, not an inherently more important driver.

## Locked prediction and reconciliation — pending

Previously recorded prediction: **Not yet provided.**

Time or evidence that it was locked before viewing results: **Not yet provided.**

Reconciliation to the observed results: **Pending the original prediction.** The observed output spans above are available for comparison. A prediction written after these results cannot be labelled a previously locked prediction.

## Partner exchange — Deere & Company (DE / John Deere) — pending

Actual question asked and who asked it: **Not yet provided.**

Actual partner response: **Not yet provided.**

Suggested question to ask if the exchange has not occurred: “For Deere, which of your two independent operating inputs produces the larger final-year operating-profit and free-cash-flow span over your tested ranges? What are the exact ranges, and does your restored base match the initial base?”

## Check of the partner’s analysis — pending

Partner table or model evidence: **Not yet provided.**

Check actually performed on Deere’s analysis: **Not yet performed; no partner results were supplied.**

Proposed check, once the partner provides results: recompute one signed change as scenario output minus base output, using their FCFF or FCFE definition and units; compare with their reported change within the stated rounding tolerance. Record the exact scenario, operands, calculation, reported result, and pass/fail conclusion. If raw results are available, also verify each span as maximum minus minimum and compare restored-base outputs.

## Supporting files and reproducibility

- Model command: `../.venv/bin/python COST_proforma_from_ABG.py --sensitivity`
- Model: `COST_proforma_from_ABG.py`
- Analysis: `costco_operating_sensitivity_2026_09_29.py`
- Preserved base inputs: `costco_base_rerun_2026_09_29_inputs.json`
- Exact inputs, forecasts, differences, spans, restored base: `costco_operating_sensitivity_2026_09_29_runs.json`
- Full visible statement traces and check gaps: `costco_operating_sensitivity_2026_09_29_full_output.md`

Prepared for FIN 43900 as an individual educational exercise with AI assistance. Partner contributions must be recorded from the actual exchange before this draft is complete.
