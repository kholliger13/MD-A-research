# Costco revised model — provisional statement integration

Run date: October 19, 2026. USD millions. FY2025 opening balances; FY2026–2030 forecast.
Not a final October 8, 2025 valuation. Source review remains pending. Use --dcf for a separately labeled provisional valuation with timing estimates.

Source: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm (pp. 39, 41, 52–54).

## Forecast assumptions and limits

- Sales growth: 8%, 7%, 6%, 5%, 5%; fee growth: 9%, 8%, 7%, 6%, 5%; tax: 26.1%. These are provisional analyst assumptions.
- Borrowings net: 5,788; finance leases: 1,479; operating leases: 2,668; remaining liabilities including working-capital items: 38,000.
- New finance-lease assets are noncash additions with equal liability additions; they are not cash capex or cash borrowing proceeds. Principal payments are financing cash outflows.
- Finance-lease amortization is separated from existing expense ratios and replaced by the schedule amount. Total D&A is added back once.
- Finance-lease additions scale from 131 with sales; amortization uses 102/1,488 of opening assets; principal uses 147/1,479 of opening liabilities; interest uses 4.63% of opening liabilities. These are simplifying assumptions, not contractual payments.
- Provisional D&A allocation: 2,426 less 102 finance-lease amortization is assigned to PP&E. Verify remaining amortization before finalizing.
- Operating lease assets/liabilities and other residual balances remain constant. Replacement lease activity and accounting are simplified.
- Borrowings are refinanced at constant principal; their 17 discount/cost balance is held constant. Assumed interest is 4%.
- Finance-lease interest is provisionally placed below EBIT. Note 5 says some interest is in merchandise costs, but does not quantify that split; expense allocation remains unresolved. The default statements use zero embedded interest; --dcf compares both allocation endpoints.
- Stock compensation remains an economic expense, with no forecast addback or new award issuance; historical GAAP cash-flow reconciliation remains separate.
- This is a simultaneous integration run, not a cold run or human-authored locked changed-input test.

## Income statement

| Item | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Net sales | 291,504.96 | 311,910.31 | 330,624.93 | 347,156.17 | 364,513.98 |
| Membership fees | 5,802.07 | 6,266.24 | 6,704.87 | 7,107.16 | 7,462.52 |
| Total revenue | 297,307.03 | 318,176.54 | 337,329.80 | 354,263.34 | 371,976.50 |
| Merchandise costs + SG&A before finance-lease amortization | 285,930.00 | 305,945.10 | 324,301.81 | 340,516.90 | 357,542.74 |
| Finance-lease amortization | 102.00 | 104.71 | 107.91 | 111.51 | 115.41 |
| Operating income | 11,275.03 | 12,126.74 | 12,920.09 | 13,634.93 | 14,318.35 |
| Borrowing interest | 232.20 | 232.20 | 232.20 | 232.20 | 232.20 |
| Finance-lease interest | 68.48 | 68.22 | 68.45 | 69.08 | 70.01 |
| Interest income | 458.52 | 553.66 | 655.79 | 764.22 | 878.15 |
| Pretax income | 11,432.87 | 12,379.98 | 13,275.22 | 14,097.87 | 14,894.28 |
| Income taxes | 2,983.98 | 3,231.17 | 3,464.83 | 3,679.55 | 3,887.41 |
| Net income | 8,448.89 | 9,148.80 | 9,810.39 | 10,418.33 | 11,006.87 |

## Balance sheet

