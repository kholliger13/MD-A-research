"""Save five years of completed monthly Yahoo adjusted closes to prices.csv."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yfinance as yf

from mandate_optimizer import TICKERS

ROOT = Path(__file__).resolve().parent
end = pd.Timestamp("2026-10-01")
start = end - pd.DateOffset(years=5)
data = yf.download(TICKERS, start=str(start.date()), end=str(end.date()),
                   interval="1mo", auto_adjust=False, progress=False,
                   threads=False)
if data.empty or "Adj Close" not in data:
    raise SystemExit("No adjusted-close data downloaded; no CSV written.")
prices = data["Adj Close"].reindex(columns=TICKERS).sort_index()
prices.index = pd.DatetimeIndex(prices.index).tz_localize(None)
expected = pd.date_range(start, end, freq="MS", inclusive="left")
if (not prices.index.equals(expected) or prices.shape != (60, 6)
        or not np.isfinite(prices.to_numpy()).all()
        or (prices.to_numpy() <= 0).any().any()):
    raise SystemExit("Incomplete or invalid monthly prices; no CSV written.")
prices.index.name = "Date"
path = ROOT / "prices.csv"
if path.exists():
    raise SystemExit("prices.csv already exists; refusing to overwrite.")
prices.to_csv(path, date_format="%Y-%m-%d", float_format="%.10f")
check = pd.read_csv(path, parse_dates=["Date"])
assert check.columns.tolist() == ["Date", *TICKERS]
assert len(check) == 60 and check.Date.is_monotonic_increasing
assert not check.isna().any().any()
downloaded = datetime.now(ZoneInfo("America/Indiana/Indianapolis")).isoformat(timespec="seconds")
notes = ROOT / "Lab14_portfolio_app_2026_10_22.md"
with notes.open("a") as file:
    file.write("\n\n## Monthly adjusted-close price file\n\n")
    file.write(f"Download timestamp: {downloaded} (America/Indiana/Indianapolis).\n\n")
    file.write("`prices.csv` contains 60 monthly adjusted-close observations, October 2021 "
               "through September 2026, in USD. Columns are `Date,QQQ,XLE,EWZ,LQD,TLT,FBMPX`, "
               "oldest month first. The date is Yahoo's month-start label for the monthly "
               "bar, not the date of the closing trade. October 2026 is excluded because "
               "it is incomplete. Values are Yahoo's explicit `Adj Close` field downloaded "
               "with `auto_adjust=False`; adjustments account for distributions and splits.\n\n")
    file.write("Source: Yahoo Finance historical data, retrieved using yfinance "
               f"{yf.__version__}, monthly interval. Per-fund source pages:\n\n")
    for ticker in TICKERS:
        file.write(f"- [{ticker} historical data](https://finance.yahoo.com/quote/{ticker}/history/)\n")
    file.write("\nValidation: exactly 60 unique consecutive months, six numeric positive "
               "price columns, no missing values, and ascending dates. Reproduce with "
               "`.venv/bin/python download_prices.py` (the script refuses to overwrite an existing CSV). "
               "Sixty price rows produce 59 monthly returns. The earlier optimizer used "
               "an additional September 2021 starting price to calculate 60 returns; "
               "its previously reported estimates therefore use a slightly different window.\n")
print(f"Saved {path.name}: {len(check)} rows, {check.Date.iloc[0]:%Y-%m-%d} to {check.Date.iloc[-1]:%Y-%m-%d}")
print(check.head(2).to_string(index=False))
print(f"Download timestamp: {downloaded}")
