# Meridian Foundation — assigned common case

Reserve: $100 million. Analysis is limited to the assigned common case, supplied holdings and candidates A–D.

## What is an investment policy statement?

An **investment policy statement (IPS)** is a written agreement that guides how a portfolio is managed. It records the investor's goals, the limits on investment decisions, and the procedures for monitoring results and approving changes. For Meridian, it connects the foundation's payout needs and return target to the CIO's investment decisions and the committee's oversight.

## How objectives and constraints work together

**Objectives describe what the portfolio should achieve.** Meridian's stated return objective is CPI + 4% a year after costs over rolling five-year periods (S2). An objective is a target to evaluate, not a guaranteed return. The IPS should explain how the target will guide decisions and how success will be measured.

**Constraints define the boundaries within which the manager works.** Meridian must maintain its payout reserve, use permitted instruments, limit company concentration and turnover, and meet the liquidity requirement. A portfolio that violates a binding constraint is ineligible unless the policy expressly allows an approved exception. A portfolio that passes those checks still needs to be suitable for the objectives.

In practice, the CIO first clarifies the policy, then screens portfolios against its constraints, assesses whether eligible portfolios credibly support its objectives, and monitors compliance and performance over time. Optimization comes only after the CIO specifies the quantity to optimize and acceptable trade-offs (S10). A benchmark supplies a comparison; it does not automatically require matching its weights.

## Mapping S1–S10 to an IPS

| Statement | IPS section | What it means for Meridian |
|---|---|---|
| S1 | Time horizon and implementation | Plan for seven years and rebalance annually; the planning horizon differs from S2's rolling five-year performance window. |
| S2 | Return objective and performance evaluation | Target CPI + 4% annually net of costs over rolling five-year periods; clarify whether credible expected achievement is an eligibility requirement or an aspiration. |
| S3 | Spending policy and liquidity needs | Fund $0.75 million quarterly payouts and maintain twelve months of payouts—$3 million—in eligible reserve assets. |
| S4 | Benchmark and reporting | Compare performance with 60% global equities and 40% U.S. investment-grade bonds; no matching-weight or tracking-error requirement is stated. |
| S5 | Permitted investments and trading restrictions | Require long-only holdings and prohibit borrowing, short sales and derivatives. |
| S6 | Diversification and concentration limits | Limit each company's combined securities to 8%; apply the supplied exemptions for cash, Treasury and diversified funds. |
| S7 | Portfolio implementation and governance | Keep annual turnover at or below 25% unless the committee approves an exception; define how turnover is calculated. |
| S8 | Portfolio liquidity limit | Require at least 90% redeemable within five business days; this is separate from S3's reserve-eligibility test. |
| S9 | Risk objective or limit and breach governance—unfinished | The 10% calendar-year loss statement needs a defined measure, assessment method and breach response before it can function as an operational rule. |
| S10 | Investment preferences and decision criterion—partly missing | No sector, ESG, tax or home-bias preference is stated; the CIO must still specify what the pilot should optimize. |

The existing checker implements only the numerical rules supported by the supplied holdings and weights. It does not replace the IPS: D's 100% cash allocation demonstrates why passing those checks does not settle suitability under S2.

| Statement | Type | One-line reason |
|---|---|---|
| S1 — Horizon seven years; annual rebalancing. | Hard constraint | Sets the planning horizon and required rebalancing schedule, rather than a quantity to maximize. |
| S2 — Objective: CPI + 4% a year, net of costs, over rolling five-year periods. | Objective | States a net real-return target and evaluation window; it is a target, not a guaranteed outcome or a complete optimization criterion. |
| S3 — Pays out $0.75 million every quarter; twelve months of payouts held in cash or daily-liquid government securities. | Hard constraint | Requires quarterly funding and a $3 million qualifying liquidity buffer (3% of the initial reserve). |
| S4 — Benchmark: 60% global equities, 40% U.S. investment-grade bonds. | Preference | Establishes a reference portfolio for comparison, without requiring those weights or specifying a tracking-error limit. |
| S5 — Long-only: no borrowing, short sales or derivatives. | Hard constraint | Explicitly prohibits leverage, short positions and derivatives. |
| S6 — No single issuer above 8%. | Hard constraint | Caps each company's combined securities at 8%; cash, Treasury and diversified funds are exempt under the supplied issuer rule. |
| S7 — Annual turnover at most 25% without committee approval. | Hard constraint | Caps annual turnover unless the committee grants an exception; the turnover calculation must be defined. |
| S8 — At least 90% redeemable within five business days. | Hard constraint | Requires at least 90% portfolio liquidity within the specified period, with redemption and settlement conventions to be confirmed. |
| S9 — “The reserve cannot have a calendar-year loss greater than 10%.” No measure, no breach rule. | Unverifiable promise | An unconditional future loss ceiling cannot be certified from portfolio weights, and no operational risk measure or breach response is defined. |
| S10 — No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize. | Missing | The listed preferences are explicitly absent, while the pilot's optimization criterion and risk–return trade-off remain unspecified. |

## What is permitted, and what must the CIO answer?

**Among the original candidates A–C, A is the only candidate that passes all hard constraints testable from the supplied holdings and weights. B and C fail.** A remains conditional on the annual rebalancing and turnover requirements; weights alone do not establish those. S2 supplies a performance target; S4 does not mandate a 60/40 allocation. S9 cannot yet be used as a testable portfolio eligibility rule.

