# SDVOSB market derivation from USASpending

Mike's method, 2026-08-26. Feeds the Market-Size sheet of
`../sdvosb-financial-model-v4-target-backed.xlsx`.

Reproduce: `python3 pull_sdvosb_tam.py` (free, keyless, ~3 min).

Free public API, our own analysis, nothing redistributed — this is deliberately not the
data-feed line that PLAN-V5 risk 2 / TASK-0019 flags as ToS-exposed.

## Files

| File                      | What                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| `pull_sdvosb_tam.py`      | The pull. Filters, windows and endpoints are documented in its docstring.                  |
| `SUMMARY.json`            | Everything: per-FY counts, 3-year NAICS ranking, per-NAICS FY2025 actions and firm counts. |
| `DERIVED.txt`             | The aggregates quoted in the workbook and SUMMARY-v4.md.                                   |
| `naics_<scope>_<fy>.json` | Full NAICS distribution per scope per fiscal year.                                         |

`recipients_<scope>_<fy>.json` are **not** committed (~1.8 MB of firm names, regenerable by
re-running the script). Only the distinct counts are used, and those are in `SUMMARY.json`.

## Headlines

- Firms that **win** SDVOSB set-aside work: ~1,700/yr, 2,989 distinct over FY2023-FY2025.
  The certified pool is ~15,000. Do not plan off the certified number.
- New award actions: 11,950 -> 11,429 -> 9,255 all-agency; 6,929 -> 6,035 -> 5,125 VA.
  **Down 23% and 26% respectively.** Re-run quarterly.
- Work spans ~390 distinct NAICS. The current 6 target codes capture 1,849 of FY2025's 9,255
  all-agency actions (20%).
- Supersedes the ~250-400 sellable-notice-moments figure as the planning denominator for a
  multi-deliverable-type product. See the Market-Size sheet, section 5, for the reconciliation.
