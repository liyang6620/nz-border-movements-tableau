# New Zealand Border Movement Monitor

[![CI](https://github.com/liyang6620/nz-border-movements-tableau/actions/workflows/ci.yml/badge.svg)](https://github.com/liyang6620/nz-border-movements-tableau/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/liyang6620/nz-border-movements-tableau)](https://github.com/liyang6620/nz-border-movements-tableau/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An interactive Tableau BI project for monitoring New Zealand traveller movements across the pre-COVID, restriction, and recovery periods. It combines a decision-focused dashboard with explicit metric definitions, a reproducible workbook transformation, and automated validation of the packaged Hyper extract.

**[Open the live Tableau Public dashboard](https://public.tableau.com/app/profile/yang.li7346/viz/nz-border-movements/NewZealandBorderMovementRecoveryMonitor)** | [View the latest release](https://github.com/liyang6620/nz-border-movements-tableau/releases/latest) | [Review validation evidence](docs/VALIDATION.md)

![Desktop dashboard showing border movement KPIs and trends](screenshots/dashboard-desktop.png)

## Project at a Glance

| Area | Implementation |
| --- | --- |
| Business question | How far have New Zealand traveller movements recovered, and how do patterns vary by time and traveller dimension? |
| Delivery | Interactive Tableau dashboard with authored desktop and phone layouts |
| Data scale | 2,222,255 aggregated rows and 60,866,193 traveller movements |
| Coverage | 1 Jan 2019 to 8 Dec 2025; analytical views use complete months through Nov 2025 |
| Core analysis | Arrivals, departures, year-on-year change, arrival volume relative to 2019, net traveller movements, age, citizenship, port country, and travel mode |
| Quality controls | Hyper integrity tests, workbook structure checks, semantic safeguards, screenshot checks, and GitHub Actions CI |
| Reproducibility | Deterministic Python transformation for reviewed workbook definitions and layout changes |

## What This Project Demonstrates

- **Dashboard design:** a compact KPI hierarchy, focused comparisons, and supporting views without redundant charts.
- **Analytical correctness:** comparable January-November periods and automatic exclusion of partial December 2025 data.
- **Metric governance:** precise use of `Net Traveller Movements` and `Last Overseas Port Country`, with unsupported migration, tourism, and labour-market claims removed.
- **Responsive delivery:** a 1200 x 900 desktop dashboard and a separately authored phone layout rather than a scaled-down desktop canvas.
- **Engineering discipline:** versioned workbook assets, reproducible transformations, data and workbook tests, documented assumptions, and CI.

## Decision Context

The dashboard answers questions supported by the available data:

- How have monthly arrivals and departures changed since 2019?
- How close are 2025 arrivals to the comparable 2019 period?
- How do movement patterns vary by age group and citizenship?
- Which countries appear most often as the last overseas port before arrival?
- What share of arrivals travel by air?

It does **not** infer traveller purpose, residence, tourism demand, labour supply, or migration status.

## Headline Results

All comparisons use January-November to keep periods comparable. The extract is current through 8 December 2025, but December is excluded because it is incomplete.

| Metric | Result | Definition |
| --- | ---: | --- |
| 2025 arrivals | 6.02M | Arrival movements, Jan-Nov 2025 |
| Year-on-year change | +4.3% | 2025 Jan-Nov vs 2024 Jan-Nov arrivals |
| 2025 arrivals relative to 2019 | 94.2% | 2025 Jan-Nov arrivals equal 94.2% of 2019 Jan-Nov arrivals |
| Net traveller movements | -1.5K | Arrivals minus departures, Jan-Nov 2025 |
| Air share | 99.2% | Air arrivals / all arrivals, Jan-Nov 2025 |

The largest 2024 arrival age band is 40-69 (2.90M), not 18-39 (2.21M). This is a descriptive traveller-movement result, not a labour-market conclusion.

## Dashboard Experience

The desktop layout follows an insight-first hierarchy: five fixed-width KPI blocks, the primary monthly movement trend in the upper-left, net movement alongside it, then demographic and geographic context. The citizenship series are explicitly labelled as NZ citizens and Non-NZ citizens instead of relying on colour alone. Air share appears once in the KPI strip instead of being repeated in a low-information chart.

The phone layout preserves the same analytical sequence with readable charts and touch-friendly spacing.

<img src="screenshots/dashboard-mobile.png" alt="Phone layout of the border movement dashboard" width="375">

Visible analytical safeguards include:

- incomplete months excluded from every analytical worksheet;
- data freshness stated in the dashboard;
- net traveller movements kept distinct from net migration; and
- last overseas port country kept distinct from origin, residence, and nationality.

## Technical Approach

```text
Stats NZ provisional data
          |
          v
Validated Hyper extract ----> Tableau workbook ----> Desktop and phone dashboards
          |                           |
          v                           v
Data integrity tests          Workbook structure tests
          \___________________________/
                        |
                        v
                 GitHub Actions CI
```

The packaged workbook contains its own Hyper extract, so it does not depend on the original local spreadsheet path. Tests also verify that the packaged and external Hyper extracts have identical SHA-256 hashes.

Detailed references:

- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Metric definitions](docs/METRIC_DEFINITIONS.md)
- [Validation evidence](docs/VALIDATION.md)

## Run Locally

Requirements:

- Python 3.12+
- Tableau Desktop or Tableau Public 2025.3+ to edit the workbook

```bash
git clone https://github.com/liyang6620/nz-border-movements-tableau.git
cd nz-border-movements-tableau
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Open `workbook/nz-border-movements.twbx` to inspect or publish the dashboard.

To reapply the reviewed workbook definitions and layout changes deterministically:

```bash
python scripts/transform_workbook.py
```

## Repository Structure

```text
.
|-- data/                 # Hyper extract used by automated data checks
|-- docs/                 # Definitions, assumptions, and validation evidence
|-- screenshots/          # Desktop and phone release evidence
|-- scripts/              # Deterministic TWBX transformation tooling
|-- tests/                # Workbook and Hyper integrity tests
`-- workbook/             # Packaged Tableau workbook
```

## Limitations

- December 2025 is partial and excluded from trend and comparison views.
- The data counts movement events, not unique people.
- Arrivals minus departures is not net migration and cannot measure population change.
- Citizenship is not residence, visa type, trip purpose, or visitor status.
- Last overseas port country is the last overseas port in the journey, not necessarily the traveller's origin.
- Provisional data may be revised by Stats NZ.
- This is a portfolio-grade BI demonstration, not an operational forecasting or policy system.

## Project Governance

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance, [SECURITY.md](SECURITY.md) for security reporting, and [CHANGELOG.md](CHANGELOG.md) for release history. Code and workbook configuration are available under the [MIT License](LICENSE); the underlying data remains subject to the source provider's terms.

