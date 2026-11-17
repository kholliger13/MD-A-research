"""Project 1 revised model draft: opening classification and provisional finance-lease schedule.
USD millions. Source: Costco FY2025 10-K, pp. 39, 52-54.
Provisional three-statement and DCF integration.
Results depend on unresolved source and modeling assumptions; not a final recommendation.
Original COST_proforma.py is preserved.
"""

OPENING = dict(
    assets=77099.0,
    borrowings_gross=5805.0,
    debt_discounts_and_issuance_costs=17.0,
    finance_leases_current=78.0,
    finance_leases_long_term=1401.0,
    operating_leases_current=208.0,
    operating_leases_long_term=2460.0,
    total_liabilities=47935.0,
    equity=29164.0,
)


def opening_reconciliation():
    b = OPENING
    borrowings_net = b['borrowings_gross'] - b['debt_discounts_and_issuance_costs']
    finance_leases = b['finance_leases_current'] + b['finance_leases_long_term']
    operating_leases = b['operating_leases_current'] + b['operating_leases_long_term']
    other_liabilities = b['total_liabilities'] - borrowings_net - finance_leases - operating_leases
    gap = b['assets'] - borrowings_net - finance_leases - operating_leases - other_liabilities - b['equity']
    if abs(gap) > 1e-7:
        raise ValueError(f'Opening balance sheet fails: {gap}')
    return dict(borrowings_net=borrowings_net, finance_leases=finance_leases,
                operating_leases=operating_leases, remaining_liabilities=other_liabilities,
                balance_gap=gap)


# Historical anchors: Note 5, pp. 53-54. Forecast ratios below are analyst
# simplifications, not contractual payment schedules or company guidance.
LEASE_BASE = dict(asset=1488.0, liability=1479.0, additions=131.0,
                  amortization=102.0, principal=147.0, rate=0.0463)
PROPOSED_SALES_GROWTH = (0.08, 0.07, 0.06, 0.05, 0.05)


def finance_lease_schedule(growth=PROPOSED_SALES_GROWTH, additions_multiplier=1.0):
    from math import isfinite
    if len(growth) != 5 or any(not isfinite(g) or g <= -1 for g in growth):
        raise ValueError('Provide five finite sales growth rates above -100%.')
    if not isfinite(additions_multiplier) or additions_multiplier < 0:
        raise ValueError('Lease additions multiplier must be finite and nonnegative.')
    asset, liability, sales_factor = LEASE_BASE['asset'], LEASE_BASE['liability'], 1.0
    rows = []
    for year, g in enumerate(growth, 2026):
        sales_factor *= 1 + g
        additions = LEASE_BASE['additions'] * sales_factor * additions_multiplier
        amortization = asset * LEASE_BASE['amortization'] / LEASE_BASE['asset']
        principal = liability * LEASE_BASE['principal'] / LEASE_BASE['liability']
        interest = liability * LEASE_BASE['rate']
        closing_asset = asset + additions - amortization
        closing_liability = liability + additions - principal
        asset_gap = closing_asset - asset - additions + amortization
        debt_gap = closing_liability - liability - additions + principal
        if any(not isfinite(x) or x < 0 for x in
               (additions, amortization, principal, interest, closing_asset, closing_liability)):
            raise ValueError('Invalid finance-lease forecast.')
        if max(abs(asset_gap), abs(debt_gap)) > 1e-7:
            raise ValueError('Finance-lease roll-forward fails.')
        rows.append(dict(year=year, additions=additions, amortization=amortization,
                         principal=principal, interest=interest,
                         closing_asset=closing_asset, closing_liability=closing_liability,
                         asset_gap=asset_gap, liability_gap=debt_gap))
        asset, liability = closing_asset, closing_liability
    return rows


# Proposed assumptions, not guidance. Multiple changes are introduced together;
# this integration run is NOT the student's locked changed-input test.
MODEL_BASE = dict(sales=269912.0, fees=5323.0, cash=14161.0,
                  investments=1123.0, receivables=3203.0, inventory=18116.0,
                  other_current_assets=1777.0, ppe=31909.0,
                  other_assets_ex_finance_leases=5322.0,
                  payable=19783.0, salaries=5205.0, rewards=2677.0,
                  deferred_fees=2854.0, remaining_liabilities=7481.0,
                  equity=29164.0)
MODEL_ASSUMPTIONS = dict(fee_growth=(.09,.08,.07,.06,.05),
                        gross_margin=30026/269912, sga_ratio=24966/269912,
                        tax=.261, capex_ratio=.02, borrowing_rate=.04,
                        cash_yield=.03, dividend_payout=.30)
WC_ASSETS = ('receivables', 'inventory', 'other_current_assets')
WC_LIABILITIES = ('payable', 'salaries', 'rewards', 'deferred_fees')


def working_capital(row):
    return sum(row[k] for k in WC_ASSETS) - sum(row[k] for k in WC_LIABILITIES)


