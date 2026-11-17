"""October 8, 2025 annual GAAP P/E cross-check. Standard library only.
Preserves older costco_pe.py. This is not an enterprise-value calculation.
"""
import argparse, math
PRICE_DATE='2025-10-08'
TARGET=dict(ticker='COST',price=914.80,eps=18.21,fiscal_end='2025-08-31')
PEERS=[dict(ticker='BJ',price=89.15,eps=4.00,fiscal_end='2025-02-01',decision='USE'),
       dict(ticker='WMT',price=102.90,eps=2.41,fiscal_end='2025-01-31',decision='QUALIFY')]


def calculate(peers=PEERS):
    rows=[]; seen={TARGET['ticker']}
    for peer in peers:
        if peer['ticker'] in seen:
            raise ValueError('Duplicate peer or target in peer set.')
        seen.add(peer['ticker'])
        if any(not math.isfinite(peer[k]) or peer[k]<=0 for k in ('price','eps')):
            raise ValueError('Positive finite price and earnings required.')
        multiple=peer['price']/peer['eps']
        rows.append(dict(peer,multiple=multiple,implied_costco_price=multiple*TARGET['eps']))
    return rows


def report(remove=None):
    if remove is not None and remove not in {r['ticker'] for r in PEERS}:
        raise ValueError('Unknown peer to remove.')
    rows=calculate([p for p in PEERS if p['ticker']!=remove])
    out=['# Costco annual GAAP P/E peer cross-check — October 8, 2025','',
         'Prepared October 19, 2026. USD/share. These are unadjusted historical closes and annual reported GAAP diluted EPS.',
         'Policy retained from Lab 8: BJ is the closer membership-club peer (USE); Walmart is a broader retail comparison (QUALIFY). No peers selected by desired valuation result.', '',
         '| Peer | Price | Annual EPS | Fiscal end | P/E | Implied Costco price |',
         '|---|---:|---:|---|---:|---:|']
    for r in rows:
        out.append(f"| {r['ticker']} ({r['decision']}) | ${r['price']:.2f} | ${r['eps']:.2f} | {r['fiscal_end']} | {r['multiple']:.4f}x | ${r['implied_costco_price']:.2f} |")
    if len(rows)>1:
        values=[r['implied_costco_price'] for r in rows]
        out+=['',f'Peer-implied range: ${min(values):.2f}–${max(values):.2f}. No averaging with DCF.']
    elif rows:
        out+=['',f"Single-peer reference only: ${rows[0]['implied_costco_price']:.2f}; no peer range."]
    out+=['',f"Costco own annual P/E: {TARGET['price']/TARGET['eps']:.4f}x. Costco is not included in the peer set.",'',
          '## Definitions, dates and limitations','',
          '- Annual earnings, not trailing-twelve-month, adjusted or forward earnings. Costco FY2025; BJ FY2024; Walmart FY2025. Fiscal periods differ substantially; newer quarterly reports available by the cutoff still need review for a current-period cross-check.',
          '- BJ results published March 6, 2025; Walmart February 20, 2025. Both precede the valuation date. Costco annual EPS was published September 25, 2025; its 10-K was filed October 8.',
          '- Share prices are rounded to quoted cents before calculating. Walmart fiscal EPS is already restated for the 2024 stock split; no additional split adjustment applied.',
          '- P/E estimates Costco equity directly using its $18.21 annual diluted EPS; do not add cash or subtract debt again from these implied prices.',
          '- Business differences can justify different multiples; this calculation does not establish the correct Costco premium.',
          '- Enterprise-value multiple remains pending. BJ financing obligations beyond borrowings and leases, and relevant Walmart nonoperating assets/minority interests, need definition checks before that calculation.', '',
          '## Sources','',
          '- BJ FY2024 annual results, annual diluted EPS $4.00: https://investors.bjs.com/press-releases/press-release-details/2025/BJs-Wholesale-Club-Holdings-Inc.-Announces-Fourth-Quarter-and-Full-Fiscal-2024-Results/default.aspx',
          '- BJ FY2024 10-K: https://www.sec.gov/Archives/edgar/data/1531152/000153115225000013/bj-20250201.htm',
          '- Walmart FY2025 results, annual diluted EPS $2.41: https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-25-000010/earningsreleasefy25q4.htm',
          '- Costco FY2025 10-K, p. 37: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm',
          '- Price API requests, full provider payloads, observation-date and close-field metadata: costco_peer_prices_2025_sources.json.', '']
    return '\n'.join(out)+'\n'


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--remove',choices=['BJ','WMT'])
    args=parser.parse_args()
    print(report(args.remove),end='')
