# Lab 06 known-answer reconciliation

Run date: October 19, 2026. Expected answers: Session 6 instructions supplied by the student in chat.
Source link: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-06-sensitivity-and-reverse-dcf.md
Script: dcf_kaylaholliger_9_10_26.py; command: python3 -B dcf_kaylaholliger_9_10_26.py.
The terminal prints the unchanged Costco block first, then separately labeled instructor training and Costco sensitivity/reverse-DCF blocks. Compare ONLY the instructor training results to this key.

## Training fixture

Starting FCFF 100; five annual growth rates 8%, 6%, 5%, 4%, 3%; WACC 10%; terminal growth 3%; cash 50; debt 300; diluted shares 50. Matching million units; annual year-end discounting.

| WACC | Terminal growth | Expected $/share | Actual $/share | Rounded match |
|---|---|---:|---:|---|
| 9% | 2% | 28.60 | 28.59885058 | PASS |
| 9% | 3% | 32.94 | 32.94259434 | PASS |
| 9% | 4% | 39.02 | 39.02383559 | PASS |
| 10% | 2% | 24.36 | 24.35642265 | PASS |
| 10% | 3% | 27.50 | 27.49737040 | PASS |
| 10% | 4% | 31.69 | 31.68530073 | PASS |
| 11% | 2% | 21.06 | 21.05792542 | PASS |
| 11% | 3% | 23.41 | 23.41403273 | PASS |
| 11% | 4% | 26.44 | 26.44331357 | PASS |

Reverse DCF: target $30.00; expected uniform shift about +1.78 percentage points; actual +1.77794755 points; matched price $29.99999979. PASS.
Bisection bounds −5 to +10 percentage points. Every other training input held fixed.

## Scope and limitations

- All nine grid cells match the supplied expected answers when rounded to cents. The base is $27.49737040, which rounds to $27.50. Reverse result agrees with the approximate published +1.78 points.
- This validates the earlier training DCF engine against the supplied instructional key. It does not independently validate Costco forecasts or the revised lease/stub/continuity implementation.
- The Session 6 excerpt supplies the grid and reverse answer, but not the full earlier twelve-number key. No claim is made that all twelve original outputs were reconciled to an unseen key.
- No original source inputs or code changed. Full original command output is preserved in lab06_known_answer_terminal_output.txt.
- Source script SHA256 before and after: 6df4c5165286bfbd93a7d330d41977076303c3511b08d1e1a4b9edca61563f63.
- This is an AI-assisted known-answer reconciliation, not a substitute for the human-authored locked capex test or fresh-environment cold run.

