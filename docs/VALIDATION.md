# Validation Evidence

Validation is performed against both the external Hyper extract and the extract packaged inside the TWBX.

## Automated Checks

- Packaged workbook is a valid ZIP with exactly one `.twb` and one `.hyper`.
- Tableau workbook XML parses successfully.
- Required worksheets, dashboard, calculations, actions, and phone layout exist.
- All analytical worksheets apply the `Complete Month = True` filter.
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

The desktop layout is fixed at 1200 x 900. The phone layout is explicitly authored rather than auto-generated. Screenshots in `screenshots/` are release evidence for both layouts.
