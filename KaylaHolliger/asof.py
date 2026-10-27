"""As-of panel builder: applies four data rules in order, then computes a
point-in-time signal and a naive (look-ahead) signal for comparison.
Standard library only. Edit the inputs below and re-run."""

from datetime import date

# ---------------------------------------------------------------- INPUTS
DECISION_DATE = "2026-03-31"

# Paste the table here (tab-separated, header row first).
RAW_TABLE = """\
Row\tTicker\tMonth measured\tPublished on\tPrice
1\tAAA\t2026-01\t2026-02-10\t101.0
2\tAAA\t2026-02\t2026-03-10\t104.0
3\tAAA\t2026-03\t2026-04-10\t109.0
4\tAAA\t2026-02\t2026-03-25\t103.0
5\tBBB\t2026-01\t2026-02-10\t98.0
6\tBBB\t2026-02\t2026-03-10\t97.0
7\tBBB\t2026-02\t2026-03-10\t97.0
8\tBBB\t2026-03\t2026-04-10\t92.0
9\tCCC\t2026-01\t2026-02-10\t110.0
10\tCCC\t2026-02\t2026-04-05\t112.0
11\t\t2026-02\t2026-03-10\t99.0
12\tCCC\t2026-02\t2026-03-10\t111.0
"""
# ----------------------------------------------------------------------


def parse_table(text):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    rows = []
    for ln in lines[1:]:  # skip header
        parts = (ln.split("\t") + [""] * 5)[:5]
        row_no, ticker, month, published, price = (p.strip() for p in parts)
        rows.append({
            "row": int(row_no),
            "ticker": ticker,
            "month": month,
            "published": date.fromisoformat(published),
            "price": float(price),
        })
    return rows


def prev_month(ym):
    y, m = map(int, ym.split("-"))
    y, m = (y - 1, 12) if m == 1 else (y, m - 1)
    return f"{y:04d}-{m:02d}"


def rule_no_ticker(rows, _):
    removed = [r for r in rows if not r["ticker"]]
    return [r for r in rows if r["ticker"]], removed


def rule_exact_duplicate(rows, _):
    seen, kept, removed = set(), [], []
    for r in rows:
        key = (r["ticker"], r["month"], r["published"], r["price"])
        if key in seen:
            removed.append(r)
        else:
            seen.add(key)
            kept.append(r)
    return kept, removed


def rule_after_decision(rows, decision):
    removed = [r for r in rows if r["published"] > decision]
    return [r for r in rows if r["published"] <= decision], removed


def keep_latest_publication(rows):
    """For each (ticker, month) keep the latest-published row."""
    best = {}
    for r in rows:
        key = (r["ticker"], r["month"])
        if key not in best or r["published"] > best[key]["published"]:
            best[key] = r
    kept_ids = {r["row"] for r in best.values()}
    kept = [r for r in rows if r["row"] in kept_ids]
    removed = [r for r in rows if r["row"] not in kept_ids]
    return kept, removed


def rule_revision(rows, decision):
    # Rule 3 has already dropped anything published after the decision date,
    # but the filter is repeated here so this rule stands on its own.
    eligible = [r for r in rows if r["published"] <= decision]
    return keep_latest_publication(eligible)


RULES = [
    ("1. Quarantine row with no ticker", rule_no_ticker),
    ("2. Remove exact duplicate", rule_exact_duplicate),
    ("3. Remove row published after decision date", rule_after_decision),
    ("4. Keep latest knowable revision per ticker-month", rule_revision),
]


def signals(rows):
    """Percent change from previous month to latest month, per ticker."""
    by_ticker = {}
    for r in rows:
        by_ticker.setdefault(r["ticker"], {})[r["month"]] = r["price"]
    out = {}
    for t in sorted(by_ticker):
        months = by_ticker[t]
        latest = max(months)
        prior = prev_month(latest)
        if prior in months:
            pct = (months[latest] / months[prior] - 1) * 100
            out[t] = (latest, prior, months[prior], months[latest], pct)
        else:
            out[t] = (latest, prior, None, months[latest], None)
    return out


def print_signals(title, sig):
    print(f"\n{title}")
    for t, (latest, prior, p0, p1, pct) in sig.items():
        if pct is None:
            print(f"  {t}: latest month {latest}, no {prior} price -> no signal")
        else:
            print(f"  {t}: {latest} vs {prior}  {p0:.2f} -> {p1:.2f}  "
                  f"= {pct:+.2f}%  (signal month {latest})")


def main():
    decision = date.fromisoformat(DECISION_DATE)
    rows = parse_table(RAW_TABLE)

    print(f"Decision date: {decision}")
    print(f"\nROW FUNNEL  (start: {len(rows)} rows)")
    current = rows
    for name, rule in RULES:
        current, removed = rule(current, decision)
        ids = ", ".join(str(r["row"]) for r in removed) or "none"
        print(f"  {name}: removed {len(removed)} [rows {ids}] "
              f"-> {len(current)} remain")

    print("\nAS-OF PANEL")
    print(f"  {'Row':>3}  {'Ticker':<6} {'Month':<7}  {'Published':<10}  {'Price':>7}")
    for r in sorted(current, key=lambda r: (r["ticker"], r["month"])):
        print(f"  {r['row']:>3}  {r['ticker']:<6} {r['month']:<7}  "
              f"{r['published'].isoformat():<10}  {r['price']:>7.2f}")

    print_signals("AS-OF SIGNAL (knowable on decision date)", signals(current))

    # Naive: every row's latest publication, ignoring the publication date.
    # Rows with no ticker can't be assigned to anything, so they're excluded.
    naive_rows, _ = keep_latest_publication([r for r in rows if r["ticker"]])
    print_signals("NAIVE SIGNAL (latest publication, ignores publish date)",
                  signals(naive_rows))


if __name__ == "__main__":
    main()
