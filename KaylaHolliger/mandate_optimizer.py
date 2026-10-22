"""Lab 14: Diversified Growth with a Bond Floor.

Run: .venv/bin/python mandate_optimizer.py
Dependencies: numpy pandas yfinance scipy
Historical arithmetic mean returns are estimates, not forecasts or guarantees.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

TICKERS = ["QQQ", "XLE", "EWZ", "LQD", "TLT", "FBMPX"]
FUND_NAMES = {
    "QQQ": "Invesco QQQ Trust (Nasdaq-100)",
    "XLE": "Energy Select Sector SPDR",
    "EWZ": "iShares MSCI Brazil",
    "LQD": "iShares Investment Grade Corporate Bond",
    "TLT": "iShares 20+ Year Treasury Bond",
    "FBMPX": "Fidelity Select Communication Services",
}
TARGET_RETURN = 0.08
BOND_FUNDS = ["LQD", "TLT"]
BOND_MIN = 0.20
YEARS = 5


def pct(x):
    return f"{x:.2%}"


def optimize(mu, cov, target=TARGET_RETURN, bond_min=BOND_MIN):
    """Minimize variance; validate solver output before returning raw weights."""
    mu = mu.loc[TICKERS].to_numpy(dtype=float)
    cov = cov.loc[TICKERS, TICKERS].to_numpy(dtype=float)
    if not np.isfinite(mu).all() or not np.isfinite(cov).all():
        raise ValueError("Asset estimates must all be finite.")
    if not np.isfinite(target) or not 0 <= bond_min <= 1:
        raise ValueError("Check the target and bond minimum.")
    if not np.allclose(cov, cov.T) or np.linalg.eigvalsh(cov).min() < -1e-10:
        raise ValueError("Covariance must be symmetric and positive semidefinite.")
    idx = [TICKERS.index(t) for t in BOND_FUNDS]
    # Exact maximum for a long-only portfolio with only this group floor.
    max_return = bond_min * max(mu[idx]) + (1 - bond_min) * max(mu)
    if target > max_return + 1e-10:
        raise ValueError(f"INFEASIBLE: target {pct(target)} exceeds maximum "
                         f"{pct(max_return)} with this bond floor.")
    constraints = [
        {"type": "eq", "fun": lambda w: w.sum() - 1},
        {"type": "ineq", "fun": lambda w: w[idx].sum() - bond_min},
        {"type": "ineq", "fun": lambda w: w @ mu - target},
    ]
    result = minimize(lambda w: w @ cov @ w,
                      np.full(len(mu), 1 / len(mu)),
                      jac=lambda w: 2 * cov @ w,
                      bounds=[(0, 1)] * len(mu), constraints=constraints,
                      method="SLSQP", options={"ftol": 1e-12, "maxiter": 1000})
    w = result.x
    if (not result.success or not np.isfinite(w).all()
            or abs(w.sum() - 1) > 1e-8 or w.min() < -1e-8
            or w.max() > 1 + 1e-8 or w[idx].sum() < bond_min - 1e-8
            or w @ mu < target - 1e-8):
        raise ValueError(f"No verified solution: {result.message}")
    return w, result.message, max_return


def load_estimates():
    # Exclude the current, unfinished month. Download an extra month to
    # supply the starting price for five years of monthly returns.
    end = pd.Timestamp.today().normalize().replace(day=1)
    start = end - pd.DateOffset(years=YEARS, months=1)
    data = yf.download(TICKERS, start=start.strftime("%Y-%m-%d"),
                       end=end.strftime("%Y-%m-%d"), interval="1mo",
                       auto_adjust=True, progress=False)
    if data.empty or "Close" not in data:
        raise ValueError("No prices downloaded. Check connection and tickers.")
    prices = data["Close"].reindex(columns=TICKERS)
    missing = prices.columns[prices.notna().sum() < 2].tolist()
    if missing:
        raise ValueError(f"Missing usable price history: {missing}")
    returns = prices.pct_change(fill_method=None).dropna().tail(12 * YEARS)
    if len(returns) < 12 * YEARS - 2:
        raise ValueError(f"Only {len(returns)} complete monthly returns; "
                         "insufficient common history for this five-year model.")
    return returns.mean() * 12, returns.cov() * 12, returns.corr(), returns


def main():
    print("MANDATE: Diversified Growth with a Bond Floor")
    print(f"Minimize volatility; expected return >= {pct(TARGET_RETURN)}")
    print(f"LQD + TLT >= {pct(BOND_MIN)}; fully invested; long-only")
    mu, cov, corr, returns = load_estimates()
    print(f"\nMonthly returns: {len(returns)} "
          f"({returns.index[0]:%b %Y} to {returns.index[-1]:%b %Y})")
    print("Estimates use adjusted prices and completed months; "
          "no separate fee or tax adjustment.")
    print("\nTABLE 1: Annualized historical estimates")
    print(pd.DataFrame({"Fund": [FUND_NAMES[t] for t in TICKERS],
                        "Expected return": mu.map(pct),
                        "Volatility": pd.Series(np.sqrt(np.diag(cov)),
                                                index=TICKERS).map(pct)}).to_string())
    print("\nTABLE 2: Correlations\n", corr.round(2).to_string())
    w, status, maximum = optimize(mu, cov)
    print(f"\nHighest feasible estimated return: {pct(maximum)}")
    print("\nTABLE 3: Optimal weights")
    for t, weight in zip(TICKERS, w):
        print(f"  {t:<6} {FUND_NAMES[t]:<44} {pct(weight)}")
    bond_weight = sum(w[TICKERS.index(t)] for t in BOND_FUNDS)
    print(f"\nExpected return: {pct(w @ mu.to_numpy())}")
    print(f"Volatility: {pct(np.sqrt(w @ cov.to_numpy() @ w))}")
    print(f"Bond weight: {pct(bond_weight)} "
          f"({'BINDING' if abs(bond_weight - BOND_MIN) < 1e-6 else 'slack'})")
    print(f"Solver: {status}")
    ew = np.full(len(TICKERS), 1 / len(TICKERS))
    print("\nEqual-weight comparison")
    print(f"Expected return: {pct(ew @ mu.to_numpy())}")
    print(f"Volatility: {pct(np.sqrt(ew @ cov.to_numpy() @ ew))}")
    print(f"Bond weight: {pct(2 / len(TICKERS))}")
    print(f"Meets return target: {ew @ mu.to_numpy() >= TARGET_RETURN}")
    print("\nHistorical estimates do not guarantee future returns or maximum losses.")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(str(error)) from error
