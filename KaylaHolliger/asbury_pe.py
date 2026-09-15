"""Retrospective FY2024 peer P/E exercise; standard library only.

December 31, 2024 closing prices are paired with subsequently reported
FY2024 total GAAP diluted EPS. Figures come from the user's case table;
underlying source links were not supplied or independently checked here.
Edit the inputs below, then run: python3 asbury_pe.py
"""

import math
from statistics import median


# EDITABLE CASE INPUTS: USD per share. Use None for a missing value.
TARGET = {"ticker": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81},
]
# Case decision: AN is a candidate peer; GPI is a qualified candidate peer.
# Keep both unless business evidence shows one is not comparable.


def positive_number(value):
    """Return whether a price or EPS can support a meaningful P/E."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def ticker_key(company):
    return str(company.get("ticker") or "").strip().upper()


def unique_peers(peers, target):
    """Keep the first occurrence of each ticker and remove the target."""
    seen = set()
    kept = []
    excluded = []
    target_key = ticker_key(target)
    for peer in peers:
        key = ticker_key(peer)
        if not key:
            excluded.append("peer with missing ticker")
        elif key == target_key:
            excluded.append(f"{key} (target)")
        elif key in seen:
            excluded.append(f"{key} (duplicate)")
        else:
            seen.add(key)
            kept.append(peer)
    return kept, excluded


def peer_multiple(peer):
    price, eps = peer.get("price"), peer.get("eps")
    if not positive_number(price) or not positive_number(eps):
        return None
    return price / eps


def implied_price(multiple, target):
    if multiple is None or not positive_number(target.get("eps")):
        return None
    return multiple * target["eps"]


def money(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def main():
    peers, excluded = unique_peers(PEERS, TARGET)
    print("Asbury Automotive (ABG) — retrospective FY2024 peer P/E exercise")
    print("Dec. 31, 2024 closing prices / subsequently reported FY2024 total GAAP diluted EPS")
    print("Inputs: user-supplied case table; underlying source links not supplied or verified in this file.")
    print("P/E = price per share / annual diluted EPS; Asbury is the target, not a peer.")
    print(f"Target: {ticker_key(TARGET)} | price {money(TARGET.get('price') if positive_number(TARGET.get('price')) else None)} | EPS {money(TARGET.get('eps') if positive_number(TARGET.get('eps')) else None)}")
    if excluded:
        print("Excluded: " + ", ".join(excluded))

    valid = []
    for peer in peers:
        multiple = peer_multiple(peer)
        print(f"Peer {ticker_key(peer)}: price {money(peer.get('price') if positive_number(peer.get('price')) else None)} / EPS {money(peer.get('eps') if positive_number(peer.get('eps')) else None)} = " + ("not meaningful" if multiple is None else f"{multiple:.6f}x"))
        if multiple is not None:
            valid.append((ticker_key(peer), multiple))

    multiples = [multiple for _, multiple in valid]
    full_price = None
    if not valid:
        print("No usable peers; median P/E and implied prices: not meaningful.")
    else:
        full_median = median(multiples)
        full_price = implied_price(full_median, TARGET)
        print(f"Median peer P/E: {full_median:.6f}x")
        if len(valid) == 1:
            print("One valid peer: reference estimate, no range.")
            print(f"Reference implied price: {money(full_price)}")
        else:
            for label, multiple in (("Minimum", min(multiples)), ("Median", full_median), ("Maximum", max(multiples))):
                print(f"{label} peer P/E {multiple:.6f}x -> implied ABG price {money(implied_price(multiple, TARGET))}")

    print("Peer-removal sensitivity (dollar changes use unrounded estimates):")
    valid_by_ticker = dict(valid)
    if len(valid) == 2 and "AN" in valid_by_ticker and "GPI" in valid_by_ticker:
        if valid_by_ticker["GPI"] > valid_by_ticker["AN"]:
            print("Prediction: removing GPI lowers the midpoint because GPI has the higher P/E.")
        elif valid_by_ticker["GPI"] < valid_by_ticker["AN"]:
            print("Prediction: removing GPI raises the midpoint because GPI has the lower P/E.")
        else:
            print("Prediction: removing GPI leaves the midpoint unchanged because both P/Es are equal.")
    for peer in peers:
        removed = ticker_key(peer)
        remaining = [multiple for ticker, multiple in valid if ticker != removed]
        if not remaining:
            print(f"Remove {removed}: no estimate (no peers remain).")
            continue
        remaining_price = implied_price(median(remaining), TARGET)
        change = None if remaining_price is None or full_price is None else remaining_price - full_price
        change_text = "not meaningful" if change is None else f"{change:+,.2f}"
        range_note = "; one-peer reference estimate, no range" if len(remaining) == 1 else ""
        print(f"Remove {removed}: remaining median-implied price {money(remaining_price)}; change {change_text}{range_note}")

    if len(valid) == 2 and "AN" in valid_by_ticker and "GPI" in valid_by_ticker:
        print("Explanation: the two-peer median is their midpoint. Removing GPI leaves AN's multiple and its implied price.")
        print("One remaining peer supplies one multiple and one reference price, so there is no peer minimum-to-maximum range.")
    print("Case peer decision: retain AN and qualified GPI unless business evidence warrants changing the peer set.")
    print("Educational peer-multiple comparison; no cash/debt bridge or investment recommendation.")


if __name__ == "__main__":
    main()
