# Costco reverse DCF — conditional market-implied margin

Calculated October 19, 2026; valuation date October 8, 2025. USD/share unless noted.

## Sales-only diagnostic

- Held fee growth, merchandise margin, SG&A intensity, capital-spending intensity, WACC and terminal convention fixed; shifted all five sales growth rates by the same amount.
- Base sales schedule gives $267.53; +10 percentage points in each year gives $277.93.
- Target $914.80 is not bracketed on the tested +0 to +10 percentage-point grid. No sales-growth solution is asserted. Wider extrapolation is not assumed monotonic: reinvestment can offset sales growth.

## Reverse-margin method

- Solve for a single merchandise gross margin applied in FY2026–2030. Keep base sales growth 8%, 7%, 6%, 5%, 5%; fee growth 9%, 8%, 7%, 6%, 5%; SG&A ratio 9.2497%; cash capex 2%; tax 26.1%; cash reserve 2%; and other model assumptions fixed.
- WACC 7.9630%; terminal growth 3%; continuity terminal FCFF. The final reinvestment share and implied ROIC recalculate as linked outputs, not fixed independent inputs.
- Search bracket: base gross margin to 20%. Check a 21-point price grid for increasing values, then bisect to a $0.000001/share price tolerance; reject unbracketed targets rather than clipping.
- Compare both expense-allocation endpoints. The market price is matched mathematically; no operating plausibility is implied.

| Historical lease-interest allocation | Solved gross margin | Increase vs base (percentage points) | Matched price |
|---|---:|---:|---:|
| 0 million | 17.1146% | 5.9902 | $914.800000 |
| 63 million | 17.0912% | 5.9669 | $914.800000 |

## Interpretation

- These margins ask what would be required if margin alone explained the price gap. Investors could instead assume different growth, membership economics, reinvestment, discount rates, or a combination.
- A substantially higher margin could conflict with the low-price business model, change customer demand, or require different SG&A. Those feedback effects are excluded in this one-input diagnostic.
- This is not evidence that investors actually expect the solved margin, and it is not proof of mispricing.
- All source, proxy, share-count, stub-timing and terminal limitations in costco_project1_provisional_dcf.md and costco_project1_scenarios.md remain.
- This AI-assisted analysis is not the human-authored AI-off locked changed-input test.

