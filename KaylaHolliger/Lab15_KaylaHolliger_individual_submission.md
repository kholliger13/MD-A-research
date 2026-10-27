# Lab 15 — Point-in-time data gate

Kayla Holliger — individual submission

Decision date: March 31, 2026. Source: the supplied classroom table and four ordered rules. These are planted training prices, not market data.

## Known-answer verification

My `asof.py` applies the four rules in order and preserves original row numbers. Every row disposition, signal value and signal month matches the supplied known answer.

| Funnel step | Rows excluded | Rows remaining |
|---|---|---:|
| Start | — | 12 |
| 1. Quarantine missing ticker | 11 | 11 |
| 2. Remove exact duplicate | 7 | 10 |
| 3. Remove publication after March 31 | 3, 8, 10 | 7 |
| 4. Replace older publication with latest knowable revision | 2 | 6 |

The as-of panel contains **1, 4, 5, 6, 9, 12**. All 12 original rows are accounted for: six admitted, five removed and one quarantined.

Return = latest knowable month's price / previous calendar month's price − 1.

| Ticker | As-of calculation | March 31 as-of signal | Naive signal |
|---|---|---|---|
| AAA | 103 / 101 − 1 | +1.98% (February) | +5.83% (March) |
| BBB | 97 / 98 − 1 | −1.02% (February) | −5.15% (March) |
| CCC | 111 / 110 − 1 | +0.91% (February) | +1.82% (February, revised) |

AAA correctly uses row 4's revised price of 103.0, published March 25. Keeping row 2's 104.0 would incorrectly produce +2.97%. The future April publications are excluded even when their measured month is February or March.

## Partner date-shift check

I ran my partner's `asof.py` at its original March 31 cutoff and confirmed the same known-answer signals. I temporarily changed its decision date to **April 15, 2026** and reran it.

| Ticker | Partner April 15 as-of | Partner naive | Match |
|---|---:|---:|---|
| AAA | +5.83% | +5.83% | Yes |
| BBB | −5.15% | −5.15% | Yes |
| CCC | +1.82% | +1.82% | Yes |

By April 15, every publication in this fixture is available. The as-of signal therefore becomes the naive signal, ticker for ticker. I restored the partner's file byte for byte to its original March 31 version and reran it; the original output was reproduced.

The difference between the March 31 columns comes from publications not yet available on that date. For AAA and BBB, the naive calculation also advances the signal period from February to March. For CCC, it uses a later revision of February. The gap therefore includes both access to a later measured month and access to a later revision, depending on the ticker.

## V — sanity check after provenance

Yield = 100 / price − 1 for the exercise's one-year zero-coupon funds.

| Row | Fund | Month | Price | Yield | Breaks under the exercise's rules |
|---|---|---|---:|---:|---|
| 1 | AAA | January | 101.0 | −0.99% | Negative yield |
| 4 | AAA | February | 103.0 | −2.91% | Negative yield |
| 5 | BBB | January | 98.0 | +2.04% | Nothing |
| 6 | BBB | February | 97.0 | +3.09% | Nothing |
| 9 | CCC | January | 110.0 | −9.09% | Negative yield; priced above BBB and AAA |
| 12 | CCC | February | 111.0 | −9.91% | Negative yield; priced above BBB and AAA |

All six rows pass provenance, but four fail the exercise's sanity checks. Both months violate the required credit-price ordering AAA > BBB > CCC. On time is not the same as true: the provenance gate establishes availability, while a separate sanity gate checks financial validity.

## Reproduction and evidence

Run from the course folder:

```sh
.venv/bin/python asof.py
.venv/bin/python verify_asof.py
.venv/bin/python verify_partner_asof.py
```

The script also runs with `python3 asof.py`; this shell has no bare `python` command without selecting an environment.

- `asof.py`: individual standalone filter, panel and both signals.
- `asof_known_answer_proof.txt`: explicit comparisons with the supplied answer key and actual program output.
- `partner_asof_date_shift_proof.txt`: both partner runs, equality checks and restoration hash.

Both verification scripts passed again on October 27, 2026. Signal comparisons match the key's two-decimal percentage precision. No filter fixes were needed.

AI assistance: Codex helped save and run the scripts, verify the results and draft this individual record. Prepared for FIN 43900 as a learning exercise.
