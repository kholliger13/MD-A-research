"""Lab 13: course-authored training inputs, not market estimates."""

import numpy as np

SLEEVES = ["Treasury bills", "Treasury 10-year note", "IG bond fund", "Global equity"]
RETURNS = np.array([0.035, 0.043, 0.050, 0.080])
VOLATILITIES = np.array([0.005, 0.070, 0.060, 0.160])
CORRELATIONS = np.array([
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
])
COVARIANCE = np.outer(VOLATILITIES, VOLATILITIES) * CORRELATIONS
OBJECTIVE = 0.065
RESERVE_MINIMUM = 0.03


def main():
    inverse_volatility = 1 / VOLATILITIES
    baselines = {
        "Benchmark": np.array([0.0, 0.0, 0.4, 0.6]),
        "Equal weight": np.full(4, 0.25),
        "Inverse volatility": inverse_volatility / inverse_volatility.sum(),
    }
    for name, weights in baselines.items():
        expected_return = float(weights @ RETURNS)
        volatility = float(np.sqrt(weights @ COVARIANCE @ weights))
        reserve = float(weights[:2].sum())
        print(f"\n{name}")
        for sleeve, weight in zip(SLEEVES, weights):
            print(f"  {sleeve}: {weight:.4%}")
        print(f"  Expected return: {expected_return:.4%}")
        print(f"  Volatility: {volatility:.4%}")
        print(f"  Reserve eligible: {reserve:.4%}")
        print(f"  Expected return >= 6.5%: {expected_return >= OBJECTIVE}")
        print(f"  Reserve >= 3%: {reserve >= RESERVE_MINIMUM}")
    print("\nReturns have no separate cost adjustment: no fee input was supplied.")
    print("Volatility is not a maximum-loss guarantee. Full mandate compliance remains open.")


if __name__ == "__main__":
    main()
