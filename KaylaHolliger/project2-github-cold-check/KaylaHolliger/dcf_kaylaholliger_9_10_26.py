"""Costco FY2025 training DCF. All dollar amounts are USD millions.

used for educational purposes, not financial advice
Run: python dcf_kaylaholliger_9_10_26.py
Uses only the Python standard library. Edit the training assumptions below.
"""

import math

# EDITABLE SENSITIVITY / REVERSE-DCF SETTINGS (rates are decimals).
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 902.60
TARGET_PRICE_STATUS = "Sep. 9, 2026 close; today's price unresolved; dated training target"
TARGET_PRICE_SOURCE = "https://www.financialcontent.com/quote/NQ%3ACOST/historical"
SOLVE_FOR = "uniform_growth_shift"  # Only this variable is supported.
SHIFT_LOWER = -0.05  # -5 percentage points, added to every explicit growth rate.
SHIFT_UPPER = 0.10   # +10 percentage points.
PRICE_TOLERANCE = 0.000001  # Dollars per share.
MAX_ITERATIONS = 200

# Instructor training fixture supplied by the user; illustrative, no market date.
# Cash-flow/cash/debt amounts and share counts use matching million units.
TRAINING_CASE = dict(starting_fcff=100, growth=(0.08, 0.06, 0.05, 0.04, 0.03),
                     wacc=0.10, terminal_growth=0.03, cash=50, debt=300, shares=50)
TRAINING_TARGET = 30.00


SOURCE = "https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm"
DISCLAIMER = "used for educational purposes, not financial advice"

# INPUTS BLOCK
# Reported FY2025 figures: cash flows p. 40; income statement p. 37;
# effective tax rate: Management Discussion, p. 28.
OPERATING_CASH_FLOW = 13_335
CAPITAL_EXPENDITURES = 5_498  # Positive amount representing cash spent.
INTEREST_EXPENSE = 154
TAX_RATE = 0.251

# Simplified FCFF proxy: cash available to debt and equity investors.
# After-tax interest is added back because operating cash flow is after interest.
STARTING_FCFF = OPERATING_CASH_FLOW + INTEREST_EXPENSE * (1 - TAX_RATE) - CAPITAL_EXPENDITURES

# Unresolved forecast inputs retain training values, marked PLACEHOLDER.
# These are NOT company guidance or verified market estimates.
GROWTH = (0.08, 0.07, 0.06, 0.05, 0.04)  # PLACEHOLDER
YEARS = 5
WACC = 0.08  # PLACEHOLDER; Weighted average cost of capital: annual discount rate.
TERMINAL_GROWTH = 0.03  # PLACEHOLDER; Constant annual growth after year 5.

CASH = 14_161  # FY2025 10-K balance sheet, p. 39; excludes investments.
DEBT = 5_805  # FY2025 10-K Note 4, p. 52; includes current portion.
DILUTED_SHARES = 444.803  # Millions; FY2025 weighted average, p. 37.
MARKET_PRICE = 902.60  # USD/share; Sep. 9, 2026 close, FinancialContent.
PRICE_SOURCE = "https://www.financialcontent.com/quote/NQ%3ACOST/historical"
# END INPUTS BLOCK


def calculate_dcf(starting_fcff, growth, wacc, terminal_growth):
    """Use year-end cash flows and the perpetual-growth terminal formula."""
    if starting_fcff <= 0 or not growth:
        raise ValueError("Supply positive starting FCFF and at least one forecast year; negative FCFF requires an explicit cash-flow path.")
    if wacc <= terminal_growth or terminal_growth <= -1:
        raise ValueError("WACC must exceed terminal growth; terminal growth must exceed -100%.")
    if any(rate <= -1 for rate in growth):
        raise ValueError("Forecast growth rates must exceed -100%.")
    rows = []
    fcff = starting_fcff
    for year, rate in enumerate(growth, start=1):
        fcff *= 1 + rate
        present_value = fcff / (1 + wacc) ** year
        rows.append((year, rate, fcff, present_value))
    terminal_value = fcff * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** len(growth)
    enterprise_value = sum(row[3] for row in rows) + pv_terminal
    return rows, terminal_value, pv_terminal, enterprise_value


