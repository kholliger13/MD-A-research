"""Normalized FY2026–2030 Costco three-statement model; USD millions.
ABG-style statement and strict-check workflow adapted to Costco's membership model.
Run: .venv/bin/python COST_proforma_from_ABG.py
See costco_proforma_assumptions.md for sources, conventions and limitations.
"""
from math import isfinite

OPENING = dict(sales=269912., fees=5323., cash=14161., investments=1123.,
            receivables=3203., inventory=18116., other_current_assets=1777.,
            ppe=31909., other_assets=6810., payable=19783., salaries=5205.,
            rewards=2677., deferred_fees=2854., other_liabilities=11611.,
            debt=5805., equity=29164.)
ASSUMPTIONS = dict(sales_growth=(.08,.07,.06,.05,.04),
                   fee_growth=(.09,.08,.07,.06,.05),
                   gross_margin=(269912-239886)/269912,
                   sga_ratio=24966/269912, da_ratio=2426/269912,
                   capex_ratio=.02, tax=.251, debt_rate=.04,
                   cash_yield=.03, dividend_payout=.30, shares=444.803,
                   wacc=.08, terminal_growth=.03, terminal_roic=.20,
                   operating_cash_ratio=.02, cost_of_equity=.08)

def working_capital(r):
    return (r['receivables']+r['inventory']+r['other_current_assets']
            -r['payable']-r['salaries']-r['rewards']-r['deferred_fees'])

def project(a=ASSUMPTIONS):
    if len(a['sales_growth']) != 5 or len(a['fee_growth']) != 5:
        raise ValueError('Provide exactly five sales and membership growth assumptions')
    prior = OPENING.copy()
    rows = []
    for i, (sg, fg) in enumerate(zip(a['sales_growth'], a['fee_growth'])):
        r = prior.copy()
        r['year'] = 2026+i
        r['sales'] = prior['sales']*(1+sg)
        r['fees'] = prior['fees']*(1+fg)
        r['revenue'] = r['sales']+r['fees']
        r['cogs'] = r['sales']*(1-a['gross_margin'])
        r['sga'] = r['sales']*a['sga_ratio']
        r['ebit'] = r['revenue']-r['cogs']-r['sga']
        r['da'] = r['sales']*a['da_ratio']  # already included in COGS/SG&A
        r['interest'] = prior['debt']*a['debt_rate']
        r['interest_income'] = (max(0., prior['cash'])+prior['investments'])*a['cash_yield']
        r['pretax'] = r['ebit']-r['interest']+r['interest_income']
        r['tax'] = max(0., r['pretax'])*a['tax']
        r['net_income'] = r['pretax']-r['tax']
        for k in ('receivables','inventory','other_current_assets','payable','salaries','rewards'):
            r[k] = OPENING[k]*r['sales']/OPENING['sales']
        r['deferred_fees'] = OPENING['deferred_fees']*r['fees']/OPENING['fees']
        r['delta_wc'] = working_capital(r)-working_capital(prior)
        r['capex'] = r['sales']*a['capex_ratio']
        r['ppe'] = prior['ppe']+r['capex']-r['da']
        r['cfo'] = r['net_income']+r['da']-r['delta_wc']
        r['cfi'] = -r['capex']
        r['dividends'] = max(0., r['net_income'])*a['dividend_payout']
        r['cff'] = -r['dividends']
        r['cash_change'] = r['cfo']+r['cfi']+r['cff']
        r['cash'] = prior['cash']+r['cash_change']
        r['equity'] = prior['equity']+r['net_income']-r['dividends']
        r['assets'] = sum(r[k] for k in ('cash','investments','receivables','inventory','other_current_assets','ppe','other_assets'))
        r['liabilities'] = sum(r[k] for k in ('payable','salaries','rewards','deferred_fees','other_liabilities','debt'))
        r['balance_gap'] = r['assets']-r['liabilities']-r['equity']
        r['operating_cash_investment'] = (r['sales']-prior['sales'])*a['operating_cash_ratio']
        r['fcff'] = r['ebit']-max(0., r['ebit'])*a['tax']+r['da']-r['capex']-r['delta_wc']-r['operating_cash_investment']
        # Net borrowing is zero under the unchanged-debt policy; dividends are not deducted.
        r['fcfe'] = r['cfo']-r['capex']-r['operating_cash_investment']
        r['funding_shortfall'] = max(0., r['sales']*a['operating_cash_ratio']-r['cash'])
        check_gap(r['year'], 'balance sheet', r['balance_gap'])
        # A liquidity failure is reported, not hidden or allowed to stop all statements.
        r['cash_gap'] = r['cash']-prior['cash']-r['cash_change']
        r['cash_headroom'] = r['cash']-r['sales']*a['operating_cash_ratio']
        check_gap(r['year'], 'cash reconciliation', r['cash_gap'])
        rows.append(r)
        prior = r
    return rows

