"""One-at-a-time sensitivity for the existing Costco linked model."""
from pathlib import Path
from copy import deepcopy
import json
import math
import COST_proforma_from_ABG as model

ROOT = Path(__file__).resolve().parent
PREFIX = 'costco_operating_sensitivity_2026_09_29'
BASE_FILE = ROOT / 'costco_base_rerun_2026_09_29_inputs.json'


def run_case(base, driver, level, shift):
    a = deepcopy(base['ASSUMPTIONS'])
    opening = deepcopy(base['OPENING'])
    if driver == 'fee_growth':
        a[driver] = [x + shift for x in a[driver]]
    elif driver == 'gross_margin':
        a[driver] += shift
    changed = [k for k in a if a[k] != base['ASSUMPTIONS'][k]]
    assert changed == ([] if shift == 0 else [driver])
    result = dict(driver=driver, level=level, assumptions=deepcopy(a), opening=opening,
                  changed_inputs=changed, forecast=[], valid=False, errors=[],
                  operating_profit=None, fcff=None, value_per_share=None)
    old_opening = model.OPENING
    model.OPENING = deepcopy(opening)
    try:
        model.check_opening()
        rows = model.project(a)
        result['forecast'] = rows
        result['operating_profit'] = rows[-1]['ebit']
        result['fcff'] = rows[-1]['fcff']
        model.assert_balanced(rows)
        if not all(math.isfinite(v) for row in rows for v in row.values()):
            raise ValueError('Nonfinite forecast output')
        result['valid'] = True
        try:
            v = model.value(rows, a['wacc'], a['terminal_growth'], a['terminal_roic'], a)
            if v is None:
                result['valuation_limitation'] = 'Existing valuation unavailable: nonpositive final-year or terminal FCFF; no terminal value assigned.'
            elif not all(math.isfinite(x) for x in v.values()):
                result['valuation_limitation'] = 'Existing valuation unavailable: nonfinite valuation output.'
            else:
                result['valuation'] = v
                result['value_per_share'] = v['per_share']
        except (ValueError, ArithmeticError) as exc:
            result['valuation_limitation'] = f'Existing valuation unavailable: {exc}'
    except (ValueError, ArithmeticError) as exc:
        result['errors'].append(str(exc))
        result['valuation_limitation'] = 'Unavailable: invalid model run.'
    finally:
        model.OPENING = old_opening
    return result


def fmt(x, signed=False):
    if x is None:
        return 'Unavailable'
    return format(x, '+,.2f' if signed else ',.2f')


