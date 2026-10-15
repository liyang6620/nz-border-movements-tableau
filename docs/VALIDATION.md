# Validation Evidence

Validation is performed against both the external Hyper extract and the extract packaged inside the TWBX.

## Automated Checks

- Packaged workbook is a valid ZIP with exactly one `.twb` and one `.hyper`.
- Tableau workbook XML parses successfully.
- Required worksheets, the named release dashboard, filter actions, and the authored phone layout exist.
- Analytical worksheets apply the `Complete Month = True` filter; KPI calculations explicitly limit comparisons to January-November.
- Packaged and external Hyper extracts have identical SHA-256 hashes.
- Schema includes all 14 expected fields with compatible data types.
- `direction_code` contains only `A` and `D`.
- `total_movements` is never negative.
- Date coverage, row count, and total movement count match the reviewed baseline.
- The latest source month is detected as incomplete.

Run locally with:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

## Reviewed Baseline

| Check | Expected |
| --- | ---: |
| Minimum date | 2019-01-01 |
| Maximum date | 2025-12-08 |
| Rows | 2,222,255 |
| Total movements | 60,866,193 |
| Negative movement rows | 0 |
| Direction values | A, D |
| Latest complete month | Nov 2025 |

## Visual QA

The desktop layout is fixed at 1280 x 760. The phone layout is explicitly authored as a 375 x 2600 vertical experience rather than auto-generated. The PNG files in `screenshots/` were captured from the live Tableau Public release and are checked for expected dimensions and non-trivial file size in CI.

Published dashboard: [New Zealand Border Movement Recovery Monitor](https://public.tableau.com/app/profile/yang.li7346/viz/nz-border-movements/NewZealandBorderMovementRecoveryMonitor)
