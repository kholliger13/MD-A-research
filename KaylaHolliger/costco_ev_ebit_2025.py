"""Provisional annual EV/EBIT comparison at October 8, 2025.
USD millions except prices. Financing assets/liabilities use older annual proxies.
Walmart is a qualified broad-retail peer; BJ EV calculation remains unresolved.
"""
import math

WMT = dict(price=102.90, shares=8016.849444, short_borrowing=3068.,
           current_long_debt=2598., long_debt=33401.,
           current_finance_lease=800., long_finance_lease=5923.,
           redeemable_nci=271., other_nci=6408., cash=9037.,
           equity_investments=3041., asda_debt_investment=1200., ebit=29348.)
COST = dict(price=914.80, shares=443.179176, diluted_share_proxy=444.803,
            borrowings_net=5788., finance_leases=1479., cash=14161.,
            investments=1123., ebit=10383., ebit_allocation_upper=10446.)


def calculate(wmt=None, cost=None):
    wmt=dict(WMT if wmt is None else wmt);cost=dict(COST if cost is None else cost)
    if any(not math.isfinite(x) or x<0 for x in (*wmt.values(),*cost.values())):
        raise ValueError('Inputs must be finite and nonnegative.')
    if min(wmt['shares'],wmt['ebit'],cost['diluted_share_proxy'],cost['ebit'])<=0:
        raise ValueError('Positive shares and EBIT required.')
    equity=wmt['price']*wmt['shares']
    borrowings=sum(wmt[k] for k in ('short_borrowing','current_long_debt','long_debt'))
    leases=wmt['current_finance_lease']+wmt['long_finance_lease']
    nci=wmt['redeemable_nci']+wmt['other_nci']
    investments=wmt['equity_investments']+wmt['asda_debt_investment']
    ev=equity+borrowings+leases+nci-wmt['cash']-investments
    multiple=ev/wmt['ebit']
    implied_ev=multiple*cost['ebit']
    bridge=cost['cash']+cost['investments']-cost['borrowings_net']-cost['finance_leases']
    implied_equity=implied_ev+bridge
    return dict(wmt_equity=equity,wmt_borrowings=borrowings,wmt_finance_leases=leases,
                wmt_nci=nci,wmt_investments=investments,wmt_ev=ev,multiple=multiple,
                implied_costco_ev=implied_ev,costco_bridge=bridge,
                implied_costco_equity=implied_equity,
                implied_costco_price=implied_equity/cost['diluted_share_proxy'],
                allocation_upper_price=(multiple*cost['ebit_allocation_upper']+bridge)/cost['diluted_share_proxy'])


def report():
    r=calculate()
    out=['# Costco enterprise-value cross-check — annual EV/EBIT','',
         'Prepared October 19, 2026. Valuation price date October 8, 2025. USD millions except per-share data and multiples.',
         'PROVISIONAL: annual balance-sheet/share-count proxies, not reconstructed October 8 enterprise values.', '',
         '## Policy and definitions','',
         '- Peer policy retained: BJ USE as closer membership-club peer; Walmart QUALIFY as broader retailer. Walmart supplies one EV multiple because its selected adjustments are identified; BJ is not excluded for its valuation result.',
         '- EV = common equity market value + borrowings + finance leases + minority interests - cash - identified nonoperating investments. Operating lease liabilities excluded; related rent remains in reported EBIT.',
         '- Denominator: consolidated annual reported operating income (EBIT), not net income, adjusted EBITDA or forward earnings. Walmart FY2025 ends January 31, 2025; Costco FY2025 ends August 31, 2025.',
         '- All cash is deducted for this conventional peer reference, unlike the DCF excess-cash-only convention. This and stale dates are explicit method differences; do not mechanically average.',
         '- Book borrowings and lease/NCI values are valuation proxies. Walmart shares 8,016.849444 million are outstanding March 12, 2025, from its 10-K cover, not weighted-average diluted shares or confirmed October 8 shares.',
         '- Walmart equity investments 3,041 and Asda debt investment approximately 1,200 are deducted because associated investment returns are outside operating income. The latter is rounded and may require a realizability haircut.',
         '- Target diluted denominator 444.803 remains a historical proxy. Costco reported EBIT could contain up to 63 of finance-lease interest; a supplementary upper endpoint removes that amount. Other definition differences remain.', '',
         '## Walmart EV build','',
         '| Component | USD millions |','|---|---:|',
         f"| Price 102.90 × outstanding shares 8,016.849444 | {r['wmt_equity']:,.6f} |",
         f"| Add borrowings (3,068 + 2,598 + 33,401) | {r['wmt_borrowings']:,.3f} |",
         f"| Add finance leases (800 + 5,923) | {r['wmt_finance_leases']:,.3f} |",
         f"| Add minority interests (271 + 6,408) | {r['wmt_nci']:,.3f} |",
         '| Deduct cash | 9,037.000 |',
         f"| Deduct identified investments (3,041 + approx. 1,200) | {r['wmt_investments']:,.3f} |",
         f"| Provisional EV | {r['wmt_ev']:,.6f} |",'| Annual operating income | 29,348.000 |',
         f"| EV / EBIT | {r['multiple']:.6f}x |",'',
         '## Apply the multiple to Costco','',
         f"- Implied Costco EV: {r['multiple']:.6f} × 10,383 = {r['implied_costco_ev']:,.6f}.",
         '- Costco equity bridge: add cash 14,161 and investments 1,123; subtract net borrowings 5,788 and finance leases 1,479; no NCI assumed from the reported consolidated equity.',
         f"- Implied equity: {r['implied_costco_equity']:,.6f}; divide by 444.803 million diluted share proxy = ${r['implied_costco_price']:.2f}/share.",
         f"- If all 63 of disclosed finance-lease interest were reclassified out of operating costs, the reference becomes ${r['allocation_upper_price']:.2f}/share. This is an allocation sensitivity, not a business range.",
         '- Single qualified peer: no EV peer range and no median. Walmart business mix differs from Costco.', '',
         '## Outstanding checks','',
         '- Update market capitalization and financing balances using latest filings public by cutoff; consider TTM earnings to reduce period mismatch.',
         '- BJ has 575 gross borrowings, 28.204 finance leases and 63.619 noncurrent financing obligations (USD millions). Current financing obligations are not separately quantified in the reviewed table. BJ EV remains unresolved; do not assume missing financing is zero.',
         '- The completeness and realizable value of nonoperating assets and minority interests remain subject to review; their book values are proxies.', '',
         '## Sources and locators','',
         '- Walmart FY2025 10-K (filed March 14, 2025): cover shares; p. 53 EBIT; p. 55 cash, debt, finance leases and NCI; p. 60 Asda debt investment; p. 70 equity investments: https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-25-000021/wmt-20250131.htm',
         '- Costco FY2025 10-K: pp. 37, 39, 52–53: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm',
         '- BJ FY2024 10-K: Notes 6, 7, 16, 17: https://www.sec.gov/Archives/edgar/data/1531152/000153115225000013/bj-20250201.htm',
         '- October 8 unadjusted closing-price observation preserved in costco_peer_prices_2025_sources.json.', '']
    return '\n'.join(out)+'\n'


if __name__=='__main__':
    print(report(),end='')