def project(additions_multiplier=1.0, lease_interest_in_costs=0.0,
            sales_growth=None, assumption_overrides=None):
    from math import isfinite
    if not isfinite(lease_interest_in_costs) or not 0 <= lease_interest_in_costs <= 63:
        raise ValueError("Historical finance-lease interest allocation must be between 0 and 63 million.")
    base, a = MODEL_BASE, dict(MODEL_ASSUMPTIONS)
    overrides = {} if assumption_overrides is None else dict(assumption_overrides)
    unknown = set(overrides)-set(a)
    if unknown:
        raise ValueError(f'Unknown assumption overrides: {sorted(unknown)}')
    a.update(overrides)
    sales_growth = PROPOSED_SALES_GROWTH if sales_growth is None else tuple(sales_growth)
    if len(sales_growth)!=5 or len(a['fee_growth'])!=5:
        raise ValueError('Five annual sales and fee growth rates required.')
    if any(not isfinite(g) or g<=-1 for g in (*sales_growth,*a['fee_growth'])):
        raise ValueError('Growth rates must be finite and above -100%.')
    for key in ('gross_margin','sga_ratio','tax','capex_ratio','borrowing_rate','cash_yield','dividend_payout'):
        if not isfinite(a[key]) or not 0<=a[key]<=1:
            raise ValueError(f'{key} must be finite and between zero and one.')
    opening = opening_reconciliation()
    prior = dict(base)
    prior['finance_lease_asset'] = LEASE_BASE['asset']
    prior['finance_lease_liability'] = LEASE_BASE['liability']
    base_assets = sum(base[k] for k in ('cash','investments', *WC_ASSETS,
                                      'ppe','other_assets_ex_finance_leases')) + LEASE_BASE['asset']
    base_liabilities = sum(base[k] for k in WC_LIABILITIES) + base['remaining_liabilities'] + opening['operating_leases'] + opening['borrowings_net'] + LEASE_BASE['liability']
    if abs(base_assets - OPENING['assets']) > 1e-7 or abs(base_liabilities - OPENING['total_liabilities']) > 1e-7:
        raise ValueError('Opening classifications do not reconcile to the filing.')
    rows = []
    leases = finance_lease_schedule(growth=sales_growth, additions_multiplier=additions_multiplier)
    for i, (sg, fg, lease) in enumerate(zip(sales_growth, a['fee_growth'], leases)):
        row = dict(prior)
        row['year'] = 2026+i
        row['sales'] = prior['sales']*(1+sg)
        row['fees'] = prior['fees']*(1+fg)
        factor = row['sales']/base['sales']
        row['revenue'] = row['sales']+row['fees']
        row['merchandise_costs_and_sga_before_lease_amortization'] = row['sales']*(1-a['gross_margin']+a['sga_ratio'])-LEASE_BASE['amortization']*factor-lease_interest_in_costs*factor
        row['lease_interest_removed_from_operating_costs'] = lease_interest_in_costs*factor
        row['lease_amortization'] = lease['amortization']
        row['ebit'] = row['revenue']-row['merchandise_costs_and_sga_before_lease_amortization']-row['lease_amortization']
        # Provisional: 2,426 total D&A less 102 finance-lease amortization.
        # Remaining D&A is assigned to PP&E; other amortization is not identified.
        row['ppe_depreciation_proxy'] = (2426-102)*factor
        row['da'] = row['ppe_depreciation_proxy']+row['lease_amortization']
        row['borrowing_interest'] = OPENING['borrowings_gross']*a['borrowing_rate']
        row['lease_interest'] = lease['interest']
        row['interest_income'] = (max(0,prior['cash'])+base['investments'])*a['cash_yield']
        row['pretax'] = row['ebit']-row['borrowing_interest']-row['lease_interest']+row['interest_income']
        row['tax'] = max(0,row['pretax'])*a['tax']
        row['net_income'] = row['pretax']-row['tax']
        for k in (*WC_ASSETS, 'payable','salaries','rewards'):
            row[k] = base[k]*factor
        row['deferred_fees'] = base['deferred_fees']*row['fees']/base['fees']
        row['delta_wc'] = working_capital(row)-working_capital(prior)
        row['capex'] = a['capex_ratio']*row['sales']
        row['ppe'] = prior['ppe']+row['capex']-row['ppe_depreciation_proxy']
        row['lease_additions_noncash'] = lease['additions']
        row['finance_lease_asset'] = lease['closing_asset']
        row['finance_lease_liability'] = lease['closing_liability']
        row['lease_principal'] = lease['principal']
        row['cfo'] = row['net_income']+row['da']-row['delta_wc']
        row['cfi'] = -row['capex']
        row['dividends'] = max(0,row['net_income'])*a['dividend_payout']
        row['cff'] = -row['dividends']-row['lease_principal']
        row['cash_change'] = row['cfo']+row['cfi']+row['cff']
        row['cash'] = prior['cash']+row['cash_change']
        row['equity'] = prior['equity']+row['net_income']-row['dividends']
        row['assets'] = sum(row[k] for k in ('cash','investments', *WC_ASSETS,
                              'ppe','other_assets_ex_finance_leases','finance_lease_asset'))
        row['liabilities'] = sum(row[k] for k in WC_LIABILITIES)+base['remaining_liabilities']+opening['operating_leases']+opening['borrowings_net']+row['finance_lease_liability']
        row['balance_gap'] = row['assets']-row['liabilities']-row['equity']
        row['cash_gap'] = row['cash']-prior['cash']-row['cfo']-row['cfi']-row['cff']
        row['lease_asset_gap'] = lease['asset_gap']
        row['lease_liability_gap'] = lease['liability_gap']
        row['cash_floor_shortfall'] = max(0,.02*row['sales']-row['cash'])
        for k in ('balance_gap','cash_gap','lease_asset_gap','lease_liability_gap'):
            if not isfinite(row[k]) or abs(row[k]) > 1e-7:
                raise ValueError(f"{row['year']} {k} failed: {row[k]}")
        rows.append(row)
        prior=row
    return rows


