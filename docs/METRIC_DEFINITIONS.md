# Metric Definitions

Unless stated otherwise, headline 2025 metrics use January-November, the latest complete comparable period in the extract. The dashboard opens with `Direction = (All)`, so its default KPI context includes arrivals and departures. The cards recalculate when a supported direction, citizenship, or last-overseas-port selection is applied.

## Selected Movements

```text
SUM(total_movements) in the active dashboard filter context
```

Default result for Jan-Nov 2025: **12,033,708** movements (**12.034M**). A movement is a border-crossing event, not a unique person.

## Year-on-Year Change

```text
(2025 Jan-Nov selected movements / 2024 Jan-Nov selected movements) - 1
```

Default result: **+4.6%** (12,033,708 vs 11,506,047).

## Recovery vs 2019

```text
2025 Jan-Nov selected movements / 2019 Jan-Nov selected movements
```

Default result: **94.4%** (12,033,708 vs 12,752,709). In other words, January-November 2025 movement volume reached 94.4% of the corresponding 2019 level. This is a period-to-period volume ratio, not a growth rate or an economic recovery index.

With `Direction = Arrivals`, the same cards report:

| Metric | Result | Compared values |
| --- | ---: | ---: |
| Selected movements | 6.016M | 6,016,113 arrivals |
| Year-on-year change | +4.3% | 6,016,113 vs 5,767,833 |
| Recovery vs 2019 | 94.2% | 6,016,113 vs 6,388,800 |
| Air share | 99.23% | 5,970,054 / 6,016,113 |

## Net Traveller Movements

```text
SUM(IF direction_code = "A" THEN total_movements ELSE -total_movements END)
```

Result for Jan-Nov 2025: **-1,482**. This measure is not net migration, because the dataset does not identify migrant status, usual residence, or permanent/long-term movement.

## Air Share

```text
air movements / selected movements
```

Default result for Jan-Nov 2025: **99.2%** (11,942,820 / 12,033,708). With the arrivals filter applied, the result is **99.23%** (5,970,054 / 6,016,113).

## Interactive Filter Scope

- The direction control changes the four KPI cards and the movement context.
- Selecting a citizenship series or last-overseas-port country updates the KPI context through dashboard filter actions.
- Clearing a selection restores the broader context.
- The net traveller movement chart remains a signed arrivals-minus-departures measure and is not redefined as migration.

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
