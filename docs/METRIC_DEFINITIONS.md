# Metric Definitions

Unless stated otherwise, headline 2025 metrics use January-November, the latest complete comparable period in the extract.

## Arrivals

```text
SUM(total_movements) WHERE direction_code = "A"
```

This counts arrival movements, not unique people.

## Year-on-Year Arrival Change

```text
(2025 Jan-Nov arrivals / 2024 Jan-Nov arrivals) - 1
```

Result: **+4.3%** (6,016,113 vs 5,767,833).

## 2025 Arrivals Relative to 2019

```text
2025 Jan-Nov arrivals / 2019 Jan-Nov arrivals
```

Result: **94.2%** (6,016,113 vs 6,388,800). In other words, 2025 January-November arrival volume reached 94.2% of the corresponding 2019 level. This compares traveller-movement volume only; it is not an economic recovery index or a growth rate.

## Net Traveller Movements

```text
SUM(IF direction_code = "A" THEN total_movements ELSE -total_movements END)
```

Result for Jan-Nov 2025: **-1,482**. This measure is not net migration, because the dataset does not identify migrant status, usual residence, or permanent/long-term movement.

## Air Share

```text
air arrival movements / all arrival movements
```

Result for Jan-Nov 2025: **99.23%** (5,970,054 / 6,016,113).

## Complete Month Rule

```tableau
DATETRUNC('month', [Date]) < DATETRUNC('month', { MAX([Date]) })
```

The extract ends on 8 December 2025. The calculation therefore retains data through 30 November 2025 and prevents a partial December value from appearing as an artificial decline.

## COVID Period Bands

- Pre-COVID: before 1 March 2020
- COVID: 1 March 2020 through 30 June 2022
- Post-COVID: from 1 July 2022

These bands are presentation aids, not causal claims.