def report():
    rows = project()
    opening = opening_reconciliation()
    out = ['# Costco revised model — provisional statement integration', '',
           'Run date: October 19, 2026. USD millions. FY2025 opening balances; FY2026–2030 forecast.',
           'Not a final October 8, 2025 valuation. Source review remains pending. Use --dcf for a separately labeled provisional valuation with timing estimates.', '',
           'Source: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm (pp. 39, 41, 52–54).', '',
           '## Forecast assumptions and limits', '',
           '- Sales growth: 8%, 7%, 6%, 5%, 5%; fee growth: 9%, 8%, 7%, 6%, 5%; tax: 26.1%. These are provisional analyst assumptions.',
           '- Borrowings net: 5,788; finance leases: 1,479; operating leases: 2,668; remaining liabilities including working-capital items: 38,000.',
           '- New finance-lease assets are noncash additions with equal liability additions; they are not cash capex or cash borrowing proceeds. Principal payments are financing cash outflows.',
           '- Finance-lease amortization is separated from existing expense ratios and replaced by the schedule amount. Total D&A is added back once.',
           '- Finance-lease additions scale from 131 with sales; amortization uses 102/1,488 of opening assets; principal uses 147/1,479 of opening liabilities; interest uses 4.63% of opening liabilities. These are simplifying assumptions, not contractual payments.',
           '- Provisional D&A allocation: 2,426 less 102 finance-lease amortization is assigned to PP&E. Verify remaining amortization before finalizing.',
           '- Operating lease assets/liabilities and other residual balances remain constant. Replacement lease activity and accounting are simplified.',
           '- Borrowings are refinanced at constant principal; their 17 discount/cost balance is held constant. Assumed interest is 4%.',
           '- Finance-lease interest is provisionally placed below EBIT. Note 5 says some interest is in merchandise costs, but does not quantify that split; expense allocation remains unresolved. The default statements use zero embedded interest; --dcf compares both allocation endpoints.',
           '- Stock compensation remains an economic expense, with no forecast addback or new award issuance; historical GAAP cash-flow reconciliation remains separate.',
           '- This is a simultaneous integration run, not a cold run or human-authored locked changed-input test.', '']
    groups = {
        'Income statement': [('Net sales','sales'),('Membership fees','fees'),('Total revenue','revenue'),('Merchandise costs + SG&A before finance-lease amortization','merchandise_costs_and_sga_before_lease_amortization'),('Finance-lease amortization','lease_amortization'),('Operating income','ebit'),('Borrowing interest','borrowing_interest'),('Finance-lease interest','lease_interest'),('Interest income','interest_income'),('Pretax income','pretax'),('Income taxes','tax'),('Net income','net_income')],
        'Balance sheet': [(k.replace('_',' ').title(),k) for k in ('cash','investments',*WC_ASSETS,'ppe','other_assets_ex_finance_leases','finance_lease_asset','assets',*WC_LIABILITIES,'remaining_liabilities','finance_lease_liability','liabilities','equity')],
        'Cash flow and noncash lease activity': [('Net income','net_income'),('D&A addback','da'),('Increase in working capital (deduct)','delta_wc'),('Operating cash flow','cfo'),('Cash capex','capex'),('Investing cash flow','cfi'),('Dividends','dividends'),('Finance-lease principal paid','lease_principal'),('Financing cash flow','cff'),('Change in cash','cash_change'),('Closing cash','cash'),('Noncash lease additions (disclosure only)','lease_additions_noncash')],
        'Checks': [(k.replace('_',' ').title(),k) for k in ('balance_gap','cash_gap','lease_asset_gap','lease_liability_gap','cash_floor_shortfall')],
    }
    # Display financing balances explicitly rather than hiding them in totals.
    for row in rows:
        row['borrowings_net']=opening['borrowings_net']
        row['operating_lease_liability']=opening['operating_leases']
    groups['Balance sheet'].insert(-2,('Borrowings net','borrowings_net'))
    groups['Balance sheet'].insert(-2,('Operating lease liabilities','operating_lease_liability'))
    for title,fields in groups.items():
        out += ['## '+title,'','| Item | '+' | '.join(str(r['year']) for r in rows)+' |', '|---|'+'---:|'*len(rows)]
        for label,key in fields:
            out.append('| '+label+' | '+' | '.join(f"{r[key]:,.2f}" for r in rows)+' |')
        out.append('')
    return '\n'.join(out)+'\n'


