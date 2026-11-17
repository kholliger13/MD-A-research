# Costco one-at-a-time sensitivity

Run: `../.venv/bin/python COST_proforma_from_ABG.py --sensitivity`

Preserved base input set: `costco_base_rerun_2026_09_29_inputs.json`. Every run uses a fresh deep copy of all assumptions and opening balances. Lower/base/higher are independently rerun for each driver. Only the named driver changes; linked statement quantities recalculate.

Existing ranges: membership growth ±2 percentage points; merchandise margin ±0.25 percentage points. Both apply to FY2026–2030. Input percentages below are displayed to six decimals; JSON retains full precision. No other independent assumptions change.

Operating profit = EBIT. FCFF = signed free cash flow to the firm after operating-cash investment. Profit, FCFF and their changes/spans are USD millions; value and its changes/span are USD/share. Changes are scenario minus that driver’s independently rerun base. No positive-only cash-flow subtotal is used.

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

## Visible accounting checks

| Run | Opening balance | FY2026–2030 balance sheets | Cash reconciliation | Minimum cash |
|---|---|---|---|---|
| fee_growth / Lower | PASS | PASS | PASS | PASS |
| fee_growth / Base | PASS | PASS | PASS | PASS |
| fee_growth / Higher | PASS | PASS | PASS | PASS |
| gross_margin / Lower | PASS | PASS | PASS | PASS |
| gross_margin / Base | PASS | PASS | PASS | PASS |
| gross_margin / Higher | PASS | PASS | PASS | PASS |
| Final / Restored base | PASS | PASS | PASS | PASS |

Invalid runs are flagged and excluded from spans; no ranking is produced. Valuation availability is evaluated separately with the existing valuation rules. Signed annual cash flows remain in the trace files.

Final base rerun: exact forecast and value match both driver base runs. All independent inputs restored to the preserved base.

Full linked statement fields, annual check gaps and valuation components: `costco_operating_sensitivity_2026_09_29_full_output.md`. Exact inputs and results: `costco_operating_sensitivity_2026_09_29_runs.json`.
