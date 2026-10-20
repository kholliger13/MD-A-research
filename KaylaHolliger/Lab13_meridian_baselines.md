# Lab 13 — Meridian baseline portfolios

All return, volatility and correlation inputs below are course-authored training values, not market estimates. These are three new four-sleeve baselines, distinct from candidates A–D in the earlier mandate exercise. The Lab 13 expected-return objective is 6.5%. No separate fee or inflation inputs were supplied, so this comparison does not establish achievement of the original CPI + 4% net objective.

| Sleeve | Expected return | Volatility |
|---|---:|---:|
| Treasury bills | 3.5% | 0.5% |
| Treasury 10-year note | 4.3% | 7.0% |
| Investment-grade bond fund | 5.0% | 6.0% |
| Global equity index fund | 8.0% | 16.0% |

| Correlation | Bills | 10-year | IG bonds | Equity |
|---|---:|---:|---:|---:|
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | -0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | -0.10 | 0.25 | 1.00 |

Expected portfolio return is the weighted average of sleeve returns. Covariance equals correlation times the two sleeve volatilities. Portfolio volatility is the square root of w-transpose × covariance × w, so it accounts for how the sleeves move together. Inverse-volatility weights equal (1 / sleeve volatility) divided by the sum of all four inverse volatilities; this does not necessarily equalize contributions to portfolio risk.

| Baseline | Bills | 10-year | IG bonds | Equity | Expected return | Volatility | Eligible reserve |
|---|---:|---:|---:|---:|---:|---:|---:|
| Benchmark | 0.00% | 0.00% | 40.00% | 60.00% | 6.80% | 10.46% | 0.00% |
| Equal weight | 25.00% | 25.00% | 25.00% | 25.00% | 5.20% | 5.21% | 50.00% |
| Inverse volatility | 84.32% | 6.02% | 7.03% | 2.63% | 3.77% | 1.05% | 90.34% |

The reserve-eligible sleeves are bills and the 10-year note. The original mandate requires $3 million of the initial $100 million portfolio, or 3%, in eligible reserves. Under the earlier supplied redemption times, all four sleeves redeem within five business days. All three baselines are fully invested, long-only and exempt from the company concentration cap under the supplied exemptions.

- **Benchmark:** Expected return exceeds the 6.5% objective by 0.30 percentage points, but its zero eligible reserve fails the 3% reserve rule. Its 10.46% volatility is the highest of these three baselines.
- **Equal weight:** Passes the reserve rule but expected return falls 1.30 percentage points short of the objective. Its 5.21% volatility is intermediate.
- **Inverse volatility:** Passes the reserve rule but expected return falls 2.73 percentage points short of the objective. The very low volatility of bills gives them 84.32% of capital, producing the lowest expected return and volatility.

**None of the three simultaneously reaches the 6.5% expected-return objective and satisfies the reserve rule.** Missing the expected-return objective is distinct from violating a hard constraint. The benchmark remains a valid performance reference even though using its exact weights as Meridian's actual portfolio would fail the reserve rule.

Full mandate approval also requires annual rebalancing and turnover evidence, ongoing payout funding, and clarification of the 10% calendar-year loss statement. Volatility measures return variability; 10.46% volatility neither means a 10.46% maximum loss nor proves that a 10% loss limit will be breached. No baseline can guarantee that limit from these inputs.

Reproduce the calculations with `.venv/bin/python lab13_baselines.py` from the course project directory. Calculations use unrounded weights.