# DCF inputs: provisional, with definitions and source limitations in output.
VALUATION = dict(risk_free=.0413, beta=.975320, erp=.0377,
                 price=914.80, outstanding_shares=443.179176,
                 diluted_shares_proxy=444.803, debt_fair_value_proxy=5370.,
                 borrowing_cost_proxy=.045, finance_lease_rate=.0463,
                 tax_shield_proxy=.261, operating_cash_ratio=.02,
                 terminal_growth=.03, terminal_roic=.20)


def calculate_wacc():
    v=VALUATION
    equity=v['price']*v['outstanding_shares']
    lease=LEASE_BASE['liability']
    cost_equity=v['risk_free']+v['beta']*v['erp']
    total=equity+v['debt_fair_value_proxy']+lease
    return (equity*cost_equity+(v['debt_fair_value_proxy']*v['borrowing_cost_proxy']+lease*v['finance_lease_rate'])*(1-v['tax_shield_proxy']))/total


def fiscal_year_end(year):
    from datetime import date, timedelta
    anchor=date(year,8,31)
    return min((anchor+timedelta(days=d) for d in range(-3,4)),
               key=lambda day: abs((day-anchor).days) if day.weekday()==6 else 999)


def dcf(wacc=None, growth=.03, terminal_roic=.20,
        lease_interest_in_costs=0.0, valuation_date=None,
        sales_growth=None, assumption_overrides=None, terminal_method="roic"):
    from datetime import date
    from math import isfinite
    wacc=calculate_wacc() if wacc is None else wacc
    valuation_date=date(2025,10,8) if valuation_date is None else valuation_date
    if not all(isfinite(x) for x in (wacc,growth,terminal_roic)):
        raise ValueError('DCF rates must be finite.')
    if wacc <= growth or growth < 0 or terminal_roic <= growth or terminal_roic <= 0:
        raise ValueError('Require WACC > growth >= 0 and terminal ROIC > growth.')
    base_date=date(2025,8,31)
    first_end=fiscal_year_end(2026)
    if not base_date <= valuation_date < first_end:
        raise ValueError('This stub implementation supports dates from FY2025 close to before FY2026 close only.')
    elapsed=(valuation_date-base_date).days/(first_end-base_date).days
    if terminal_method not in ('roic','continuity'):
        raise ValueError('Unknown terminal method.')
    assumptions=dict(MODEL_ASSUMPTIONS)
    assumptions.update({} if assumption_overrides is None else assumption_overrides)
    rows=project(lease_interest_in_costs=lease_interest_in_costs,
                 sales_growth=sales_growth,assumption_overrides=assumption_overrides)
    prior=dict(MODEL_BASE)
    pv_flows=0.0
    details=[]
    for row in rows:
        operating_cash_increase=(row['sales']-prior['sales'])*VALUATION['operating_cash_ratio']
        nopat=row['ebit']*(1-assumptions['tax'])
        fcff=nopat+row['da']-row['capex']-row['lease_additions_noncash']-row['delta_wc']-operating_cash_increase
        remaining=1-elapsed if row['year']==2026 else 1.0
        years=(fiscal_year_end(row['year'])-valuation_date).days/365.0
        pv=fcff*remaining/(1+wacc)**years
        pv_flows+=pv
        details.append(dict(year=row['year'],nopat=nopat,da=row['da'],cash_capex=row['capex'],
                            lease_additions=row['lease_additions_noncash'],delta_wc=row['delta_wc'],
                            operating_cash_increase=operating_cash_increase,
                            full_year_fcff=fcff,included_fcff=fcff*remaining,
                            discount_years=years,present_value=pv))
        prior=row
    reinvestment_share=1-details[-1]['full_year_fcff']/details[-1]['nopat'] if details[-1]['nopat']>0 else float('nan')
    effective_terminal_roic=terminal_roic
    if terminal_method=='continuity':
        if not isfinite(reinvestment_share) or not 0<reinvestment_share<1:
            raise ValueError('Continuity requires positive NOPAT and reinvestment share between zero and one.')
        terminal_fcff=details[-1]['full_year_fcff']*(1+growth)
        effective_terminal_roic=growth/reinvestment_share
    else:
        terminal_fcff=details[-1]['nopat']*(1+growth)*(1-growth/terminal_roic)
    if details[-1]['full_year_fcff']<=0 or terminal_fcff<=0:
        raise ValueError('Positive final-year and terminal FCFF required for this going-concern convention.')
    terminal_value=terminal_fcff/(wacc-growth)
    pv_terminal=terminal_value/(1+wacc)**details[-1]['discount_years']
    enterprise=pv_flows+pv_terminal
    # Linear stub estimates, not observed October 8 balances. Uniform cash flow is
    # a simplifying assumption; seasonal daily activity is not reconstructed.
    cash=MODEL_BASE['cash']+elapsed*(rows[0]['cash']-MODEL_BASE['cash'])
    sales_run_rate=MODEL_BASE['sales']+elapsed*(rows[0]['sales']-MODEL_BASE['sales'])
    required_cash=VALUATION['operating_cash_ratio']*sales_run_rate
    excess_cash=cash-required_cash
    if excess_cash < 0:
        raise ValueError('Cash reserve exceeds estimated cash; review financing needs before valuation.')
    lease_debt=LEASE_BASE['liability']+elapsed*(rows[0]['finance_lease_liability']-LEASE_BASE['liability'])
    equity=enterprise+excess_cash+MODEL_BASE['investments']-VALUATION['debt_fair_value_proxy']-lease_debt
    if VALUATION['diluted_shares_proxy']<=0:
        raise ValueError('Positive diluted shares required.')
    return dict(wacc=wacc,growth=growth,terminal_roic=effective_terminal_roic,
                terminal_method=terminal_method,final_reinvestment_share=reinvestment_share,
                lease_interest_in_costs=lease_interest_in_costs,elapsed_fraction=elapsed,
                explicit_cashflows=details,pv_explicit=pv_flows,terminal_fcff=terminal_fcff,
                terminal_fcff_step=terminal_fcff/details[-1]['full_year_fcff']-1,
                pv_terminal=pv_terminal,terminal_share=pv_terminal/enterprise,
                enterprise_value=enterprise,estimated_cash=cash,required_cash=required_cash,
                excess_cash=excess_cash,investments=MODEL_BASE['investments'],
                borrowing_value_proxy=VALUATION['debt_fair_value_proxy'],
                estimated_finance_lease_debt=lease_debt,equity_value=equity,
                shares=VALUATION['diluted_shares_proxy'],per_share=equity/VALUATION['diluted_shares_proxy'])


