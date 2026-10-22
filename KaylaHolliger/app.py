"""Run: .venv/bin/python -m streamlit run app.py"""
from pathlib import Path
import pandas as pd
import streamlit as st
from portfolio import SLEEVES, CORRELATIONS, OBJECTIVE_RETURN
from portfolio_core import (OBJECTIVE, RESERVE_ELIGIBLE, RESERVE_MIN,
                            build_covariance, choose_window, estimate_inputs,
                            load_prices, monthly_returns, optimize)

FUND_NAMES = {
    "QQQ": "Invesco QQQ Trust (Nasdaq-100)", "XLE": "Energy Select Sector SPDR",
    "EWZ": "iShares MSCI Brazil", "LQD": "iShares Investment Grade Corporate Bond",
    "TLT": "iShares 20+ Year Treasury Bond", "FBMPX": "Fidelity Select Communication Services",
}
st.set_page_config(page_title="Portfolio Recommendation", layout="wide")
st.title("Diversified Growth with a Bond Floor")
st.caption("Built with AI help, a learning demonstration, not investment advice.")
st.write("Seek the lowest modeled volatility while meeting an estimated annual return "
         "objective and a minimum bond reserve. Every mix is fully invested, long-only, "
         "and uses 5 percentage point steps.")
source = st.sidebar.radio("Input source", ["Six-fund CSV", "Meridian training inputs"])
meridian = source == "Meridian training inputs"
upload = st.sidebar.file_uploader("prices.csv (optional, uses the local file if blank)", type="csv", disabled=meridian)
if not meridian:
    try:
        prices = load_prices(upload if upload is not None else Path(__file__).with_name("prices.csv"))
    except (OSError, ValueError, UnicodeError) as error:
        st.error(f"Price data problem: {error}. Upload prices.csv or run download_prices.py.")
        st.stop()
st.sidebar.header("Mandate settings")
window = st.sidebar.radio("Estimation window", ["All returns", "Last 36 months"], disabled=meridian)
objective = st.sidebar.number_input("Return objective (%)", 0.0, 30.0,
                                   (OBJECTIVE_RETURN if meridian else OBJECTIVE) * 100, 0.5,
                                   key=f"objective_{source}") / 100
reserve_min = st.sidebar.number_input("Minimum reserve weight (%)", 0.0, 100.0,
                                     3.0 if meridian else RESERVE_MIN * 100, 5.0,
                                     key=f"minimum_{source}") / 100
if meridian:
    names = [s['name'] for s in SLEEVES]
    mu = base_mu = pd.Series([s['return'] for s in SLEEVES], index=names)
    vol = base_vol = pd.Series([s['volatility'] for s in SLEEVES], index=names)
    corr = base_corr = pd.DataFrame(CORRELATIONS, index=names, columns=names)
    eligible_defaults = {s['name'] for s in SLEEVES if s['reserve_eligible']}
    data_key = str((SLEEVES, CORRELATIONS))
    st.caption("Meridian course training estimates loaded directly from portfolio.py.")
else:
    all_returns = monthly_returns(prices)
    try:
        returns = choose_window(all_returns, "all" if window == "All returns" else 36)
        mu, vol, corr = estimate_inputs(returns)
        base_mu, base_vol, base_corr = estimate_inputs(all_returns)
    except ValueError as error:
        st.error(str(error))
        st.stop()
    eligible_defaults = RESERVE_ELIGIBLE
    data_key = str(pd.util.hash_pandas_object(prices).sum())
    st.caption(f"Estimated from {len(returns)} monthly returns, "
               f"{returns.index[0]:%b %Y} to {returns.index[-1]:%b %Y}. "
               "Annualized historical averages are estimates, not forecasts.")
st.subheader("1. Review assumptions")
st.write("Edit annual return estimates or change which funds count as reserves.")
assumptions = pd.DataFrame({
    "Fund": [FUND_NAMES.get(t, t) for t in mu.index],
    "Annual return estimate (%)": mu * 100, "Volatility (%)": vol * 100,
    "Reserve eligible": [t in eligible_defaults for t in mu.index],
}, index=mu.index)
edited = st.data_editor(assumptions, disabled=["Fund", "Volatility (%)"],
                        column_config={"Annual return estimate (%)": st.column_config.NumberColumn(format="%.2f", required=True),
                                       "Volatility (%)": st.column_config.NumberColumn(format="%.2f")},
                        width="stretch", key=f"assumptions_{source}_{window}_{data_key}")
with st.expander("Correlation matrix"):
    st.dataframe(corr.round(2), width="stretch")

@st.cache_data(show_spinner=False)
def solve(mu, cov, eligible, objective, reserve_min):
    return optimize(mu, cov, eligible, objective, reserve_min)

eligible = edited.index[edited["Reserve eligible"]].tolist()
try:
    with st.spinner("Trying every 5-point mix…"):
        result = solve(edited["Annual return estimate (%)"] / 100,
                       build_covariance(vol, corr), eligible, objective, reserve_min)
        baseline = solve(base_mu, build_covariance(base_vol, base_corr), eligible, objective, reserve_min)
except ValueError as error:
    st.error(str(error))
    st.stop()
st.subheader("2. Recommended portfolio")
if not eligible and reserve_min > 0:
    st.warning("No funds are marked reserve eligible, so the reserve minimum cannot be met.")

def display(result, heading):
    st.markdown(f"### {heading}")
    if not result["found"]:
        st.error("no mix meets the objective")
        maximum = result['max_return_on_grid']
        st.caption("No grid mix satisfies the reserve minimum." if maximum is None else
                   f"Highest estimated return among reserve-feasible mixes: {maximum:.2%}.")
        return
    st.metric("Estimated annual return", f"{result['return']:.2%}")
    st.metric("Volatility", f"{result['volatility']:.2%}")
    st.metric("Reserve-eligible weight", f"{result['reserves']:.2%}")
    weights = result['weights']
    st.dataframe(pd.DataFrame({"Fund": [FUND_NAMES.get(t, t) for t in weights.index],
                               "Weight (%)": weights.map(lambda x: f"{x * 100:.2f}")},
                              index=weights.index), width="stretch")
    st.bar_chart(weights[weights > 0] * 100, y_label="Weight (%)")
    st.caption(f"Tested {result['mixes_tested']:,} mixes; "
               f"{result['mixes_qualifying']:,} met both requirements.")

left, right = st.columns(2)
with left:
    display(result, "Your assumptions")
with right:
    display(baseline, "Inputs as loaded · Meridian" if meridian else "Inputs as loaded · all months")
if result['found'] and baseline['found']:
    changes = (result['weights'] - baseline['weights']) * 100
    ticker = changes.abs().idxmax()
    st.metric(f"Largest weight change · {ticker} (percentage points)", f"{changes[ticker]:+.2f}")
else:
    st.caption("Largest weight change is unavailable until both mixes are feasible.")
st.caption("Both answers use the same objective, reserve minimum, and eligibility selections. "
           "Lowest risk means lowest volatility on the 5-point grid. Historical estimates "
           "do not guarantee future returns; a bond allocation does not guarantee capital stability.")