def value_per_share(growth, wacc, terminal_growth, case=None):
    starting_fcff = STARTING_FCFF if case is None else case["starting_fcff"]
    cash = CASH if case is None else case["cash"]
    debt = DEBT if case is None else case["debt"]
    shares = DILUTED_SHARES if case is None else case["shares"]
    if shares <= 0:
        raise ValueError("Diluted shares must be positive.")
    enterprise_value = calculate_dcf(starting_fcff, growth, wacc, terminal_growth)[3]
    return (enterprise_value + cash - debt) / shares


def print_sensitivity():
    print("\nSENSITIVITY — values per diluted share")
    print("Instructor training case (illustrative; source: user-provided assignment inputs)")
    print("WACC / Terminal g | " + " | ".join(f"{g:>10.1%}" for g in SENSITIVITY_TERMINAL_GROWTHS))
    for wacc in SENSITIVITY_WACCS:
        cells = []
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            if (not math.isfinite(wacc) or not math.isfinite(terminal_growth)
                    or terminal_growth >= wacc or terminal_growth <= -1):
                cells.append(f"{'INVALID':>10}")
            else:
                cells.append(f"{value_per_share(TRAINING_CASE['growth'], wacc, terminal_growth, TRAINING_CASE):>10.2f}")
        print(f"{wacc:>17.1%} | " + " | ".join(cells))
    print("Costco case (placeholder forecast assumptions)")
    print("WACC / Terminal g | " + " | ".join(f"{g:>10.1%}" for g in SENSITIVITY_TERMINAL_GROWTHS))
    for wacc in SENSITIVITY_WACCS:
        cells = []
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            if (not math.isfinite(wacc) or not math.isfinite(terminal_growth)
                    or terminal_growth >= wacc or terminal_growth <= -1):
                cells.append(f"{'INVALID':>10}")
            else:
                cells.append(f"{value_per_share(GROWTH, wacc, terminal_growth):>10.2f}")
        print(f"{wacc:>17.1%} | " + " | ".join(cells))
    print("Fixed: starting FCFF, five explicit growth rates, cash, debt, diluted shares; year-end discounting.")


def solve_growth_shift(target, lower, upper, case=None):
    """Return (shift or None, lower price, upper price); never clip a solution."""
    growth = GROWTH if case is None else case["growth"]
    wacc = WACC if case is None else case["wacc"]
    terminal_growth = TERMINAL_GROWTH if case is None else case["terminal_growth"]
    if not all(math.isfinite(x) for x in (target, lower, upper)):
        raise ValueError("Target and bounds must be finite.")
    if lower >= upper:
        raise ValueError("Lower bound must be less than upper bound.")
    if any(g + bound <= -1 for g in growth for bound in (lower, upper)):
        raise ValueError("Bracket refused: an annual growth rate reaches -100% or below.")
    if PRICE_TOLERANCE <= 0 or not math.isfinite(PRICE_TOLERANCE) or MAX_ITERATIONS <= 0:
        raise ValueError("Tolerance and iteration limit must be positive.")

    def price(shift):
        return value_per_share(tuple(g + shift for g in growth), wacc, terminal_growth, case)

    low_price, high_price = price(lower), price(upper)
    # Positive FCFF and growth factors make price strictly increasing in shift.
    if not low_price <= target <= high_price:
        return None, low_price, high_price
    if target == low_price:
        return lower, low_price, high_price
    if target == high_price:
        return upper, low_price, high_price
    for _ in range(MAX_ITERATIONS):
        midpoint = (lower + upper) / 2
        midpoint_price = price(midpoint)
        if abs(midpoint_price - target) <= PRICE_TOLERANCE:
            return midpoint, low_price, high_price
        if midpoint_price < target:
            lower = midpoint
        else:
            upper = midpoint
    raise ValueError("Bisection did not converge; no solution returned.")


