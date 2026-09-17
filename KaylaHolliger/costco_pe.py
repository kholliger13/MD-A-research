"""Costco Lab 08 peer P/E using the saved Lab 07 calculator functions.

Run: python3 costco_pe.py
Sensitivity: python3 costco_pe.py --remove WMT
All prices are unadjusted September 9, 2026 USD closes. EPS is reported
annual GAAP diluted USD per share, public before that date. Source links and
publication dates are recorded in Lab_08_09_17_2026.md.
"""

import argparse
from statistics import median

from asbury_pe import implied_price, peer_multiple, positive_number, ticker_key, unique_peers


TARGET = {"ticker": "COST", "name": "Costco Wholesale", "price": 902.60, "eps": 18.21}
PEERS = [
    {"ticker": "BJ", "name": "BJ's Wholesale Club", "price": 88.51, "eps": 4.38, "decision": "USE"},
    {"ticker": "WMT", "name": "Walmart", "price": 105.83, "eps": 2.73, "decision": "QUALIFY"},
]


def main():
    parser = argparse.ArgumentParser(description="Costco peer P/E calculator")
    parser.add_argument("--remove", metavar="TICKER", help="remove one eligible peer for sensitivity")
    args = parser.parse_args()

    if not positive_number(TARGET["eps"]):
        print("Costco annual reported diluted EPS is zero, negative, or missing; P/E valuation is not meaningful.")
        return
    peers, excluded = unique_peers(PEERS, TARGET)
    if excluded:
        raise ValueError("Unexpected duplicate or invalid peer: " + ", ".join(excluded))
    if any(peer["decision"] not in {"USE", "QUALIFY"} for peer in peers):
        raise ValueError("Only USE and QUALIFY peers may enter the calculator.")
    if args.remove:
        removed = args.remove.strip().upper()
        if removed not in {ticker_key(peer) for peer in peers}:
            parser.error(f"{removed} is not an eligible peer ticker")
        peers = [peer for peer in peers if ticker_key(peer) != removed]

    print("Costco (COST) Lab 08 peer P/E valuation")
    print("Price date: September 9, 2026 close | currency: USD per share")
    print(f"Costco annual reported diluted EPS: ${TARGET['eps']:.2f} (FY ended August 31, 2025)")
    if args.remove:
        print(f"Sensitivity: removed {removed}; main peer decision unchanged")
    implied = []
    for peer in peers:
        multiple = peer_multiple(peer)
        if multiple is None:
            print(f"{ticker_key(peer)}: P/E not meaningful; price or annual EPS invalid.")
            continue
        value = implied_price(multiple, TARGET)
        implied.append(value)
        print(
            f"{ticker_key(peer)} ({peer['decision']}): ${peer['price']:.2f} / "
            f"${peer['eps']:.2f} = {multiple:.6f}x; "
            f"Costco implied price = ${value:.2f}"
        )

    if len(implied) >= 2:
        print(f"Peer-implied Costco range: ${min(implied):.2f}–${max(implied):.2f}")
        print(f"Median peer-implied Costco price: ${median(implied):.2f}")
    elif implied:
        print(f"Single-peer Costco reference price: ${implied[0]:.2f}; no peer range.")
    else:
        print("No usable peer P/E; Costco implied price unresolved.")


if __name__ == "__main__":
    main()