| Check | A | B | C |
|---|---|---|---|
| Weights total 100%; nonnegative, permitted instruments (S5) | Pass: 100% | Pass: 100% | Pass: 100% |
| Reserve-eligible holdings ≥ $3 million / 3% (S3) | Pass: 14% / $14m | **Fail: 1% / $1m**, $2m short | **Fail: 2% / $2m**, $1m short |
| Nonexempt issuer ≤ 8% (S6) | Pass: no nonexempt issuer | **Fail: Acme 5% + 4% = 9%** | Pass: Acme exactly 8% |
| Redeemable within five business days ≥ 90% (S8) | Pass: 100% | **Fail: 85%**; 15% requires 90 days | Pass: 100% |
| Overall holdings-based eligibility | **Pass, conditional** | **Reject** | **Reject** |

The reserve calculation includes cash, Treasury bills and the Treasury 10-year note because all three are explicitly reserve-eligible. The note's ten-year maturity does not change its supplied one-business-day redemption time. B's diversified private real estate fund is exempt from the issuer cap but still fails the five-day liquidity test. C's 8% Acme position meets the ceiling because the rule prohibits amounts above 8%.

Annual turnover (S7) requires starting holdings and the trading/rebalancing path; it cannot be inferred from any candidate's ending weights. Seven-year suitability and annual rebalancing (S1), actual payout funding over time (S3), and achievement of CPI + 4% (S2) also cannot be certified from a static allocation. None of these candidates can be certified to satisfy the undefined future loss promise in S9.

Before anyone optimizes, the CIO must answer:

1. **What should the pilot optimize?** For example, minimize a specified risk measure while targeting CPI + 4%, maximize the probability of meeting that target, or minimize benchmark tracking error subject to a return requirement—and what trade-offs are acceptable?
2. **What does the 10% loss statement mean?** Define loss (including treatment of payouts and costs), the risk measure and assessment method, any probability or stress assumptions, and the action or approval process following a breach. If an absolute guarantee is intended, its feasibility must be established rather than assumed.
3. **How will compliance be measured?** Confirm the CPI series and return calculation, turnover definition and starting holdings, liquidity evidence and settlement timing, and monitoring dates and remedies for passive breaches between annual rebalances. Apply the supplied issuer exemptions and combine each company's securities.

## Candidate D — passes the code, still open to CIO rejection

D holds 100% cash and 0% in every other supplied holding. Running `python3 mandate.py` confirms: total weight 100.0 (pass), lowest weight 0.0 (pass), reserve-eligible 100.0% (pass), five-day liquidity 100.0% (pass), largest nonexempt company 0.0% (pass). The verdict is “passes every checkable rule.” No optimization was performed.

The CIO could reasonably reject D under **S2** if it lacks a credible path to CPI + 4% annually net of costs over rolling five-year periods. The objection is a return-target suitability concern, not a demonstrated hard-constraint violation: no cash yield, inflation or cost assumptions were supplied, so the weights alone cannot prove that D will miss S2. S4's benchmark does not itself prohibit all cash. S10 still requires the CIO to choose an optimization criterion before any optimization begins.

Partner exchange completed: the partner also proposed 100% cash. I cite **S2** against their candidate, and they cite **S2** against D: neither allocation, by itself, establishes a credible path to CPI + 4% net. This supports reasonable CIO rejection but does not prove a violation without return, inflation and fee assumptions evaluated over the mandated horizon and rolling five-year periods. Both pass the coded static checks; passing the code does not settle S2. The identical allocations are valid for the exchange; no different allocation is required.

## Question for the CIO

Under S2, must the portfolio have a credible expected return of CPI + 4% net over a specified horizon, or is that only an aspiration?

## Reflections

1. **Why passing every checkable rule can still be wrong for this client:** The checker verifies numerical boundaries using the supplied holdings and weights; it does not establish that a portfolio meets Meridian's investment purpose. D's 100% cash allocation passes the reserve, liquidity, concentration, total-weight and long-only checks, yet does not establish a credible path to S2's CPI + 4% net return target. The CIO could reasonably reject it on that basis, although the allocation alone does not prove a return-target violation. The checker also cannot settle the undefined loss statement in S9 or verify future turnover and annual rebalancing from static weights. Passing the code is therefore a screening result, not a complete suitability judgment.

2. **The S1–S10 type I was least sure of:** S4 was the least certain classification. I labeled it **preference** because the required categories do not include “benchmark” or “performance reference.” A 60/40 benchmark tells us how to compare results, but it does not by itself require 60/40 holdings or make minimizing tracking error the objective. “Preference” is the closest available label, with that qualification; treating S4 as a hard allocation constraint would add a requirement the CIO did not state.

## Checker verification and negative-weight probe

Running `python3 mandate.py` matched every value and verdict in the supplied known answer. The reserve minimum printed as 3.0% ($3 million).

| Rule | A | B | C |
|---|---|---|---|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | Requires CIO clarification | Requires CIO clarification | Requires CIO clarification |
| Verdict | Passes every checkable rule | Fails 3 rules | Fails 1 rule |

For the probe, A's cash was temporarily changed from 2% to −2% and its global equity fund from 60% to 64%. The rerun produced:

| Rule | Modified A |
|---|---|
| Weights sum to 100 | 100.0 pass |
| Long-only (lowest weight) | −2.0 FAIL |
| Reserve ≥ 3.0% | 10.0 pass |
| Redeemable in 5 days ≥ 90% | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass |
| Verdict | Fails 1 rule: long-only |

Cash was restored to 2% and the global equity fund to 60%. The final rerun again matched the known answer. Acme bonds and stock are aggregated by company. The total-weight check uses `math.isclose(total, 100, rel_tol=0, abs_tol=1e-9)` to tolerate small floating-point rounding differences.
