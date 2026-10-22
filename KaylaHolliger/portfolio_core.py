"""Pandas interface for the shared portfolio.py engine; no duplicated math."""
import io

import pandas as pd

from portfolio import (estimate_from_csv, estimate_monthly_returns,
                       build_covariance_matrix, search_portfolio)

OBJECTIVE = 0.08
RESERVE_MIN = 0.20
RESERVE_ELIGIBLE = {"LQD", "TLT"}


def load_prices(source):
    if hasattr(source, "getvalue"):
        source = io.BytesIO(source.getvalue())
    frame = pd.read_csv(source)
    # Use the shared CSV validator before constructing the indexed frame.
    estimate_from_csv(io.StringIO(frame.to_csv(index=False)))
    frame[frame.columns[0]] = pd.to_datetime(frame.iloc[:, 0])
    frame = frame.set_index(frame.columns[0])
    frame.index = pd.DatetimeIndex(frame.index)
    return frame.astype(float)


def monthly_returns(prices):
    return prices.pct_change(fill_method=None).iloc[1:]


def choose_window(returns, window):
    if window == "all":
        return returns
    if window != 36:
        raise ValueError("Choose all returns or the last 36 months.")
    if len(returns) < 36:
        raise ValueError("Last 36 months requires at least 37 monthly prices.")
    return returns.tail(36)


def estimate_inputs(returns):
    sleeves, correlations = estimate_monthly_returns(
        returns.to_numpy().tolist(), returns.columns.tolist())
    return (pd.Series([s['return'] for s in sleeves], index=returns.columns),
            pd.Series([s['volatility'] for s in sleeves], index=returns.columns),
            pd.DataFrame(correlations, index=returns.columns, columns=returns.columns))


def build_covariance(vol, corr):
    sleeves = [{"volatility": float(vol[t])} for t in vol.index]
    return pd.DataFrame(build_covariance_matrix(sleeves, corr.loc[vol.index, vol.index].values.tolist()),
                        index=vol.index, columns=vol.index)


def optimize(mu, cov, eligible, objective, reserve_min):
    # Convert the covariance to the shared engine's sleeve/correlation interface.
    sleeves = [{"name": t, "return": float(mu[t]), "volatility": float(cov.loc[t, t] ** .5),
                "reserve_eligible": t in eligible} for t in mu.index]
    vols = pd.Series([s['volatility'] for s in sleeves], index=mu.index)
    corr = cov.loc[mu.index, mu.index].div(vols, axis=0).div(vols, axis=1)
    for t in mu.index:
        corr.loc[t, t] = 1.0
    # Eliminate floating-point asymmetry from the covariance conversion.
    for i, t in enumerate(mu.index):
        for u in mu.index[:i]:
            corr.loc[t, u] = corr.loc[u, t]
    details = search_portfolio(sleeves, corr.values.tolist(), objective,
                               reserve_min, return_details=True)
    result = details.pop("portfolio")
    details["found"] = result is not None
    if result:
        details.update(result)
        details["weights"] = pd.Series(result["weights"], index=mu.index)
        details["reserves"] = result["reserve_weight"]
    return details