def print_reverse_dcf():
    print("\nREVERSE DCF — conditional scenarios, not proof of mispricing")
    print(f"Instructor training target: ${TRAINING_TARGET:.2f} (illustrative, no market date)")
    print("Training held fixed: " + str(TRAINING_CASE) + "; five years; year-end discounting. Only the uniform growth shift varies.")
    try:
        if SOLVE_FOR != "uniform_growth_shift":
            raise ValueError("Unsupported solve variable; use uniform_growth_shift.")
        training_shift, low, high = solve_growth_shift(TRAINING_TARGET, SHIFT_LOWER, SHIFT_UPPER, TRAINING_CASE)
        if training_shift is None:
            print(f"Training solved shift: none — no solution in that bracket (${low:.6f} to ${high:.6f}).")
        else:
            print(f"Training solved shift: {training_shift * 100:+.6f} percentage points")
            rates = tuple(g + training_shift for g in TRAINING_CASE["growth"])
            print("Training shifted growth: " + ", ".join(f"{g:.6%}" for g in rates))
            print(f"Training matched price: ${value_per_share(rates, TRAINING_CASE['wacc'], TRAINING_CASE['terminal_growth'], TRAINING_CASE):.6f}")
    except ValueError as error:
        print(f"Training reverse DCF refused: {error}")
    print("Costco case — unresolved forecast assumptions")
    print(f"Target price: ${TARGET_SHARE_PRICE:,.2f}; {TARGET_PRICE_STATUS}")
    print(f"Target source: {TARGET_PRICE_SOURCE}")
    print(f"Solve for: {SOLVE_FOR}; bracket {SHIFT_LOWER * 100:+.2f} to {SHIFT_UPPER * 100:+.2f} percentage points")
    print(f"Held fixed: starting FCFF={STARTING_FCFF:,.3f}; WACC={WACC:.1%}; terminal growth={TERMINAL_GROWTH:.1%}; cash={CASH:,.0f}; debt={DEBT:,.0f}; diluted shares={DILUTED_SHARES:,.3f} million; horizon={YEARS} years; year-end discounting.")
    print("Base growth schedule held fixed before adding the same shift: " + ", ".join(f"{g:.1%}" for g in GROWTH))
    try:
        if SOLVE_FOR != "uniform_growth_shift":
            raise ValueError("Unsupported solve variable; use uniform_growth_shift.")
        shift, low_price, high_price = solve_growth_shift(TARGET_SHARE_PRICE, SHIFT_LOWER, SHIFT_UPPER)
        print(f"Prices at bracket endpoints: ${low_price:,.6f} to ${high_price:,.6f}")
        if shift is None:
            print("Solved shift: none — no solution in that bracket.")
        else:
            print(f"Solved shift: {shift * 100:+.6f} percentage points")
            shifted_growth = tuple(g + shift for g in GROWTH)
            print("Shifted annual growth rates: " + ", ".join(f"{g:.6%}" for g in shifted_growth))
            print(f"Matched value per share: ${value_per_share(shifted_growth, WACC, TERMINAL_GROWTH):,.6f}")
    except ValueError as error:
        print(f"Reverse DCF refused: {error}")
    print("This is a conditional training result, not proof of mispricing.")


