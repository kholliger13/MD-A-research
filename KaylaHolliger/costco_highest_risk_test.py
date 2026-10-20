"""Highest-risk failure checks. Run offline using standard-library Python.
Writes visible results next to this script; never changes model inputs on disk.
Not the required recorded fresh-environment cold run.
"""
from pathlib import Path
import runpy, math, json, hashlib, datetime


def main():
    p=Path(__file__).resolve().parent
    f=p/'COST_project1_revised.py'
    before=hashlib.sha256(f.read_bytes()).hexdigest()
    m=runpy.run_path(str(f),run_name='risk_model')
    checks=[]
    def expect_refusal(name, kwargs):
        try:
            m['dcf'](**kwargs)
        except ValueError as error:
            checks.append(dict(test=name,status='PASS',behavior=str(error)))
        else:
            raise AssertionError(f'{name}: invalid valuation returned instead of refusing')
    w=m['calculate_wacc']()
    expect_refusal('Terminal growth equals WACC',dict(wacc=w,growth=w))
    expect_refusal('Terminal growth exceeds WACC',dict(wacc=w,growth=w+.01))
    expect_refusal('Terminal ROIC cannot fund assumed growth',dict(terminal_roic=.02,growth=.03))
    expect_refusal('Nonfinite WACC',dict(wacc=math.nan))
    rows=m['project'](assumption_overrides={'gross_margin':.06})
    if len(rows)!=5:
        raise AssertionError('Loss stress did not produce all five years')
    max_gap=max(max(abs(r[k]) for k in ('balance_gap','cash_gap','lease_asset_gap','lease_liability_gap')) for r in rows)
    if max_gap>1e-7:
        raise AssertionError('Loss-stress statements fail accounting reconciliation')
    if not all(r['dividends']==0 and r['tax']==0 for r in rows if r['net_income']<0):
        raise AssertionError('Losses produce unsupported dividends or immediate tax credits')
    shortfall=max(r['cash_floor_shortfall'] for r in rows)
    if shortfall<=0 or min(r['cash'] for r in rows)>=0:
        raise AssertionError('Deliberate funding stress did not expose deficit')
    checks.append(dict(test='6% merchandise-margin loss stress',status='PASS',
                       behavior='All five statement years retained; accounting reconciles; no dividends or immediate tax credits in loss years; cash shortfalls exposed.',
                       max_gap=max_gap,max_cash_shortfall=shortfall,minimum_cash=min(r['cash'] for r in rows)))
    expect_refusal('No unsupported going-concern value for loss stress',dict(terminal_method='continuity',assumption_overrides={'gross_margin':.06}))
    # Deliberately corrupt opening equity in memory; validation must catch it.
    equity=m['MODEL_BASE']['equity']
    try:
        m['MODEL_BASE']['equity']=equity+1
        try:m['project']()
        except ValueError as error:checks.append(dict(test='Opening-equity mismatch of 1 million',status='PASS',behavior=str(error)))
        else:raise AssertionError('Corrupted equity was silently accepted')
    finally:
        m['MODEL_BASE']['equity']=equity
    if hashlib.sha256(f.read_bytes()).hexdigest()!=before:
        raise AssertionError('Source changed during tests')
    if m['project']()!=runpy.run_path(str(f),run_name='fresh_restore')['project']():
        raise AssertionError('Restored base differs from independent reload')
    checks.append(dict(test='Restore original base and source integrity',status='PASS',behavior='Source hash unchanged; restored forecast equals fresh module reload.'))
    record=dict(run_time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),model_sha256=before,checks=checks)
    (p/'costco_highest_risk_failure_results.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    out=['# Highest-risk failure test — Costco','',
         'Risk: an arithmetically linked model could still report misleading value from an invalid terminal denominator or an unfunded, loss-making business.',
         'Command: python3 -B costco_highest_risk_test.py',
         f"Run UTC: {record['run_time_utc']}",f'Model SHA256: {before}', '',
         '| Test | Result | Observed behavior |','|---|---|---|']
    for c in checks:out.append(f"| {c['test']} | {c['status']} | {c['behavior']} |")
    out+=['',f'Loss-stress minimum forecast cash: {min(r["cash"] for r in rows):,.2f} USD million.',
          f'Largest required-cash shortfall: {shortfall:,.2f} USD million.',
          'Negative cash is an unfunded financing need, not an executable cash balance. No borrowing plug or positive valuation is inserted.',
          'The 6% margin is a deliberate failure probe, not a calibrated downside case or company forecast.', '',
          '## Model correction recorded','',
          '- DCF NOPAT now taxes only positive EBIT, matching the existing no-immediate-loss-tax-benefit policy. Current positive-profit base/scenario outputs are unchanged. Locked capex-test model and records were not modified.', '',
          '## Limits','',
          '- Passing these tests validates specific failure behavior, not forecasts, source completeness or overall valuation accuracy.',
          '- This AI-assisted failure test is distinct from the student’s locked capex prediction and the still-required recorded clean run in a fresh environment.', '']
    text='\n'.join(out)+'\n'
    (p/'costco_highest_risk_failure_test.md').write_text(text)
    print(text,end='')


if __name__=='__main__':
    main()
