"""Run only AFTER prediction/model/runner are committed. Offline standard library.
This preserves the submitted forecast before generating any changed-input results.
"""
from pathlib import Path
import subprocess, runpy, json, hashlib, datetime


def main():
    p=Path(__file__).resolve().parent
    def git(*args):
        return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
    commit=git('rev-parse','HEAD')
    required=('prediction.md','frozen_costco_model.py','pre_run_manifest.json','run_locked_capex_test.py')
    for name in required:
        committed=subprocess.check_output(['git','-C',str(p),'show',f'HEAD:{name}'])
        if committed!=(p/name).read_bytes():
            raise ValueError(f'Committed input changed: {name}')
    manifest=json.loads((p/'pre_run_manifest.json').read_text())
    for name,key in [('prediction.md','prediction_sha256'),('frozen_costco_model.py','model_sha256')]:
        if hashlib.sha256((p/name).read_bytes()).hexdigest()!=manifest[key]:
            raise ValueError('Pre-run manifest hash mismatch')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    m=runpy.run_path(str(p/'frozen_costco_model.py'),run_name='locked_model')
    from copy import deepcopy
    original=deepcopy(m['MODEL_ASSUMPTIONS'])
    case=deepcopy(m['SCENARIOS']['base'])
    changed=deepcopy(case)
    changed['assumption_overrides']['capex_ratio']=.025
    baseline=dict(case);baseline['assumption_overrides']=dict(case['assumption_overrides'],capex_ratio=.02)
    def run(config):
        statements=m['project'](**config)
        valuation=m['dcf'](terminal_method='continuity',**config)
        return dict(statements=statements,valuation=valuation)
    base=run(baseline);stress=run(changed);restored=run(baseline)
    if original!=m['MODEL_ASSUMPTIONS'] or restored!=base:
        raise ValueError('Base not restored exactly')
    all_keys=set(baseline['assumption_overrides'])|set(changed['assumption_overrides'])
    if [k for k in sorted(all_keys) if baseline['assumption_overrides'].get(k)!=changed['assumption_overrides'].get(k)]!=['capex_ratio'] or baseline['sales_growth']!=changed['sales_growth']:
        raise ValueError('Input isolation failed')
    details=[]
    for b,s,bc,sc in zip(base['statements'],stress['statements'],base['valuation']['explicit_cashflows'],stress['valuation']['explicit_cashflows']):
        expected=.005*b['sales']
        decline=bc['full_year_fcff']-sc['full_year_fcff']
        if abs(decline-expected)>1e-7:
            raise ValueError('FCFF change does not equal isolated incremental capex')
        if abs(bc['nopat']-sc['nopat'])>1e-7 or abs(b['da']-s['da'])>1e-7:
            raise ValueError('Unexpected NOPAT or D&A change')
        details.append(dict(year=b['year'],sales=b['sales'],old_capex=b['capex'],new_capex=s['capex'],
                            base_fcff=bc['full_year_fcff'],changed_fcff=sc['full_year_fcff'],
                            decrease=decline,expected_from_sales=expected))
    vb,vs=base['valuation'],stress['valuation']
    decrease=1-vs['per_share']/vb['per_share']
    terminal_decline=1-vs['pv_terminal']/vb['pv_terminal']
    last_fcff_decline=1-vs['explicit_cashflows'][-1]['full_year_fcff']/vb['explicit_cashflows'][-1]['full_year_fcff']
    if abs(terminal_decline-last_fcff_decline)>1e-12:
        raise ValueError('Continuity terminal directional reconciliation failed')
    max_gap=max(max(abs(r[k]) for k in ('balance_gap','cash_gap','lease_asset_gap','lease_liability_gap')) for run in (base,stress) for r in run['statements'])
    record=dict(run_started_utc=started,pre_run_commit=commit,commit_timestamp=git('show','-s','--format=%cI','HEAD'),
                pre_run_manifest=manifest,base_inputs=baseline,changed_inputs=changed,
                baseline=base,changed=stress,annual_changes=details,
                value_decrease_fraction=decrease,terminal_value_decrease_fraction=terminal_decline,
                final_fcff_decrease_fraction=last_fcff_decline,max_accounting_gap=max_gap,
                restored_base_exact=True,input_isolation_pass=True)
    destination=p/'actual_results.json'
    if destination.exists():
        raise ValueError('Results already exist; preserve the first run.')
    destination.write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    out=['# Locked capex test — actual results and reconciliation','',
         f'Run started UTC: {started}',f'Pre-run commit: {commit}',
         f"Commit timestamp: {record['commit_timestamp']}",
         'The committed prediction is preserved verbatim in prediction.md. AI-off authorship cannot be independently certified by the runner.', '',
         '## Actual results','',
         f"- Value/share: ${vb['per_share']:.2f} → ${vs['per_share']:.2f}; decrease {decrease:.2%}.",
         f'- Terminal PV decrease: {terminal_decline:.2%}; FY2030 FCFF decrease: {last_fcff_decline:.2%}.',
         f'- Maximum accounting-check gap: {max_gap:.12g} USD million. Restored base matches exactly; only independent capex ratio changed.', '',
         '| Year | Base capex | Changed capex | Base FCFF | Changed FCFF | FCFF decrease |',
         '|---|---:|---:|---:|---:|---:|']
    for r in details:
        out.append(f"| {r['year']} | {r['old_capex']:,.2f} | {r['new_capex']:,.2f} | {r['base_fcff']:,.2f} | {r['changed_fcff']:,.2f} | {r['decrease']:,.2f} |")
    out+=['','## Reconcile to the submitted prediction','',
          f"- Value decrease prediction (25–30%): {'within' if .25<=decrease<=.30 else 'outside'} the predicted range; actual {decrease:.2%}.",
          '- Dollar-for-dollar FCFF mechanism confirmed: annual full-year FCFF decline equals 0.5% of forecast sales. NOPAT and assumed D&A unchanged.',
          '- FY2026 prediction approximately 1,458 matches rounding. FY2030 prediction approximately 1,805 differs from the current 5% ending-growth forecast; actual is reported in the table. Do not edit the locked prediction to match.',
          '- This model uses sales-linked D&A. Additional capex raises PP&E but does not itself change forecast depreciation or sales; this is an isolated investment stress, not a complete warehouse expansion plan.',
          '- Model FCFF also includes working-capital funding, noncash lease investment and required operating cash; the student simplified margin arithmetic omits these. FY2026 FCFF is prorated after the valuation date, and the estimated starting excess-cash bridge also changes.',
          '- Continuity retains each run’s final reinvestment share, so terminal PV and FY2030 FCFF fall by the same percentage. The implied terminal ROIC changes as a linked output.',
          '- Decision effect for student review: lower value continues to support watch/defer rather than initiate under the current inputs. A margin of safety was not positive at the market price before this stress.',
          '- This record was made now; it does not recreate an earlier lab prediction or establish the Edition A checkpoint. No fresh-environment cold run or published training-case validation is claimed.', '']
    (p/'reconciliation.md').write_text('\n'.join(out)+'\n')
    print('\n'.join(out))


if __name__=='__main__':
    main()