def dcf_report():
    low,high=dcf(),dcf(lease_interest_in_costs=63.)
    w=low['wacc']
    out=['# Costco provisional DCF — October 8, 2025','',
         'Calculated October 19, 2026. USD millions except per-share values. This is a conditional model result, not a final recommendation.', '',
         '## Inputs and qualifications','',
         '- WACC uses 4.13% risk-free rate, raw monthly beta 0.975320 and provisional ERP 3.77%; ERP pre-cutoff publication remains unconfirmed.',
         '- Financing weights: $914.80 close × 443.179176 million outstanding shares; debt fair-value proxy 5,370 and finance-lease liability 1,479, both from August 31. Borrowing cost: AA index proxy 4.50% (October 7), lease rate proxy 4.63%, tax shield proxy 26.1%. Proxy suitability and deductibility remain open.',
         '- DCF denominator: historical weighted-average diluted shares 444.803 million, not a fully reconciled valuation-date diluted count.',
         '- 38 days of FY2026 precede the valuation date. Assume uniform annual FCFF: exclude 38/364 of FY2026 and discount the remaining flow to its fiscal year end, August 30, 2026. Later fiscal dates use the Sunday nearest August 31; actual/365 discounting.',
         '- Cash, required operating cash and finance-lease debt at October 8 are linear estimates from opening and FY2026 forecast amounts; investments and borrowing fair value are stale-date proxies. No actual October 8 balances are asserted.',
         '- Required cash is 2% of sales; only excess cash enters the bridge. Future accumulated cash is not added again.',
         '- FCFF deducts new finance-lease assets as reinvestment. Finance-lease principal is excluded from FCFF; lease obligations are subtracted once in the equity bridge. Operating leases retain operating treatment.',
         '- Finance-lease interest embedded in merchandise costs is unquantified. Compare historical allocation endpoints 0 and 63 (the full disclosed finance-lease interest expense), each scaled with sales and removed from operating costs. This brackets only allocation uncertainty, not overall business risk.',
         '- Terminal growth 3% and incremental ROIC 20% are analyst assumptions. Terminal reinvestment g/ROIC includes total operating reinvestment, including lease investment and operating cash, rather than adding further terminal deductions.',
         '- Year-end discounting plus uniform first-year cash-flow proration is an approximation. Original historical reconciliation and forecast expense/D&A classifications still need review.', '',
         '## Conditional allocation endpoints','',
         '| Metric | No interest embedded | All 63 embedded |','|---|---:|---:|']
    for label,key in [('WACC (%)','wacc'),('PV explicit FCFF','pv_explicit'),('PV terminal value','pv_terminal'),('Enterprise value','enterprise_value'),('Estimated October 8 cash','estimated_cash'),('Required cash reserve','required_cash'),('Excess cash added','excess_cash'),('Investments added','investments'),('Borrowing value subtracted','borrowing_value_proxy'),('Estimated finance leases subtracted','estimated_finance_lease_debt'),('Equity value','equity_value'),('Diluted share proxy','shares'),('Value per share','per_share'),('Terminal share of EV (%)','terminal_share'),('Terminal FCFF step vs FY2030 (%)','terminal_fcff_step')]:
        factor=100 if key in ('wacc','terminal_share','terminal_fcff_step') else 1
        out.append(f'| {label} | {low[key]*factor:,.4f} | {high[key]*factor:,.4f} |')
    out+=['','## FCFF trace — zero embedded-interest endpoint','',
          '| Fiscal year | NOPAT | D&A | Cash capex | Lease investment | Change WC | Operating cash investment | Full-year FCFF | Included FCFF | Discount years | PV |',
          '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    keys=('nopat','da','cash_capex','lease_additions','delta_wc','operating_cash_increase','full_year_fcff','included_fcff','discount_years','present_value')
    for r in low['explicit_cashflows']:
        out.append('| '+str(r['year'])+' | '+' | '.join(f'{r[k]:,.4f}' for k in keys)+' |')
    out+=['','## WACC–growth sensitivity — zero embedded-interest endpoint','',
          '| WACC | g=2% | g=3% | g=4% |','|---|---:|---:|---:|']
    for rate in (w-.01,w,w+.01):
        out.append(f'| {rate:.4%} | '+' | '.join(f"${dcf(wacc=rate,growth=g)['per_share']:,.2f}" for g in (.02,.03,.04))+' |')
    out+=['','Sources:',
          '- Filing: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm (cover, pp. 37, 39, 41, 52–54).',
          '- Treasury: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2025',
          '- Borrowing proxy: https://fred.stlouisfed.org/data/BAMLC0A2CAAEY',
          '- Price: https://www.financecharts.com/compare/VOO%2CCOST/summary/price',
          '- ERP snapshot: https://psc.ky.gov/pscecf/2025-00257/mkurtz%40bkllawfirm.com/12082025035042/KPCO_1-2_-_Damodaran_On-line_Home_Page_Oct_31_2025.pdf',
          '- Beta data, method and retrieval record: costco_beta_results.md and costco_beta_sources.json.', '']
    return '\n'.join(out)+'\n'


# Causal operating scenarios: proposed analyst stress assumptions, not guidance.
SCENARIOS = {
    'downside': dict(sales_growth=(.05,.04,.03,.03,.03),
                     assumption_overrides=dict(fee_growth=(.07,.06,.05,.04,.03),
                       gross_margin=MODEL_ASSUMPTIONS['gross_margin']-.0025,
                       sga_ratio=MODEL_ASSUMPTIONS['sga_ratio']+.001)),
    'base': dict(sales_growth=PROPOSED_SALES_GROWTH,
                 assumption_overrides=dict(fee_growth=MODEL_ASSUMPTIONS['fee_growth'],
                   gross_margin=MODEL_ASSUMPTIONS['gross_margin'],
                   sga_ratio=MODEL_ASSUMPTIONS['sga_ratio'])),
    'upside': dict(sales_growth=(.09,.08,.07,.06,.06),
                   assumption_overrides=dict(fee_growth=(.10,.09,.08,.07,.06),
                     gross_margin=MODEL_ASSUMPTIONS['gross_margin']+.0015,
                     sga_ratio=MODEL_ASSUMPTIONS['sga_ratio']-.001)),
}


def run_scenarios():
    from copy import deepcopy
    records={}
    for name,config in SCENARIOS.items():
        config=deepcopy(config)
        records[name]=dict(inputs=config,allocation_endpoints={})
        for allocation in (0.,63.):
            rows=project(lease_interest_in_costs=allocation,**config)
            result=dcf(lease_interest_in_costs=allocation,
                       terminal_method='continuity',**config)
            records[name]['allocation_endpoints'][str(int(allocation))]=dict(
                statements=rows,valuation=result,
                checks=dict(max_balance_gap=max(abs(r['balance_gap']) for r in rows),
                            max_cash_gap=max(abs(r['cash_gap']) for r in rows),
                            max_lease_gap=max(max(abs(r['lease_asset_gap']),abs(r['lease_liability_gap'])) for r in rows),
                            max_cash_shortfall=max(r['cash_floor_shortfall'] for r in rows)))
    return records


def scenarios_report():
    records=run_scenarios()
    out=['# Costco operating scenarios — provisional continuity DCF','',
         'Calculated October 19, 2026; valuation date October 8, 2025. USD millions except per-share amounts.',
         'These are analyst scenarios, not forecasts with assigned probabilities or a final valuation recommendation.', '',
         '## Common assumptions','',
         f"- WACC {calculate_wacc():.4%}, terminal growth 3%, capex 2% of net sales, tax 26.1%, required cash 2% of sales.",
         '- Continuity terminal convention: terminal FCFF = final-year FCFF × 1.03. Each case retains its own final-year reinvestment share; implied terminal ROIC is derived, not measured Costco ROIC.',
         '- All prior DCF source/definition limits still apply: ERP publication, corporate yield proxy, financing weights, valuation-date diluted shares, expense/D&A allocation, and interpolated balance-sheet amounts.',
         '- Values span only the 0–63 historical finance-lease-interest allocation endpoints; there is no averaging or probability weighting.',
         '- Uniform first-year FCFF proration excludes 38/364 of FY2026; cash and lease liabilities are estimated at October 8 separately in each run.',
         '- Operating assumptions are simultaneous causal scenarios; these runs do not replace a human AI-off prediction, locked changed-input test, or fresh-environment cold run.', '',
         '## Scenario inputs','',
         '| Case | Sales growth FY2026–30 | Fee growth FY2026–30 | Gross margin | SG&A / net sales |',
         '|---|---|---|---:|---:|']
    for name,record in records.items():
        c=record['inputs'];a=c['assumption_overrides']
        out.append('| '+name+' | '+', '.join(f'{g:.0%}' for g in c['sales_growth'])+' | '+', '.join(f'{g:.0%}' for g in a['fee_growth'])+f" | {a['gross_margin']:.4%} | {a['sga_ratio']:.4%} |")
    out+=['','## Scenario outputs','',
          '| Case | Value/share: allocation 0–63 | FY2030 EBIT (allocation 0) | FY2030 FCFF (allocation 0) | Terminal share of EV | Implied terminal ROIC | Statement checks | Cash floor |',
          '|---|---:|---:|---:|---:|---:|---|---|']
    for name,record in records.items():
        lo=record['allocation_endpoints']['0'];hi=record['allocation_endpoints']['63']
        v=lo['valuation'];last=lo['statements'][-1]
        accounting=all(max(e['checks'][k] for k in ('max_balance_gap','max_cash_gap','max_lease_gap'))<1e-7 for e in record['allocation_endpoints'].values())
        funded=all(e['checks']['max_cash_shortfall']<1e-7 for e in record['allocation_endpoints'].values())
        out.append(f"| {name} | ${v['per_share']:,.2f}–${hi['valuation']['per_share']:,.2f} | {last['ebit']:,.2f} | {v['explicit_cashflows'][-1]['full_year_fcff']:,.2f} | {v['terminal_share']:.2%} | {v['terminal_roic']:.2%} | {'PASS' if accounting else 'FAIL'} | {'PASS' if funded else 'FAIL'} |")
    out+=['','## WACC–growth grid — base case, zero embedded-interest allocation','',
          '| WACC | g=2% | g=3% | g=4% |','|---|---:|---:|---:|']
    w=calculate_wacc()
    for rate in (w-.01,w,w+.01):
        out.append(f'| {rate:.4%} | '+' | '.join(f"${dcf(wacc=rate,growth=g,terminal_method='continuity',**SCENARIOS['base'])['per_share']:,.2f}" for g in (.02,.03,.04))+' |')
    out+=['','## Interpretation and outstanding work','',
          '- These results replace neither peer valuation nor reverse DCF. Test separate capital-spending/working-capital stresses before finalizing the recommendation.',
          '- Continuity avoids the original terminal reinvestment cliff but does not prove the retained reinvestment share is sustainable. A five-year fade or measured long-term return assumption could produce different results.',
          '- Original --dcf output retains the 20% ROIC convention explicitly as an alternative; --scenarios uses continuity. Label both outputs to prevent mixing conventions.',
          '- Full scenario inputs, statement traces, bridges and check gaps are in costco_project1_scenario_runs.json.',
          '- Sources and other limitations are documented in costco_project1_provisional_dcf.md and costco_beta_results.md.', '']
    return '\n'.join(out)+'\n'


def reverse_margin(target=None, lease_interest_in_costs=0.0, tolerance=.000001):
    from math import isfinite
    target=VALUATION['price'] if target is None else target
    if not isfinite(target) or target<=0 or not isfinite(tolerance) or tolerance<=0:
        raise ValueError('Positive finite target and tolerance required.')
    def value(margin):
        overrides=dict(SCENARIOS['base']['assumption_overrides'])
        overrides['gross_margin']=margin
        return dcf(assumption_overrides=overrides,
                   terminal_method='continuity',lease_interest_in_costs=lease_interest_in_costs)
    lower=MODEL_ASSUMPTIONS['gross_margin'];upper=.20
    low_value=value(lower)['per_share'];high_value=value(upper)['per_share']
    # Check the actual implemented path before using bisection; no global
    # monotonicity assumption is made for arbitrary sales-growth changes.
    previous=low_value
    for i in range(1,21):
        current=value(lower+(upper-lower)*i/20)['per_share']
        if current<=previous:
            raise ValueError('Margin bracket is not strictly increasing on the tested grid.')
        previous=current
    info=dict(target=target,lower_margin=lower,upper_margin=upper,
              lower_price=low_value,upper_price=high_value,
              lease_interest_in_costs=lease_interest_in_costs)
    if not low_value<=target<=high_value:
        return dict(info,status='unbracketed',solution=None)
    for iteration in range(1,101):
        mid=(lower+upper)/2;result=value(mid)
        error=result['per_share']-target
        if abs(error)<=tolerance:
            return dict(info,status='solved',solution=mid,
                        margin_change_percentage_points=(mid-MODEL_ASSUMPTIONS['gross_margin'])*100,
                        matched_price=result['per_share'],price_error=error,
                        iterations=iteration,valuation=result)
        if error<0:lower=mid
        else:upper=mid
    raise ValueError('Margin reverse DCF failed to converge.')


def reverse_report():
    results=[reverse_margin(lease_interest_in_costs=a) for a in (0.,63.)]
    sales_scan=[]
    for i in range(11):
        shift=i*.01
        growth=tuple(g+shift for g in PROPOSED_SALES_GROWTH)
        result=dcf(sales_growth=growth,terminal_method='continuity')
        sales_scan.append((shift,result['per_share']))
    out=['# Costco reverse DCF — conditional market-implied margin','',
         'Calculated October 19, 2026; valuation date October 8, 2025. USD/share unless noted.', '',
         '## Sales-only diagnostic','',
         '- Held fee growth, merchandise margin, SG&A intensity, capital-spending intensity, WACC and terminal convention fixed; shifted all five sales growth rates by the same amount.',
         f"- Base sales schedule gives ${sales_scan[0][1]:,.2f}; +10 percentage points in each year gives ${sales_scan[-1][1]:,.2f}.",
         '- Target $914.80 is not bracketed on the tested +0 to +10 percentage-point grid. No sales-growth solution is asserted. Wider extrapolation is not assumed monotonic: reinvestment can offset sales growth.', '',
         '## Reverse-margin method','',
         '- Solve for a single merchandise gross margin applied in FY2026–2030. Keep base sales growth 8%, 7%, 6%, 5%, 5%; fee growth 9%, 8%, 7%, 6%, 5%; SG&A ratio 9.2497%; cash capex 2%; tax 26.1%; cash reserve 2%; and other model assumptions fixed.',
         f"- WACC {calculate_wacc():.4%}; terminal growth 3%; continuity terminal FCFF. The final reinvestment share and implied ROIC recalculate as linked outputs, not fixed independent inputs.",
         '- Search bracket: base gross margin to 20%. Check a 21-point price grid for increasing values, then bisect to a $0.000001/share price tolerance; reject unbracketed targets rather than clipping.',
         '- Compare both expense-allocation endpoints. The market price is matched mathematically; no operating plausibility is implied.', '',
         '| Historical lease-interest allocation | Solved gross margin | Increase vs base (percentage points) | Matched price |',
         '|---|---:|---:|---:|']
    for r in results:
        if r['status']=='solved':
            out.append(f"| {r['lease_interest_in_costs']:.0f} million | {r['solution']:.4%} | {r['margin_change_percentage_points']:.4f} | ${r['matched_price']:.6f} |")
        else:
            out.append(f"| {r['lease_interest_in_costs']:.0f} million | No bracketed solution | — | — |")
    out+=['','## Interpretation','',
          '- These margins ask what would be required if margin alone explained the price gap. Investors could instead assume different growth, membership economics, reinvestment, discount rates, or a combination.',
          '- A substantially higher margin could conflict with the low-price business model, change customer demand, or require different SG&A. Those feedback effects are excluded in this one-input diagnostic.',
          '- This is not evidence that investors actually expect the solved margin, and it is not proof of mispricing.',
          '- All source, proxy, share-count, stub-timing and terminal limitations in costco_project1_provisional_dcf.md and costco_project1_scenarios.md remain.',
          '- This AI-assisted analysis is not the human-authored AI-off locked changed-input test.', '']
    return '\n'.join(out)+'\n'


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Provisional Costco forecast and DCF')
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--dcf',action='store_true',help='Print alternative 20% terminal-ROIC DCF')
    group.add_argument('--scenarios',action='store_true',help='Print continuity operating scenarios')
    group.add_argument('--reverse',action='store_true',help='Print reverse-margin DCF and sales-only diagnostic')
    args=parser.parse_args()
    output=reverse_report() if args.reverse else scenarios_report() if args.scenarios else dcf_report() if args.dcf else report()
    print(output,end='')
