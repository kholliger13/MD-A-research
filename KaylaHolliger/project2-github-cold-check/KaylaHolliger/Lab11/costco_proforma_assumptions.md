# Costco: five years of statements and their implied value

Prepared September 24, 2026. USD millions except per-share amounts.
Working folder: `/Users/kaylaholliger/Documents/Courses/AIFinance2026/KaylaHolliger`.

This is a normalized FY2025-base classroom model, with FY2026–2030 treated as forecast periods. It uses FY2025 financial information, not subsequent results. Values are discounted to the beginning of the forecast horizon; this is not a September 2026 market valuation or an estimate made with information available at the FY2025 closing date (the annual filing was published later).

## Result

The base case implies $155.49 billion of equity value, or **$349.58 per diluted share**. The first five years of operating free cash flow contribute $24.39 billion of present value. Continuing operations after 2030 contribute $127.02 billion, producing enterprise value of $151.41 billion. Add $8.763 billion excess cash and $1.123 billion investments and subtract $5.805 billion debt.

The 7%–9% discount-rate / 2%–4% perpetual-growth grid spans **$266.79–$539.38 per share**. This is a sensitivity range, not a confidence interval. Approximately 84% of enterprise value comes from the terminal period.

## Evidence and assumptions

Historical inputs are from [Costco FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm), statements on printed pages 37, 39 and 41, with debt in Note 4. FY2025 net sales grew about 8%; comparable sales grew 6%. Membership fees rose about 10%. Warehouses increased from 890 to 914. The filing reports sales of $269,912 million, fees of $5,323 million, merchandise costs of $239,886 million, SG&A of $24,966 million, depreciation of $2,426 million and capital spending of $5,498 million.

Every forecast input below is an analyst assumption, not company guidance.

| Driver | Forecast | Defense and limitation |
|---|---|---|
| Net sales | 8%, 7%, 6%, 5%, 4% growth | Start near the observed growth rate, then reduce growth as the business becomes larger. First-year intuition: roughly 5% comparable growth plus 3% expansion; no separate expansion uplift is added. This is a judgmental slowdown, not a statistical estimate. |
| Membership revenue | 9%, 8%, 7%, 6%, 5% growth | Begin below recent growth and gradually fade; do not repeat a fee-increase benefit indefinitely. |
| Merchandise gross margin | 11.1244% of net sales | Hold the base-year percentage. No speculative merchandise margin expansion. |
| SG&A | 9.2497% of net sales | Hold base efficiency; do not assume wages or technology become cheaper relative to sales. Depreciation is already included in costs and is not deducted twice. |
| D&A | 0.8988% of sales | Base-year ratio; a simplified substitute for an asset-vintage schedule. |
| Capital expenditure | 2% of net sales | Approximately maintains base-year investment intensity. Explicitly funds expansion rather than treating net income as cash flow. |
| Working capital | Constant base ratios | Inventory and payable days remain unchanged at constant margins. Receivables, other current assets, salaries and rewards scale with sales; deferred fees scale with fee revenue. Supplier and membership funding creates a cash source as sales rise. |
| Operating cash | 2% of sales | Judgmental liquidity reserve, approximately one week of sales. Reserve increases are deducted from free cash flow; only starting cash above the reserve enters the equity bridge. |
| Tax rate | 25.1% | Rounded base-year effective rate; no assumed tax windfall. |
| Debt and cash interest | 4% and 3% | Normalized financing assumptions, not current quoted yields. Debt is refinanced at unchanged principal. These affect projected earnings, but are excluded from operating free cash flow valuation. |
| Distributions | 30% of net income in ordinary dividends | Modeling policy, not a prediction. No special dividend or discretionary repurchase is assumed. Residual cash accumulates. |
| Discount rate | 8%; test 7%–9% | An explicit required-return judgment. Illustrative equity-cost decomposition: 4% risk-free assumption + 0.8 beta assumption × 5% equity-risk-premium assumption = 8%. All three are scenario inputs, not contemporaneous market estimates. With little debt relative to modeled enterprise value, using 8% for the firm is a rounded approximation. A current investment valuation requires date-matched Treasury, beta, premium and financing data. |
| Perpetual growth | 3%; test 2%–4% | Nominal long-run assumption, below the final forecast sales-growth rate. Not a perpetual continuation of near-term growth. |
| Terminal incremental return on capital | 20% | Judgment that an established retailer can reinvest profitably; not a measured Costco ROIC. At 3% growth, 15% of after-tax operating profit must be reinvested. This is a material valuation assumption. |
| Diluted shares | 444.803 million | Historical diluted weighted-average proxy held constant; not a current fully diluted share count. |