def main():
    base = json.loads(BASE_FILE.read_text())
    frozen = deepcopy(base)
    results = []
    for driver, width in [('fee_growth', .02), ('gross_margin', .0025)]:
        for level, shift in [('Lower', -width), ('Base', 0), ('Higher', width)]:
            results.append(run_case(base, driver, level, shift))
    # Final model execution resets every independent input and opening balance to base.
    restored = run_case(base, None, 'Restored base', 0)
    assert base == frozen, 'Saved base inputs were mutated'
    baseline = results[1]
    assert restored['forecast'] == baseline['forecast'] == results[4]['forecast']
    assert restored['value_per_share'] == baseline['value_per_share']
    outputs = ['operating_profit', 'fcff', 'value_per_share']
    spans = {}
    lines = ['# Costco one-at-a-time sensitivity', '',
             'Run: `../.venv/bin/python COST_proforma_from_ABG.py --sensitivity`', '',
             f'Preserved base input set: `{BASE_FILE.name}`. Every run uses a fresh deep copy of all assumptions and opening balances. Lower/base/higher are independently rerun for each driver. Only the named driver changes; linked statement quantities recalculate.', '',
             'Existing ranges: membership growth ±2 percentage points; merchandise margin ±0.25 percentage points. Both apply to FY2026–2030. Input percentages below are displayed to six decimals; JSON retains full precision. No other independent assumptions change.', '',
             'Operating profit = EBIT. FCFF = signed free cash flow to the firm after operating-cash investment. Profit, FCFF and their changes/spans are USD millions; value and its changes/span are USD/share. Changes are scenario minus that driver’s independently rerun base. No positive-only cash-flow subtotal is used.', '']
    for driver in ['fee_growth', 'gross_margin']:
        cases = [r for r in results if r['driver'] == driver]
        ref = cases[1]
        lines += [f'## {driver}', '',
                  'Input units: annual membership-fee revenue growth (%) by FY2026, 2027, 2028, 2029, 2030.' if driver == 'fee_growth' else 'Input units: merchandise gross margin (% of net sales), same value in each FY2026–2030 year.', '',
                  '| Run | Actual input (%) | FY2030 EBIT | Δ EBIT | FY2030 FCFF | Δ FCFF | Value/share | Δ value/share | Checks |',
                  '|---|---|---:|---:|---:|---:|---:|---:|---|']
        for r in cases:
            vals = r['assumptions'][driver]
            actual = ', '.join(f'{v*100:.6f}' for v in vals) if isinstance(vals, list) else f'{vals*100:.6f}'
            cells = []
            r['changes_from_base'] = {}
            for key in outputs:
                delta = r[key]-ref[key] if r['valid'] and ref['valid'] and r[key] is not None and ref[key] is not None else None
                r['changes_from_base'][key] = delta
                cells += [fmt(r[key]), fmt(delta, True)]
            lines.append('| ' + ' | '.join([r['level'], actual] + cells + ['PASS' if r['valid'] else 'INVALID']) + ' |')
            if r.get('valuation_limitation') or r['errors']:
                lines += ['', f"{r['level']}: " + '; '.join(r['errors'] + [r.get('valuation_limitation', '')]), '']
        spans[driver] = {}
        for key in outputs:
            valid = [r[key] for r in cases if r['valid'] and r[key] is not None]
            spans[driver][key] = dict(span=max(valid)-min(valid) if len(valid) >= 2 else None, valid_count=len(valid))
        lines += ['', '| Output | Span (maximum − minimum) | Valid cases |', '|---|---:|---:|']
        for key in outputs:
            s = spans[driver][key]
            lines.append(f"| {key} | {fmt(s['span'])} | {s['valid_count']}/3 |")
        lines += ['']
    lines += ['## Visible accounting checks', '', '| Run | Opening balance | FY2026–2030 balance sheets | Cash reconciliation | Minimum cash |', '|---|---|---|---|---|']
    for r in results + [restored]:
        name = f"{r['driver'] or 'Final'} / {r['level']}"
        status = 'PASS' if r['valid'] else 'INVALID — see detailed errors'
        lines.append('| ' + ' | '.join([name] + [status]*4) + ' |')
    lines += ['', 'Invalid runs are flagged and excluded from spans; no ranking is produced. Valuation availability is evaluated separately with the existing valuation rules. Signed annual cash flows remain in the trace files.', '',
              'Final base rerun: exact forecast and value match both driver base runs. All independent inputs restored to the preserved base.', '',
              f'Full linked statement fields, annual check gaps and valuation components: `{PREFIX}_full_output.md`. Exact inputs and results: `{PREFIX}_runs.json`.']
    details = ['# Full linked-model traces', '', 'All statement amounts and check gaps are USD millions; year is a fiscal-year label. Valuation per_share is USD/share and terminal_share is a fraction; other valuation components are USD millions.', '']
    for r in results + [restored]:
        details += [f"## {r['driver'] or 'Final'} / {r['level']}", '', '### Independent inputs and opening balances', '', '```json', json.dumps({'OPENING': r['opening'], 'ASSUMPTIONS': r['assumptions']}, indent=2), '```', '', '### Linked statements and cash flows', '']
        rows = r['forecast']
        if rows:
            details += ['| Model field | 2026 | 2027 | 2028 | 2029 | 2030 |', '|---|---:|---:|---:|---:|---:|']
            for key in rows[0]:
                if key != 'year':
                    details.append('| ' + key + ' | ' + ' | '.join(f'{row[key]:,.8f}' for row in rows) + ' |')
            details += ['', model.check_block(rows), '']
        details += ['Status: ' + ('PASS' if r['valid'] else 'INVALID'), '', json.dumps(r.get('valuation', {}), indent=2), r.get('valuation_limitation', ''), '; '.join(r['errors']), '']
    (ROOT / f'{PREFIX}.md').write_text('\n'.join(lines) + '\n')
    (ROOT / f'{PREFIX}_full_output.md').write_text('\n'.join(details) + '\n')
    (ROOT / f'{PREFIX}_runs.json').write_text(json.dumps({'base_input_file': BASE_FILE.name, 'base': base, 'runs': results, 'spans': spans, 'restored_base': restored}, indent=2, allow_nan=False) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
