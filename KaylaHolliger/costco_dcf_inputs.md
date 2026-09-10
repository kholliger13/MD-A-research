# Costco DCF inputs and price

used for educational purposes, not financial advice

Amounts are USD millions except stock prices. Base financial year: FY2025, ended August 31, 2025. Sources checked September 10, 2026.

| Input | Value used | Status and source |
|---|---:|---|
| Starting FCFF | 7,952.346 | Derived: 13,335 operating cash flow + 154 interest expense × (1 − 25.1% tax rate) − 5,498 capital expenditures; [10-K](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm), pp. 28, 37, 40. |
| Growth, Years 1–5 | 8%, 7%, 6%, 5%, 4% | **Unresolved — PLACEHOLDER**: retains previous model's training values; not company guidance. |
| Years | 5 | Assignment forecast horizon. |
| WACC | 8% | **Unresolved — PLACEHOLDER**: retains previous model's training value; market-based cost of capital has not been established. |
| Terminal growth | 3% | **Unresolved — PLACEHOLDER**: retains previous model's training value; not supplied by the filing. |
| Cash | 14,161 | FY2025 10-K balance sheet, p. 39; cash and cash equivalents only. |
| Debt | 5,805 | FY2025 10-K, Note 4, p. 52; carrying value including current portion. |
| Diluted shares | 444.803 million | FY2025 10-K income statement, p. 37; weighted-average diluted shares. |
| Market price | $902.60 per share | September 9, 2026 closing price; [FinancialContent historical prices](https://www.financialcontent.com/quote/NQ%3ACOST/historical). This is a dated quote, not a live price. |

Run `python dcf_kaylaholliger_9_10_26.py` (or `python3 dcf_kaylaholliger_9_10_26.py` if needed). The script prints twelve lines. The editable inputs block uses the values above.

The training DCF price is calculated as (enterprise value + cash − debt) ÷ diluted shares. It uses a simplified FCFF proxy and placeholder forecast assumptions. It excludes short-term investments from the equity bridge and uses historical weighted-average diluted shares rather than a current fully diluted share count. The base financials and market quote have different dates; this is a classroom comparison, not a current investment valuation. See `costco_dcf_training_notes.md` for calculation steps and further limitations.
