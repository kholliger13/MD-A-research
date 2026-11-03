# Individual submission — Kayla Holliger

## Skill and app

The `buffett-sec` skill is installed in Codex's personal skills location through a link to this course folder. It bundles the SEC download and calculation script. The Streamlit app is `app.py`.

## Verified results

- **COST:** The downloaded SEC results match every supplied fiscal-year date and monetary value for FY2022–FY2026. ROE matches at the supplied one-decimal precision. All three Buffett checks pass. The app shows owner earnings and net income, the table, checks, tags, and memo.
- **JPM:** Capital spending and owner earnings stay **not found**. Both owner-earnings checks stay **not known**. Its memo states: “I cannot judge owner earnings from these data.”
- **Hand-typed number:** Adding `40.0%` to COST's memo field triggers: “Numbers absent from the printed script output: 40.0%.” This was verified through the app using downloaded COST data. The saved memo remains unaltered.

## COST memo and my decision

Read [COST's memo](reports/COST_memo.md).

**My decision:** I cautiously trust the verdict on COST’s business quality because the supplied figures pass all three checks, but those checks alone cannot prove a durable moat or strong management.

## Supporting files

- [Skill](buffett-sec/SKILL.md)
- [SEC script](buffett-sec/scripts/sec_buffett.py)
- [Streamlit app](app.py)
- [COST printed numbers and tags](reports/COST_numbers.md)
- [JPM printed numbers and tags](reports/JPM_numbers.md)
- [JPM memo](reports/JPM_memo.md)
- [Verification record](verification_status.md)

Data: keyless SEC EDGAR, 10-K facts only. Built with AI help as a learning demonstration, not investment advice. AI assistance included code, calculations, memo drafting, and verification. This is an individual submission prepared for Kayla Holliger; it has not been uploaded to a course submission system.