def value(rows, wacc=.08, growth=.03, roic=.20, a=ASSUMPTIONS):
    if not (0 <= growth < wacc and roic > growth and a['shares'] > 0):
        raise ValueError('Require WACC > terminal growth >= 0, ROIC > growth, and positive shares')
    pv_five = sum(r['fcff']/(1+wacc)**t for t,r in enumerate(rows,1))
    # Sustainable terminal reinvestment = growth / incremental return on capital.
    terminal_fcff = rows[-1]['ebit']*(1-a['tax'])*(1+growth)*(1-growth/roic)
    if rows[-1]['fcff'] <= 0 or terminal_fcff <= 0:
        return None  # Recovery assumptions are required before a terminal valuation.
    pv_terminal = terminal_fcff/(wacc-growth)/(1+wacc)**len(rows)
    excess_cash = OPENING['cash']-OPENING['sales']*a['operating_cash_ratio']
    equity = pv_five+pv_terminal+excess_cash+OPENING['investments']-OPENING['debt']
    return dict(pv_five=pv_five,pv_terminal=pv_terminal,enterprise=pv_five+pv_terminal,
                equity=equity,per_share=equity/a['shares'],
                terminal_share=pv_terminal/(pv_five+pv_terminal) if pv_five+pv_terminal else float('nan'))

def report(a=ASSUMPTIONS):
    rows = project(a)
    sections = {
        'Income statement': [('Net sales','sales'),('Membership fees','fees'),('Total revenue','revenue'),('Merchandise costs','cogs'),('SG&A (includes D&A)','sga'),('Operating income','ebit'),('Interest expense','interest'),('Interest income','interest_income'),('Pretax income','pretax'),('Tax expense','tax'),('Net income','net_income')],
        'Balance sheet': [(k.replace('_',' ').title(),k) for k in ('cash','investments','receivables','inventory','other_current_assets','ppe','other_assets','assets','payable','salaries','rewards','deferred_fees','other_liabilities','debt','liabilities','equity','balance_gap')],
        'Cash flow statement': [('Net income','net_income'),('D&A addback','da'),('Increase in operating working capital','delta_wc'),('Operating cash flow','cfo'),('Investing cash flow','cfi'),('Dividends paid','dividends'),('Financing cash flow','cff'),('Change in cash','cash_change'),('Closing cash','cash'),('FCFF after operating cash investment','fcff'),('FCFE before dividends, after operating cash investment','fcfe'),('Unfunded operating-cash shortfall','funding_shortfall')]
    }
    out = ['# Costco normalized five-year pro forma','', 'USD millions; FY2025 base. Costs shown as positive amounts. Model assumptions, not guidance.','']
    for title, fields in sections.items():
        out += ['## '+title,'','| Item | 2026 | 2027 | 2028 | 2029 | 2030 |','|---|---:|---:|---:|---:|---:|']
        out += ['| '+label+' | '+' | '.join(f'{r[key]:,.1f}' for r in rows)+' |' for label,key in fields]
        out += ['']
    out += ['## FCFE: positive-only classroom calculation','',
            '| Year | FCFE | Status | PV of positive FCFE |',
            '|---|---:|---|---:|']
    positive_pv = 0.
    for t, r in enumerate(rows, 1):
        pv = max(0., r['fcfe'])/(1+a['cost_of_equity'])**t
        positive_pv += pv
        status = 'negative FCFE' if r['fcfe'] < 0 else ('positive FCFE' if r['fcfe'] > 0 else 'zero FCFE')
        out.append(f"| {r['year']} | {r['fcfe']:,.2f} | {status} | {pv:,.2f} |")
    out += ['', f"PV of positive forecast FCFE only: ${positive_pv:,.2f} million at {a['cost_of_equity']:.1%} assumed cost of equity.",
            'This subtotal excludes cash deficits and terminal value; it is not a complete equity valuation.',
            'FCFE terminal value: not estimated in this subtotal.',
            'A perpetuity formula can produce a negative number, but negative cash flow cannot support a meaningful positive going-concern terminal value without a defensible path to sustainable positive cash flow.', '']
    v=value(rows, a['wacc'], a['terminal_growth'], a['terminal_roic'], a)
    if v is None:
        out += ['Full FCFF valuation and sensitivity: unresolved; no terminal value assigned to nonpositive final-year or terminal cash flow.']
    else:
        out += ['## Separate full FCFF valuation (includes all signed forecast FCFF)','',*[f'- {k}: {val:,.2f}' for k,val in v.items()],'',
            'Terminal share is a fraction of enterprise value. Per share is USD/share; other values are USD millions.','',
            '## Per-share sensitivity (terminal ROIC 20%)','','| WACC / terminal growth | 2% | 3% | 4% |','|---|---:|---:|---:|']
        for w in (.07,.08,.09):
            out.append(f'| {w:.0%} | '+' | '.join(f"${value(rows,w,g,a['terminal_roic'],a)['per_share']:,.2f}" for g in (.02,.03,.04))+' |')
    if a == ASSUMPTIONS:
        out += ['', 'The model estimates $349.58 per share because it discounts forecast operating cash flows and continuing operations at 8%, assumes 3% perpetual growth with a 20% return on new capital, then adjusts for excess cash, investments and debt and divides by 444.803 million shares; about 84% of operating value comes from cash flows after 2030. Stronger sustained membership and sales growth, higher margins, or a lower required return would raise the estimate, while weaker performance or greater reinvestment needs would lower it; holding other assumptions fixed, changing the discount rate from 8% to 7% raises value to $439.50, whereas 9% lowers it to $289.79.']
    out += ['', 'Checks: all five balance sheets balance and cash reconciles.']
    for r in rows:
        out.append(f"- {r['year']} operating cash: "+('PASS' if not r['funding_shortfall'] else f"FAIL — unfunded shortfall ${r['funding_shortfall']:,.2f} million; financing unresolved. Negative cash, if shown, is an unfunded deficit, not a feasible cash balance."))
    return '\n'.join(out)+'\n'


