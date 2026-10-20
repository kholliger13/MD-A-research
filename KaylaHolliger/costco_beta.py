"""Recompute historical raw monthly beta offline. Standard library only.
Prices: September 2020–September 2025 month ends; 60 returns October 2020–September 2025.
Main benchmark: SPY adjusted-close total-return proxy. S&P price index: comparison only.
This is a regression on raw returns with an intercept, not excess-return CAPM regression.
"""
import csv, math, statistics
from pathlib import Path


def beta(stock, market):
    if len(stock) != len(market) or len(stock) < 2:
        raise ValueError('Aligned return observations required.')
    xs, ys = statistics.mean(market), statistics.mean(stock)
    cross = sum((x-xs)*(y-ys) for x,y in zip(market,stock))
    variance = sum((x-xs)**2 for x in market)
    if variance <= 0:
        raise ValueError('Market variance must be positive.')
    slope = cross/variance
    intercept = ys-slope*xs
    residual = sum((y-intercept-slope*x)**2 for x,y in zip(market,stock))
    total = sum((y-ys)**2 for y in stock)
    se = math.sqrt(residual/(len(stock)-2)/variance)
    return slope, intercept, 1-residual/total, se


def main():
    path = Path(__file__).with_name('costco_beta_month_end_prices.csv')
    with path.open() as f:
        rows=list(csv.DictReader(f))
    expected=[f'{year:04d}-{month:02d}' for year in range(2020,2026) for month in range(1,13) if '2020-09'<=f'{year:04d}-{month:02d}'<='2025-09']
    if [r['month'] for r in rows] != expected:
        raise ValueError('Expected exactly 61 ordered month-end prices, September 2020–September 2025.')
    returns={}
    for key in ('COST_adjclose','SPY_adjclose','SP500_index_close'):
        prices=[float(r[key]) for r in rows]
        if any(not math.isfinite(x) or x<=0 for x in prices):
            raise ValueError('Prices must be positive and finite.')
        returns[key]=[b/a-1 for a,b in zip(prices,prices[1:])]
    print('COST historical beta — 60 monthly raw returns, October 2020–September 2025')
    for key,label in [('SPY_adjclose','SPY dividend-adjusted proxy (main)'),('SP500_index_close','S&P 500 price index (definition comparison)')]:
        slope,alpha,r2,se=beta(returns['COST_adjclose'],returns[key])
        print(f'{label}: beta={slope:.6f}; monthly intercept={alpha:.6%}; R-squared={r2:.4f}; beta standard error={se:.6f}')
    print('No post-September 2025 return observations used. Historical data retrieved October 19, 2026.')
    print('Limitations: raw rather than excess returns; provider adjustments retrieved later; beta depends on period/benchmark and is not a complete risk measure.')


if __name__=='__main__':
    main()
