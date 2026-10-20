"""Isolated first-year capex sensitivity; base file and locked records are unchanged."""
from pathlib import Path
import hashlib, importlib.util, inspect, json
ROOT=Path(__file__).resolve().parent
source=ROOT/'COST_project1_revised.py'
before=hashlib.sha256(source.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('capex_test_model',source)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base=[m.dcf(terminal_method='continuity',lease_interest_in_costs=x) for x in (0.,63.)]
# Replace only the capex expression in an in-memory copy of project().
# All downstream statement and valuation calculations remain those of the model.
old="row['capex'] = a['capex_ratio']*row['sales']"
new="row['capex'] = FY2026_CAPEX_TEST if row['year']==2026 else a['capex_ratio']*row['sales']"
function=inspect.getsource(m.project)
assert function.count(old)==1
exec(compile(function.replace(old,new),'<isolated FY2026 capex sensitivity>','exec'),m.__dict__)
records=[]
for spending in (6000.,6250.,6500.):
 m.FY2026_CAPEX_TEST=spending
 runs=[m.dcf(terminal_method='continuity',lease_interest_in_costs=x) for x in (0.,63.)]
 rows=m.project()
 for b,r in zip(base,runs):
  assert abs(r['explicit_cashflows'][0]['full_year_fcff']-b['explicit_cashflows'][0]['full_year_fcff']+spending-b['explicit_cashflows'][0]['cash_capex'])<1e-7
  assert r['terminal_fcff']==b['terminal_fcff']
  assert r['per_share']<b['per_share']
 records.append(dict(fy2026_capex=spending,runs=runs))
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
payload=dict(model_sha256=before,base=base,tests=records,source_unchanged=True,
 convention='FY2026 only; FY2027–30 capex stays 2% of sales; all other independent assumptions held fixed. D&A remains the model proxy; no incremental growth or depreciation benefit assumed.')
(ROOT/'costco_fy2026_capex_test_results.json').write_text(json.dumps(payload,indent=2))
lines=['# FY2026 capex-guidance sensitivity','',payload['convention'],'',
 '| FY2026 cash capex ($M) | Value/share, allocation 0–63 |', '|---|---:|',
 f"| Base {base[0]['explicit_cashflows'][0]['cash_capex']:,.2f} | ${base[0]['per_share']:.2f}–${base[1]['per_share']:.2f} |"]
for rec in records:
 r=rec['runs'];lines.append(f"| {rec['fy2026_capex']:,.0f} | ${r[0]['per_share']:.2f}–${r[1]['per_share']:.2f} |")
lines+=['','WACC '+format(base[0]['wacc'],'.4%')+'; terminal growth 3%; continuity terminal convention.',
 'All model statement checks ran without exception. First-year FCFF falls dollar for dollar with extra capex. Terminal FCFF is unchanged because this test changes only FY2026 spending. Valuation-date excess cash follows the existing interpolation convention.',
 'This is a sensitivity, not a revised saved base case. A permanent capex increase has a much larger terminal effect; the earlier locked 2.5% test is separate historical evidence.',
 'Management guidance source: Costco FY2025 Form 10-K, MD&A p. 29: https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm',
 'Base source SHA-256 unchanged: '+before]
report='\n'.join(lines)+'\n'
(ROOT/'costco_fy2026_capex_test.md').write_text(report)
print(report)