## How the statements connect

Revenue less merchandise costs and SG&A produces operating income. Interest and taxes produce net income. Cash flow adds back depreciation, adjusts for changes in operating working capital, and deducts capital spending and dividends. Property and equipment rolls forward through capital spending and depreciation. Equity rolls forward through income and dividends. Cash is calculated from cash flows, rather than plugged to force the balance sheet to balance.

Operating free cash flow = operating income × (1 − tax rate) + depreciation − capital spending − increase in operating working capital − increase in required operating cash.

The valuation excludes interest income and financing costs from operating cash flow. Operating leases remain operating expenses; their liabilities are not separately subtracted as financial debt. Starting financial debt includes the current portion, removed from the aggregated other-liability balance to avoid double counting.

Terminal free cash flow = FY2030 after-tax operating profit × (1 + perpetual growth) × (1 − perpetual growth / terminal return on capital). Discount this terminal value and all annual forecast flows using year-end timing.

The terminal convention implies about $9.33 billion in FY2031 free cash flow versus $6.83 billion in FY2030: reinvestment drops as the model enters maturity. This step is material, not an unexplained growth acceleration. A gradual transition or lower terminal return on capital would reduce value; the included WACC/growth grid does not capture all operating and reinvestment risks.

## Simplifications to review

These are aggregated normalized statements, not a full GAAP forecast. Other long-term assets and aggregated other liabilities (including leases) are held constant. Lease additions are assumed to offset amortization and principal reductions; rent remains in operating costs. No acquisitions, currency translation, impairments or deferred-tax changes are forecast. Depreciation is assigned to PP&E for simplicity.

Compensation is treated as a cash-equivalent economic expense: no stock-compensation addback, award issuance or related withholding is forecast. This avoids treating ongoing compensation as free cash, but differs from reported cash-flow accounting. Share count stays fixed. Model checks establish arithmetic consistency, not forecasting accuracy.

The former $440.22 training DCF grew an aggregate cash-flow proxy. This model explicitly forecasts operations and reinvestment, reserves operating cash, and applies a separate terminal reinvestment requirement. Its lower estimate is not caused by a change in the base 8% discount rate.

## Files and verification

Negative-flow handling added: build all five years even during losses; dividends are zero when net income is negative, and no immediate tax benefit is assumed on losses. FCFE equals operating cash flow less capital spending and required operating-cash investment, with zero net borrowing. Label negative years "negative FCFE". The separate positive-only five-year subtotal discounts only positive FCFE at an assumed 8% cost of equity; it excludes shortfalls and terminal value and is not full equity value. The original FCFF valuation retains signed forecast flows and is withheld if final-year or terminal FCFF is nonpositive. Cash-floor failures are displayed as unfunded shortfalls requiring financing rather than silently plugged or used to stop statement generation. A loss stress case with a 6% merchandise margin verified these behaviors.

Run `.venv/bin/python COST_proforma.py`. `costco_proforma_output.md` contains the three forecast statements and sensitivity grid. All five balance sheets balance, cash movements reconcile, and the operating-cash floor is satisfied.

Prepared for FIN 43900 as an educational exercise with AI assistance. Sources checked by the assistant; assumptions and conclusions require student review. Not investment research or personal investment advice.