def print_conditional_call():
    model_price = value_per_share(GROWTH, WACC, TERMINAL_GROWTH)
    print("\nVALUE COMPARISON AND CONDITIONAL CALL — educational scenario")
    print("Today's price: UNRESOLVED. The following comparison uses the dated reverse-DCF target.")
    print(f"Our value/share: ${model_price:,.2f} | comparison price: ${TARGET_SHARE_PRICE:,.2f} | {TARGET_PRICE_STATUS}")
    if not math.isfinite(TARGET_SHARE_PRICE) or TARGET_SHARE_PRICE <= 0:
        print("Price ratio unavailable: target must be finite and positive.")
    else:
        ratio = model_price / TARGET_SHARE_PRICE
        status = "INSIDE" if 0.5 <= ratio <= 2 else "OUTSIDE"
        print(f"Value / price = {ratio:.3f}x: {status} the inclusive 0.5x–2x range. No inputs adjusted.")
        if status == "OUTSIDE":
            print("Input distrusted most: WACC. The 8% is an unsourced placeholder, not an estimated Costco cost of capital; discounting and terminal value are highly sensitive to it.")
    try:
        shift, low, high = solve_growth_shift(TARGET_SHARE_PRICE, SHIFT_LOWER, SHIFT_UPPER)
        if shift is not None:
            print(f"Growth the target assumes: uniform shift {shift * 100:+.6f} percentage points; all other inputs held fixed as listed above.")
        elif TARGET_SHARE_PRICE > high:
            print(f"Growth the target assumes: greater than {SHIFT_UPPER * 100:+.2f} percentage points above every forecast rate would be needed under this model; exact shift unresolved outside the bracket.")
        else:
            print(f"Growth the target assumes: below {SHIFT_LOWER * 100:+.2f} percentage points relative to every forecast rate would be needed; exact shift unresolved outside the bracket.")
    except ValueError as error:
        print(f"Implied-growth comparison unavailable: {error}")
    print(f"Watch-defer. Initiate if a verified price is below about ${model_price:,.2f} AND sourced evidence supports the forecast path and discount rate; otherwise defer. Recalculate the threshold if evidence changes the inputs.")
    print("Monitor: operating margin in the next reported quarter (operating income / revenue), to assess support for the cash-flow growth forecast.")
    print("Evidence floor: PARTIAL — historical inputs sourced; company value, grid, bracketed implied-growth analysis and conditional call shown; forecast assumptions and today's quote remain unresolved.")
    print("Input sources / units / as-of dates:")
    print(f"  Filing: {SOURCE}")
    print("  FCFF: USD millions, FY ended Aug. 31, 2025; derived from OCF and capex p. 40, interest p. 37, effective tax rate p. 28.")
    print("  Cash and debt: USD millions, Aug. 31, 2025; balance sheet p. 39 and debt Note 4 p. 52.")
    print("  Diluted shares: millions, FY2025 weighted average; income statement p. 37.")
    print("  Forecast growth, WACC and terminal growth: annual rates; undated model assumptions, unresolved PLACEHOLDERS. Horizon: five years, assignment.")
    print(f"  Dated quote: $902.60/share, Sep. 9, 2026, 4:00 p.m. EDT close; {PRICE_SOURCE}")
    print("Conditional model judgment only; not proof of mispricing. " + DISCLAIMER)


def main():
    if YEARS != len(GROWTH):
        raise ValueError("Provide one growth rate for each forecast year.")
    rows, terminal_value, pv_terminal, enterprise_value = calculate_dcf(
        STARTING_FCFF, GROWTH, WACC, TERMINAL_GROWTH
    )
    equity_value = enterprise_value + CASH - DEBT
    model_price = equity_value / DILUTED_SHARES
    print("Costco (COST) — training DCF; USD millions except per-share prices")
    print(DISCLAIMER)
    print(f"Starting FCFF: {STARTING_FCFF:,.3f} (FY2025 simplified proxy)")
    print("Growth, Years 1–5: " + ", ".join(f"{g:.1%}" for g in GROWTH) + " (PLACEHOLDER)")
    print(f"WACC: {WACC:.1%} (PLACEHOLDER)")
    print(f"Terminal growth: {TERMINAL_GROWTH:.1%} (PLACEHOLDER)")
    print(f"Cash: {CASH:,.0f} (FY2025)")
    print(f"Debt: {DEBT:,.0f} (FY2025)")
    print(f"Diluted shares: {DILUTED_SHARES:,.3f} million (FY2025 weighted average)")
    print(f"Market price: ${MARKET_PRICE:,.2f} (Sep. 9, 2026 close)")
    print(f"Training enterprise value: {enterprise_value:,.2f}")
    print(f"Training DCF price: ${model_price:,.2f}/share (uses placeholder assumptions)")


if __name__ == "__main__":
    main()
    print_sensitivity()
    print_reverse_dcf()
    print_conditional_call()
