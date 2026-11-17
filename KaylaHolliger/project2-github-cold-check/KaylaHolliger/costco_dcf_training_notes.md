# Costco Python DCF — training model

used for educational purposes, not financial advice

Run `python dcf_kaylaholliger_9_10_26.py` from this folder. No packages are required. Edit the assumptions near the top of the script to explore different outcomes.

DCF (discounted cash flow) estimates business value by converting future cash flows into today's dollars. All amounts here are **USD millions**, using fiscal 2025 as the base year.

| Input | Training value | Source / status |
|---|---:|---|
| Starting FCFF | $7,952.346 million | Derived from the linked 10-K: operating cash flow $13,335 million, capital expenditures $5,498 million (p. 40), interest expense $154 million (p. 37), and effective tax rate 25.1% (p. 28). |
| Growth, Years 1–5 | 8%, 7%, 6%, 5%, 4% | Model author's illustrative declining-growth assumptions; not company forecasts. |
| Years | 5 | Assignment's Years 1–5 horizon. |
| WACC | 8% | Model author's training assumption; not a calculated market rate or a figure from the filing. |
| Terminal growth | 3% | Model author's training assumption for annual growth after year 5; not from the filing. |

Source: [Costco FY2025 Form 10-K, fiscal year ended August 31, 2025](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm). Page references are the printed filing pages.

The request repeats “Terminal growth.” This model uses it once and shows “Years” separately to provide five input lines.

## How the calculation works

1. Starting free cash flow to the firm (FCFF) = operating cash flow + interest expense × (1 − tax rate) − capital expenditures = 13,335 + 154 × 0.749 − 5,498 = **7,952.346**.
2. Each year's FCFF = previous year's FCFF × (1 + that year's growth rate).
3. Present value of each forecast = FCFF ÷ (1 + WACC)^year. WACC means weighted average cost of capital, the discount rate for the business.
4. Terminal value = year 5 FCFF × (1 + terminal growth) ÷ (WACC − terminal growth). It represents all cash flows after year 5, valued at the end of year 5.
5. Enterprise value = present values of years 1–5 + discounted terminal value.

## Interpretation and limitations

This is a simplified FCFF proxy using reported operating cash flow, an interest-expense add-back, and the effective tax rate. It does not normalize working capital, nonoperating income, stock compensation, or unusual cash flows; interest expense also need not equal cash interest paid. A full operating valuation would refine these items. Forecasts use year-end discounting.

The assumed WACC and growth rates make this a training scenario, not a current valuation. WACC must exceed terminal growth. The terminal value can dominate the result: try raising WACC from 8% to 9% and explain why value falls. Enterprise value is not a share price; an equity valuation requires additional adjustments and a suitable share count.

Prepared with AI assistance for FIN 43900 (AI Finance Applications, Purdue) as a learning exercise. Filing figures were checked by the assistant; the student should review the inputs and assumptions before submission.