| Item | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Cash | 17,332.43 | 20,736.54 | 24,351.00 | 28,148.55 | 32,151.11 |
| Investments | 1,123.00 | 1,123.00 | 1,123.00 | 1,123.00 | 1,123.00 |
| Receivables | 3,459.24 | 3,701.39 | 3,923.47 | 4,119.64 | 4,325.63 |
| Inventory | 19,565.28 | 20,934.85 | 22,190.94 | 23,300.49 | 24,465.51 |
| Other Current Assets | 1,919.16 | 2,053.50 | 2,176.71 | 2,285.55 | 2,399.82 |
| Ppe | 35,229.18 | 38,781.77 | 42,547.52 | 46,501.55 | 50,653.29 |
| Other Assets Ex Finance Leases | 5,322.00 | 5,322.00 | 5,322.00 | 5,322.00 | 5,322.00 |
| Finance Lease Asset | 1,527.48 | 1,574.16 | 1,626.72 | 1,683.70 | 1,745.20 |
| Assets | 85,477.76 | 94,227.20 | 103,261.36 | 112,484.48 | 122,185.56 |
| Payable | 21,365.64 | 22,861.23 | 24,232.91 | 25,444.55 | 26,716.78 |
| Salaries | 5,621.40 | 6,014.90 | 6,375.79 | 6,694.58 | 7,029.31 |
| Rewards | 2,891.16 | 3,093.54 | 3,279.15 | 3,443.11 | 3,615.27 |
| Deferred Fees | 3,110.86 | 3,359.73 | 3,594.91 | 3,810.60 | 4,001.13 |
| Remaining Liabilities | 7,481.00 | 7,481.00 | 7,481.00 | 7,481.00 | 7,481.00 |
| Finance Lease Liability | 1,473.48 | 1,478.41 | 1,491.94 | 1,512.14 | 1,538.76 |
| Borrowings net | 5,788.00 | 5,788.00 | 5,788.00 | 5,788.00 | 5,788.00 |
| Operating lease liabilities | 2,668.00 | 2,668.00 | 2,668.00 | 2,668.00 | 2,668.00 |
| Liabilities | 50,399.54 | 52,744.82 | 54,911.70 | 56,841.99 | 58,838.26 |
| Equity | 35,078.22 | 41,482.39 | 48,349.66 | 55,642.49 | 63,347.30 |

## Cash flow and noncash lease activity

| Item | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Net income | 8,448.89 | 9,148.80 | 9,810.39 | 10,418.33 | 11,006.87 |
| D&A addback | 2,611.92 | 2,790.32 | 2,954.66 | 3,100.60 | 3,253.96 |
| Increase in working capital (deduct) | -622.38 | -594.29 | -551.98 | -495.53 | -484.36 |
| Operating cash flow | 11,683.19 | 12,533.41 | 13,317.02 | 14,014.46 | 14,745.19 |
| Cash capex | 5,830.10 | 6,238.21 | 6,612.50 | 6,943.12 | 7,290.28 |
| Investing cash flow | -5,830.10 | -6,238.21 | -6,612.50 | -6,943.12 | -7,290.28 |
| Dividends | 2,534.67 | 2,744.64 | 2,943.12 | 3,125.50 | 3,302.06 |
| Finance-lease principal paid | 147.00 | 146.45 | 146.94 | 148.29 | 150.29 |
| Financing cash flow | -2,681.67 | -2,891.09 | -3,090.06 | -3,273.78 | -3,452.36 |
| Change in cash | 3,171.43 | 3,404.11 | 3,614.47 | 3,797.55 | 4,002.56 |
| Closing cash | 17,332.43 | 20,736.54 | 24,351.00 | 28,148.55 | 32,151.11 |
| Noncash lease additions (disclosure only) | 141.48 | 151.38 | 160.47 | 168.49 | 176.91 |

## Checks

| Item | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Balance Gap | -0.00 | 0.00 | -0.00 | 0.00 | -0.00 |
| Cash Gap | -0.00 | 0.00 | -0.00 | 0.00 | 0.00 |
| Lease Asset Gap | 0.00 | 0.00 | 0.00 | -0.00 | 0.00 |
| Lease Liability Gap | 0.00 | 0.00 | 0.00 | -0.00 | 0.00 |
| Cash Floor Shortfall | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