def check_gap(year, name, gap, tolerance=1e-7):
    if not isfinite(gap) or abs(gap) > tolerance:
        raise ValueError(f"{year}: {name} check failed; gap = {gap:.10f} million")

def check_opening():
    assets = sum(OPENING[k] for k in ('cash','investments','receivables','inventory','other_current_assets','ppe','other_assets'))
    liabilities = sum(OPENING[k] for k in ('payable','salaries','rewards','deferred_fees','other_liabilities','debt'))
    check_gap(2025, 'opening balance sheet', assets-liabilities-OPENING['equity'])
    return assets, liabilities

def check_block(rows):
    lines = ['## CHECK BLOCK', '', '| USD millions | 2026 | 2027 | 2028 | 2029 | 2030 |', '|---|---:|---:|---:|---:|---:|']
    for label,key in [('Assets minus liabilities and equity','balance_gap'),('Cash reconciliation gap','cash_gap'),('Cash above required minimum','cash_headroom')]:
        lines.append('| '+label+' | '+' | '.join(f"{0. if abs(r[key])<1e-7 else r[key]:,.2f}" for r in rows)+' |')
    return '\n'.join(lines)

def assert_balanced(rows):
    for r in rows:
        check_gap(r['year'], 'balance sheet', r['balance_gap'])
        check_gap(r['year'], 'cash reconciliation', r['cash_gap'])
        gap = r['cash_headroom']
        if not isfinite(gap) or gap < -1e-7:
            raise ValueError(f"{r['year']}: minimum-cash check failed; gap = {gap:.10f} million; financing assumption unresolved")

def opening_table():
    assets, liabilities = check_opening()
    labels = [('Cash','cash'),('Short-term investments','investments'),('Receivables','receivables'),('Inventory','inventory'),('Other current assets','other_current_assets'),('PP&E, net','ppe'),('Other assets, including lease ROU assets','other_assets'),('Accounts payable','payable'),('Accrued salaries','salaries'),('Accrued member rewards','rewards'),('Deferred membership fees','deferred_fees'),('Debt, including current portion','debt'),('Other liabilities, including leases','other_liabilities'),('Shareholders equity','equity')]
    lines = ['## Opening balance sheet — FY2025', '', '| Item | USD millions |', '|---|---:|']
    lines += [f"| {label} | {OPENING[key]:,.2f} |" for label,key in labels]
    lines += [f'| Total assets | {assets:,.2f} |',f'| Total liabilities | {liabilities:,.2f} |',f"| Liabilities plus equity | {liabilities+OPENING['equity']:,.2f} |", '| Opening balance gap | 0.00 |']
    return '\n'.join(lines)

