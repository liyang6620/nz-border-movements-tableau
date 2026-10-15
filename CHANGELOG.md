# Changelog

All notable changes to this project are documented here.

## [2.1.0] - 2026-10-15

### Changed

- Published the final 1280 x 760 dashboard with the direction filter in the left sidebar and four filter-aware KPI cards.
- Clarified the default `(All)` movement context and the 2019 recovery comparison while preserving the arrivals-only interpretation after filtering.
- Connected direction, citizenship, and last-overseas-port selections to the KPI context.
- Refined chart alignment, spacing, map sizing, colour treatment, and mobile readability.
- Replaced repository screenshots with captures from the live Tableau Public release.
- Removed broken clipboard data sources and their unused worksheets from the packaged workbook.
- Updated automated workbook checks to target the named release dashboard and its final authored phone layout.

## [2.0.1] - 2026-10-14

### Changed

- Replaced the ambiguous 2019 comparison label with an explicit Jan-Nov 2025-to-2019 arrival ratio.
- Split the desktop and phone KPI strips into fixed-width metric blocks so labels do not clip at published sizes.
- Shortened the visible dashboard title and rebalanced both layouts around the primary movement trend.
- Added explicit NZ citizen and Non-NZ citizen series labels and legends instead of relying on colour alone, with a dedicated legend row that does not overlap the chart title.
- Removed repeated borders from titles, KPI blocks, and charts so hierarchy is carried by alignment and whitespace rather than boxed panels.
- Rebuilt the dashboard around an executive BI layout: a unified navy rail and report header, explicit KPI comparison wording, and white analytical surfaces on a cool-grey canvas.
- Removed decorative navigation tabs that did not switch views and replaced the overlapping citizenship legend with a dedicated, non-scrolling legend row.
- Replaced the phone layout's floating colour legend with a fixed title-and-key block so it cannot overlap the following chart.
- Reworded the 2019 recovery KPI and compact data guide so comparison periods and field definitions remain fully visible at the published sizes.

## [2.0.0] - 2026-10-14

### Changed

- Reframed the dashboard as a traveller-movement recovery monitor.
- Replaced misleading `Net Arrivals` terminology with `Net Traveller Movements`.
- Renamed the geographic dimension to `Last Overseas Port Country`.
- Excluded the incomplete December 2025 period from analytical views.
- Added a concise KPI strip and data-definition note.
- Removed the redundant travel-mode panel from the dashboard after surfacing air share as a KPI.
- Rebuilt the desktop layout at 1280 x 760 and authored a dedicated phone layout.
- Corrected unsupported tourism, labour-market, origin-country, and migration claims.
- Renamed the Hyper asset to reflect its actual 2019-2025 coverage.
- Added reproducible workbook transformation tooling and Hyper-aware validation tests.

## [1.0.0] - 2025-12-17

- Initial Tableau dashboard and packaged extract.
