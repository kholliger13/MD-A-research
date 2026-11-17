"""Check the supplied Meridian Foundation common-case allocations."""

import math

RESERVE = 100_000_000
QUARTERLY_PAYOUT = 750_000
RESERVE_MINIMUM = 4 * QUARTERLY_PAYOUT

# holding: (issuer, business days to redeem, reserve eligible)
# None means exempt from the issuer concentration rule.
HOLDINGS = {
    "Cash": (None, 0, True),
    "Treasury bills": (None, 1, True),
    "Treasury 10-year note": (None, 1, True),
    "Global equity index fund": (None, 2, False),
    "Investment-grade bond fund": (None, 3, False),
    "Private real estate fund": (None, 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

# Percentages follow the holding order above.
CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    # D passes static checks but exposes S2: can cash meet CPI + 4% net?
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
}


def check_candidate(name, weights):
    assert len(weights) == len(HOLDINGS), "One weight is required per holding."
    reserve_pct = 0
    liquid_pct = 0
    issuer_totals = {}
    for (issuer, days, eligible), weight in zip(HOLDINGS.values(), weights):
        if eligible:
            reserve_pct += weight
        if days <= 5:
            liquid_pct += weight
        if issuer is not None:
            issuer_totals[issuer] = issuer_totals.get(issuer, 0) + weight

    largest_company = max(issuer_totals.values(), default=0)
    rules = {
        "Weights sum to 100": (
            math.isclose(sum(weights), 100, rel_tol=0, abs_tol=1e-9),
            sum(weights),
        ),
        "Long-only (lowest weight)": (
            min(weights) >= 0,
            min(weights),
        ),
        "Reserve >= 3.0%": (
            reserve_pct >= 100 * RESERVE_MINIMUM / RESERVE,
            reserve_pct,
        ),
        "Redeemable in 5 days >= 90%": (
            liquid_pct >= 90,
            liquid_pct,
        ),
        "Largest single company <= 8%": (
            largest_company <= 8,
            largest_company,
        ),
    }
    print(f"\nCandidate {name}")
    for rule, (passed, detail) in rules.items():
        print(f"  {rule}: {detail:.1f} {'pass' if passed else 'FAIL'}")
    print("  Calendar-year loss: requires CIO clarification")
    failures = sum(not passed for passed, value in rules.values())
    print("  Verdict: " + (f"fails {failures} rule(s)" if failures
                           else "passes every checkable rule"))
    return rules


def main():
    print(f"Reserve minimum: {100 * RESERVE_MINIMUM / RESERVE:.1f}% of the portfolio "
          f"(${RESERVE_MINIMUM:,.0f})")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights)
    print("\nAll candidates: S1 annual rebalancing and S7 turnover need a trading plan.")
    print("S2 is a return target; S4 is a benchmark, not required weights.")
    print("S9 cannot be certified: define the loss measure and breach rule.")
    print("S10: the CIO must specify what the pilot should optimize.")
    print("A's pass covers static holdings checks, not future performance "
          "or ongoing payout funding.")


if __name__ == "__main__":
    main()