ASSUMPTION_TABLE = """
## Assumption set

| Value | Label | Reason |
|---|---|---|
| Sales growth: 8%, 7%, 6%, 5%, 4% | Judgment | Fade growth as the business expands; includes comparable sales and new warehouses. |
| Membership revenue growth: 9%, 8%, 7%, 6%, 5% | Judgment | Fade fee-increase benefits while retaining member growth. |
| Merchandise gross margin: 11.124366% | Judgment | Hold FY2025 merchandise economics constant. |
| SG&A / merchandise gross profit: 83.147938% (equivalent to 9.249681% of net sales) | Judgment | Preserve FY2025 efficiency; expenses already include D&A. |
| Inventory days: 27.564510 | Judgment | Preserve FY2025 inventory / merchandise-cost ratio, using 365 days. |
| Historical D&A / ending net PP&E: 7.602871% | History | Historical comparator, not the forecast depreciation formula. |
| Forecast D&A / net sales: 0.898811% | Judgment | Maintain historical intensity without an asset-vintage schedule. |
| Capital spending: 2% of net sales | Judgment | Maintain investment intensity for expansion and maintenance. |
| Tax: 25.1%; no current tax benefit on losses | Judgment | Hold the historical effective rate; do not assume immediate loss monetization. |
| Floor plan: none; replacement line: membership revenue and deferred fees | Judgment | Model membership economics separately from merchandise and supplier financing. |
| Opening membership revenue 5,323; deferred fees 2,854 | History | FY2025 audited inputs. |
| Deferred fees / membership revenue: 2,854 / 5,323 | Judgment | Preserve upfront collection versus recognition relationship. |
| Receivables, inventory, other current assets, payables, salaries and rewards: fixed opening ratios to sales | Judgment | Maintain operating efficiency and funding relationships. |
| Cash floor: 2% of sales | Judgment | Reserve approximately one week of sales for liquidity. |
| Debt: 5,805, constant; net borrowing zero | Judgment | Refinance maturities at unchanged principal. |
| Debt interest 4%; cash and investment yield 3% | Judgment | Normalized rates, not market quotes. |
| Dividends: 30% of positive income; no buybacks | Judgment | Simple distribution policy, with no negative dividends. |
| Other long-term assets, other liabilities and short-term investments: constant | Judgment | Simplify balances without detailed schedules. |
| No impairments, acquisitions, FX or deferred-tax changes | Judgment | No event-specific forecast evidence; use normalized operations. |
| Compensation treated as cash-equivalent; no SBC addback or share issuance | Judgment | Retain its economic cost without granting free cash from dilution. |
| Shares: 444.803 million, constant | Judgment | Historical diluted weighted-average proxy with no net dilution assumed. |
| WACC 8%; cost of equity 8% | Judgment | Required-return scenarios, not date-matched market estimates. |
| Terminal growth 3%; incremental ROIC 20% | Judgment | Mature nominal growth with 15% reinvestment; both are valuation judgments. |

Historical source: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm
Opening aggregates: other assets = 2,725 + 4,085 = 6,810; other liabilities = 47,935 - 5,805 - 19,783 - 5,205 - 2,677 - 2,854 = 11,611. Current debt is included once. Operating leases stay in operating costs and are not separately deducted as financial debt.
Cash is rolled from cash flows, equity from earnings less dividends, and PP&E from capex less D&A. D&A is not deducted twice. No ABG floor-plan funding or impairment charge is carried over.
"""

def main():
    print(opening_table())
    print(ASSUMPTION_TABLE)
    rows = project()
    print(report())
    print(check_block(rows))
    assert_balanced(rows)
    print('All five years: balance sheet PASS; cash reconciliation PASS; minimum cash PASS.')
    v = value(rows)
    if v is not None:
        print(f"Value per share (full FCFF DCF): ${v['per_share']:,.2f}")
    else:
        print('Value per share: unresolved; terminal cash flow requires a recovery case.')

if __name__ == '__main__':
    main()
