"""ABG five-year pro forma; USD millions except value per share."""

import math


OPENING = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}

ASSUMPTIONS = {
    "growth": 0.018,
    "gross_margin": 0.1705,
    "sga_ratios": (0.665, 0.655, 0.645, 0.645, 0.645),
    "depreciation_ratio": 82.4 / 3070.4,
    "impairment": 120.0,
    "capex": 250.0,
    "tax_rate": 0.255,
    "inventory_days": 2135.8 / (17999.0 - 3071.7) * 365,
    "floor_plan_ratio": 2027.0 / 2135.8,
    "other_wc_ratio": 0.008,
    "minimum_cash": 25.0,
    "revolver_limit": 850.0,
    "revolver_rate": 0.06,
    "repayment": 150.0,
    "buyback": 150.0,
    "floor_plan_rate": 0.0467,
    "debt_rate": 0.0544,
    "cost_of_equity": 0.10,
    "terminal_growth": 0.025,
    "shares": 17.951349,
}


def project(opening, assumptions):
    prior = opening.copy()
    rows = []
    for year, sga_ratio in zip(range(2026, 2031), assumptions["sga_ratios"]):
        r = {"year": year}
        r["revenue"] = prior["revenue"] * (1 + assumptions["growth"])
        r["gross_profit"] = r["revenue"] * assumptions["gross_margin"]
        r["cost_of_sales"] = r["revenue"] - r["gross_profit"]
        r["sga"] = r["gross_profit"] * sga_ratio
        r["depreciation"] = prior["ppe"] * assumptions["depreciation_ratio"]
        r["impairment"] = assumptions["impairment"]
        r["operating_income"] = (r["gross_profit"] - r["sga"]
                                 - r["depreciation"] - r["impairment"])
        r["interest"] = (prior["floor_plan"] * assumptions["floor_plan_rate"]
                         + prior["debt"] * assumptions["debt_rate"]
                         + prior["revolver"] * assumptions["revolver_rate"])
        r["pretax"] = r["operating_income"] - r["interest"]
        r["tax"] = max(0.0, r["pretax"]) * assumptions["tax_rate"]
        r["net_income"] = r["pretax"] - r["tax"]

        r["inventory"] = r["cost_of_sales"] * assumptions["inventory_days"] / 365
        r["floor_plan"] = r["inventory"] * assumptions["floor_plan_ratio"]
        r["capex"] = assumptions["capex"]
        r["ppe"] = prior["ppe"] + r["capex"] - r["depreciation"]
        r["other_wc_change"] = assumptions["other_wc_ratio"] * (r["revenue"] - prior["revenue"])
        r["other_assets"] = prior["other_assets"] + r["other_wc_change"] - r["impairment"]
        r["repayment"] = assumptions["repayment"]
        r["debt"] = prior["debt"] - r["repayment"]
        r["other_liabilities"] = prior["other_liabilities"]
        r["buyback"] = assumptions["buyback"]
        r["equity"] = prior["equity"] + r["net_income"] - r["buyback"]

        r["inventory_change"] = r["inventory"] - prior["inventory"]
        r["floor_plan_change"] = r["floor_plan"] - prior["floor_plan"]
        r["fcfe"] = (r["net_income"] + r["depreciation"] + r["impairment"]
                     - r["capex"] - r["inventory_change"] - r["other_wc_change"]
                     + r["floor_plan_change"] - r["repayment"])
        r["opening_cash"] = prior["cash"]
        cash_before_revolver = prior["cash"] + r["fcfe"] - r["buyback"]
        if cash_before_revolver < assumptions["minimum_cash"]:
            needed = assumptions["minimum_cash"] - cash_before_revolver
            available = max(0.0, assumptions["revolver_limit"] - prior["revolver"])
            r["revolver_change"] = min(needed, available)
        else:
            r["revolver_change"] = -min(prior["revolver"], cash_before_revolver - assumptions["minimum_cash"])
        r["revolver"] = prior["revolver"] + r["revolver_change"]
        r["cash"] = cash_before_revolver + r["revolver_change"]

        r["operating_cash_flow"] = (r["net_income"] + r["depreciation"]
                                    + r["impairment"] - r["inventory_change"]
                                    - r["other_wc_change"])
        r["investing_cash_flow"] = -r["capex"]
        r["financing_cash_flow"] = (r["floor_plan_change"] - r["repayment"]
                                    - r["buyback"] + r["revolver_change"])
        r["cash_change"] = r["operating_cash_flow"] + r["investing_cash_flow"] + r["financing_cash_flow"]
        r["assets"] = r["cash"] + r["inventory"] + r["ppe"] + r["other_assets"]
        r["liabilities"] = r["floor_plan"] + r["debt"] + r["revolver"] + r["other_liabilities"]
        r["liabilities_and_equity"] = r["liabilities"] + r["equity"]
        r["balance_gap"] = r["assets"] - r["liabilities"] - r["equity"]
        r["cash_headroom"] = r["cash"] - assumptions["minimum_cash"]
        rows.append(r)
        prior = r
    return rows


