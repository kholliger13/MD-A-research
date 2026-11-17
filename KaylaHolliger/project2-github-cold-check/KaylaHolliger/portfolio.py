"""Lab 13 baseline portfolios; standard library only.

Inputs are course-authored training values, not market estimates.
Returns and volatilities are decimals: 0.035 means 3.5%.
"""

# EDITABLE INPUTS: correlation rows/columns follow this sleeve order.
SLEEVES = [
    {"name": "Treasury bills", "return": 0.035, "volatility": 0.005,
     "reserve_eligible": True},
    {"name": "Treasury 10-year note", "return": 0.043, "volatility": 0.070,
     "reserve_eligible": True},
    {"name": "Investment-grade bond fund", "return": 0.050, "volatility": 0.060,
     "reserve_eligible": False},
    {"name": "Global equity index fund", "return": 0.080, "volatility": 0.160,
     "reserve_eligible": False},
]
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065

# STUDY NOTE AND QUIZ
# "For each" means repeat the output for benchmark, equal weight, and inverse
# volatility. A sleeve is one investment category in the portfolio.
#
# 1. Weights tell you what share of the money goes into EACH sleeve.
#    Print each weight with one digit after the decimal: e.g., 25.0%.
#    Python's :.1% converts a decimal to percent and displays one decimal place.
# 2. Expected return is the portfolio's modeled gain, not a guaranteed gain.
#    Volatility measures how much returns may fluctuate, not the maximum loss.
#    Print BOTH with two decimal places: e.g., 5.20% and 5.21%.
#    Python's :.2% converts a decimal to percent and displays two decimal places.
# 3. Reserve-eligible weight is the share invested in qualifying reserve assets.
#    For this lab, add the BILLS weight to the 10-YEAR NOTE weight.
#    Do not add their returns or volatilities. The IG bond fund does not qualify.
#
# QUIZ: Try answering before running the program to check your work.
# A. Equal weight puts one quarter in each sleeve. How should each weight print?
# B. If expected return is stored as 0.052, how should it print with :.2%?
# C. If volatility is stored as 0.0521446, how should it print with :.2%?
# D. Equal weight has 25% bills and 25% ten-year notes. What is its eligible
#    reserve weight? How many dollars is that in a $100 million portfolio?
# E. The benchmark holds 40% IG bonds and 60% equities. What share qualifies
#    as reserve assets? Does it meet Meridian's 3% minimum?
# F. Does a portfolio volatility of 10.46% guarantee losses cannot exceed 10.46%?

import math
import sys


def validate_inputs(sleeves, correlations, objective):
    """Reject malformed inputs before calculating or printing portfolios."""
    n = len(sleeves)
    if not n or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square, with one row per sleeve.")
    if not math.isfinite(objective):
        raise ValueError("Objective return must be finite.")
    names = [sleeve["name"] for sleeve in sleeves]
    if len(set(names)) != n:
        raise ValueError("Sleeve names must be unique.")
    for sleeve in sleeves:
        if not math.isfinite(sleeve["return"]):
            raise ValueError(f"Expected return for {sleeve['name']} must be finite.")
        if not math.isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError(f"Volatility for {sleeve['name']} must be finite and positive.")
    for i, row in enumerate(correlations):
        for j, value in enumerate(row):
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation at row {i + 1}, column {j + 1} "
                                 "must be between -1 and 1.")
    for i in range(n):
        if correlations[i][i] != 1:
            raise ValueError("Each diagonal correlation must equal 1.")
        for j in range(i):
            if correlations[i][j] != correlations[j][i]:
                raise ValueError(f"Correlation table is not symmetric: "
                                 f"rows/columns {i + 1} and {j + 1} disagree.")


