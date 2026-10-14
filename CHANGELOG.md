# Changelog

All notable changes to this project are documented here.

## [2.0.1] - 2026-10-14

### Changed

- Replaced the ambiguous 2019 comparison label with an explicit Jan-Nov 2025-to-2019 arrival ratio.
- Split the desktop and phone KPI strips into fixed-width metric blocks so labels do not clip at published sizes.
- Shortened the visible dashboard title and rebalanced both layouts around the primary movement trend.
- Added explicit NZ citizen and Non-NZ citizen series labels and legends instead of relying on colour alone, with a dedicated legend row that does not overlap the chart title.
- Removed repeated borders from titles, KPI blocks, and charts so hierarchy is carried by alignment and whitespace rather than boxed panels.

## [2.0.0] - 2026-10-14

### Changed

- Reframed the dashboard as a traveller-movement recovery monitor.
- Replaced misleading `Net Arrivals` terminology with `Net Traveller Movements`.
- Renamed the geographic dimension to `Last Overseas Port Country`.
- Excluded the incomplete December 2025 period from analytical views.
- Added a concise KPI strip and data-definition note.
- Removed the redundant travel-mode panel from the dashboard after surfacing air share as a KPI.
- Rebuilt the desktop layout at 1200 x 900 and authored a dedicated phone layout.
- Corrected unsupported tourism, labour-market, origin-country, and migration claims.
- Renamed the Hyper asset to reflect its actual 2019-2025 coverage.
- Added reproducible workbook transformation tooling and Hyper-aware validation tests.

## [1.0.0] - 2025-12-17

- Initial Tableau dashboard and packaged extract.