def assert_balanced(rows, tolerance=1e-7):
    for r in rows:
        gap = r["balance_gap"]
        if not math.isfinite(gap) or abs(gap) > tolerance:
            raise ValueError(f"{r['year']}: balance-sheet check failed; gap = {gap:.10f} million")
        headroom = r["cash_headroom"]
        if not math.isfinite(headroom) or headroom < -tolerance:
            raise ValueError(f"{r['year']}: minimum-cash check failed; gap = {headroom:.10f} million")


def print_table(title, items, rows):
    width = 38
    print("\n" + title)
    print(f"{'USD millions':<{width}}" + "".join(f"{r['year']:>14}" for r in rows))
    print("-" * (width + 14 * len(rows)))
    for label, key, sign in items:
        values = []
        for r in rows:
            value = r[key] * sign
            if abs(value) < 0.05:
                value = 0.0
            values.append(f"{value:>14,.1f}")
        print(f"{label:<{width}}" + "".join(values))


def main():
    if len(ASSUMPTIONS["sga_ratios"]) != 5:
        raise ValueError("Provide exactly five SG&A ratios for 2026–2030")
    rows = project(OPENING, ASSUMPTIONS)
    print("Asbury Automotive Group (ABG): 2026–2030 pro forma")
    print_table("INCOME STATEMENT", [
        ("Revenue", "revenue", 1), ("Cost of sales", "cost_of_sales", -1),
        ("Gross profit", "gross_profit", 1), ("SG&A", "sga", -1),
        ("Depreciation", "depreciation", -1), ("Impairment", "impairment", -1),
        ("Operating income", "operating_income", 1), ("Interest", "interest", -1),
        ("Pretax income", "pretax", 1), ("Tax", "tax", -1),
        ("Net income", "net_income", 1),
    ], rows)
    print_table("BALANCE SHEET", [
        ("Cash", "cash", 1), ("Inventory", "inventory", 1),
        ("PP&E", "ppe", 1), ("Other assets", "other_assets", 1),
        ("Total assets", "assets", 1), ("Floor plan", "floor_plan", 1),
        ("Term debt", "debt", 1), ("Revolver", "revolver", 1),
        ("Other liabilities", "other_liabilities", 1),
        ("Total liabilities", "liabilities", 1), ("Equity", "equity", 1),
        ("Total liabilities and equity", "liabilities_and_equity", 1),
    ], rows)
    print_table("CASH FLOW STATEMENT", [
        ("Net income", "net_income", 1), ("Depreciation addback", "depreciation", 1),
        ("Impairment addback", "impairment", 1),
        ("Inventory investment", "inventory_change", -1),
        ("Other working capital investment", "other_wc_change", -1),
        ("Operating cash flow", "operating_cash_flow", 1),
        ("Capital spending", "capex", -1),
        ("Investing cash flow", "investing_cash_flow", 1),
        ("Net floor plan borrowing", "floor_plan_change", 1),
        ("Debt repayment", "repayment", -1), ("Share buyback", "buyback", -1),
        ("Revolver draw / (repayment)", "revolver_change", 1),
        ("Financing cash flow", "financing_cash_flow", 1),
        ("Change in cash", "cash_change", 1), ("Opening cash", "opening_cash", 1),
        ("Closing cash", "cash", 1),
        ("Memo: FCFE before buyback/revolver", "fcfe", 1),
    ], rows)
    print_table("CHECKS", [
        ("Assets - liabilities - equity", "balance_gap", 1),
        ("Cash above minimum", "cash_headroom", 1),
    ], rows)
    assert_balanced(rows)
    print("All five years: balance sheet PASS; minimum cash PASS.")

    cost = ASSUMPTIONS["cost_of_equity"]
    growth = ASSUMPTIONS["terminal_growth"]
    if cost <= growth:
        raise ValueError("Cost of equity must exceed terminal growth")
    if ASSUMPTIONS["shares"] <= 0:
        raise ValueError("Share count must be positive")
    pv_fcfe = sum(r["fcfe"] / (1 + cost) ** year for year, r in enumerate(rows, 1))
    terminal_value = (rows[-1]["fcfe"] + rows[-1]["repayment"]) * (1 + growth) / (cost - growth)
    pv_terminal = terminal_value / (1 + cost) ** 5
    equity_value = pv_fcfe + pv_terminal
    print("\nEQUITY VALUATION")
    print(f"PV of 2026–2030 FCFE: ${pv_fcfe:,.2f} million")
    print(f"PV of value after 2030: ${pv_terminal:,.2f} million")
    print(f"Equity value: ${equity_value:,.2f} million")
    if equity_value == 0:
        print("Share of value after 2030: undefined (zero equity value)")
    else:
        print(f"Share of value after 2030: {pv_terminal / equity_value:.2%}")
    print(f"Value per share: ${equity_value / ASSUMPTIONS['shares']:,.2f}")


if __name__ == "__main__":
    main()