def build_covariance_matrix(sleeves, correlations):
    """Covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return [[correlations[i][j] * left["volatility"] * right["volatility"]
             for j, right in enumerate(sleeves)]
            for i, left in enumerate(sleeves)]


def benchmark_weights(sleeves):
    allocation = {"Investment-grade bond fund": 0.40,
                  "Global equity index fund": 0.60}
    if not allocation.keys() <= {sleeve["name"] for sleeve in sleeves}:
        raise ValueError("Benchmark requires the investment-grade bond and global equity funds.")
    return [allocation.get(sleeve["name"], 0.0) for sleeve in sleeves]


def equal_weights(sleeves):
    return [1 / len(sleeves) for _ in sleeves]


def inverse_volatility_weights(sleeves):
    inverse = [1 / sleeve["volatility"] for sleeve in sleeves]
    total = math.fsum(inverse)
    return [value / total for value in inverse]


def expected_return(weights, sleeves):
    return math.fsum(weights[i] * sleeve["return"]
                     for i, sleeve in enumerate(sleeves))


def portfolio_volatility(weights, covariance):
    variance = math.fsum(weights[i] * covariance[i][j] * weights[j]
                         for i in range(len(weights)) for j in range(len(weights)))
    if variance < 0:
        raise ValueError("Portfolio variance is negative; check the correlation inputs.")
    return math.sqrt(variance)


def reserve_eligible_weight(weights, sleeves):
    return math.fsum(weights[i] for i, sleeve in enumerate(sleeves)
                     if sleeve["reserve_eligible"])


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def search_portfolio(sleeves, correlations, objective, reserve_minimum, return_details=False):
    """Return the least volatile feasible 5-percentage-point mix, or None.

    Fully invested integer compositions of 20 units enumerate every long-only
    grid allocation exactly once. Results retain unrounded decimal values.
    """
    validate_inputs(sleeves, correlations, objective)
    if not math.isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0 and 1.")
    covariance = build_covariance_matrix(sleeves, correlations)

    def compositions(total, count, prefix=()):
        if count == 1:
            yield prefix + (total,)
        else:
            for value in range(total + 1):
                yield from compositions(total - value, count - 1, prefix + (value,))

    best = None
    tested = qualifying = 0
    maximum = None
    for units in compositions(20, len(sleeves)):
        tested += 1
        weights = [value / 20 for value in units]
        result = expected_return(weights, sleeves)
        reserve = reserve_eligible_weight(weights, sleeves)
        # Tolerance only absorbs floating-point arithmetic at exact boundaries.
        if reserve < reserve_minimum - 1e-12:
            continue
        maximum = result if maximum is None else max(maximum, result)
        if result < objective - 1e-12:
            continue
        qualifying += 1
        volatility = portfolio_volatility(weights, covariance)
        if best is None or volatility < best["volatility"]:
            best = {"weights": weights, "return": result,
                    "volatility": volatility, "reserve_weight": reserve}
    if return_details:
        return {"portfolio": best, "mixes_tested": tested,
                "mixes_qualifying": qualifying, "max_return_on_grid": maximum}
    return best


def estimate_from_csv(source, last_36_months=False):
    """Return (sleeves, correlations) from chronological monthly prices.

    Accept a path or a readable text/binary stream. Use sample standard
    deviations and Pearson correlations; select the last 36 RETURNS after
    computing price ratios (requires at least 37 prices). No filling of gaps.
    CSV eligibility defaults to False: a price series cannot establish it.
    """
    import csv
    import io
    from datetime import date
    from pathlib import Path
    import statistics

    raw = source.read() if hasattr(source, "read") else Path(source).read_bytes()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows or len(rows[0]) < 2:
        raise ValueError("CSV needs a date column followed by ticker columns.")
    names = [name.strip() for name in rows[0][1:]]
    if any(not name for name in names) or len(set(names)) != len(names):
        raise ValueError("Ticker headers must be nonempty and unique.")
    prices, dates = [], []
    for row in rows[1:]:
        if not row:
            continue
        if len(row) != len(names) + 1:
            raise ValueError("Every CSV row must have one price per ticker.")
        try:
            dates.append(date.fromisoformat(row[0].strip()))
            values = [float(value) for value in row[1:]]
        except ValueError as error:
            raise ValueError("Use ISO dates (YYYY-MM-DD) and numeric prices.") from error
        if any(not math.isfinite(value) or value <= 0 for value in values):
            raise ValueError("Prices must be finite, positive, and never missing.")
        prices.append(values)
    if len(prices) < 3:
        raise ValueError("At least three monthly price rows are required.")
    months = [d.year * 12 + d.month for d in dates]
    if any(b - a != 1 for a, b in zip(months, months[1:])):
        raise ValueError("Dates must be oldest first, one row per consecutive month.")
    returns = [[new[i] / old[i] - 1 for i in range(len(names))]
               for old, new in zip(prices, prices[1:])]
    if last_36_months:
        if len(returns) < 36:
            raise ValueError("Last 36 months requires at least 37 monthly price rows.")
        returns = returns[-36:]
    return estimate_monthly_returns(returns, names)


def estimate_monthly_returns(returns, names):
    """Shared annualization and correlation calculation for monthly returns."""
    import statistics
    series = list(zip(*returns))
    deviations = [statistics.stdev(values) for values in series]
    if any(value <= 0 for value in deviations):
        raise ValueError("Each asset needs nonzero monthly return volatility.")
    sleeves = [{"name": name, "return": statistics.mean(values) * 12,
                "volatility": deviation * math.sqrt(12), "reserve_eligible": False}
               for name, values, deviation in zip(names, series, deviations)]
    correlations = [[1.0 if i == j else statistics.correlation(series[i], series[j])
                     for j in range(len(names))] for i in range(len(names))]
    validate_inputs(sleeves, correlations, 0.0)
    return sleeves, correlations


def print_portfolio(name, weights, sleeves, covariance, objective):
    result = expected_return(weights, sleeves)
    print(f"\n{name}")
    for sleeve, weight in zip(sleeves, weights):
        print(f"  {sleeve['name']}: {weight:.1%}")
    print(f"  Expected return: {result:.2%}")
    print(f"  Volatility: {portfolio_volatility(weights, covariance):.2%}")
    print(f"  Reserve-eligible weight: {reserve_eligible_weight(weights, sleeves):.1%}")
    print(f"  Meets {objective:.2%} objective: "
          f"{'Yes' if meets_objective(result, objective) else 'No'}")


def main():
    try:
        validate_inputs(SLEEVES, CORRELATIONS, OBJECTIVE_RETURN)
        covariance = build_covariance_matrix(SLEEVES, CORRELATIONS)
        portfolios = [
            ("Benchmark", benchmark_weights(SLEEVES)),
            ("Equal weight", equal_weights(SLEEVES)),
            ("Inverse volatility", inverse_volatility_weights(SLEEVES)),
        ]
        # Check all portfolio variances before printing any results.
        for _, weights in portfolios:
            portfolio_volatility(weights, covariance)
        print("Lab 13: course-authored training values, not market estimates.")
        for name, weights in portfolios:
            print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN)
    except ValueError as error:
        print(f"Cannot run: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
