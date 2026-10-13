# Data Dictionary

The Hyper extract stores aggregated traveller movements. Each row represents a combination of date and the available dimensions; `total_movements` is the measure to aggregate.

| Field | Type | Meaning | Notes |
| --- | --- | --- | --- |
| `year` | integer | Calendar year | Derived from the source date |
| `month` | integer | Calendar month number | 1-12 |
| `day` | text | Day value supplied by the source | Use `date` for time analysis |
| `date` | date | Movement date | Coverage: 2019-01-01 to 2025-12-08 |
| `citizenship` | text | Recorded citizenship category | Not residence, visa type, or trip purpose |
| `direction_code` | text | Direction of movement | `A` = arrival; `D` = departure |
| `customs_port_code` | text | New Zealand customs port code | Source-coded value |
| `travel_mode` | text | Travel mode code | `A` is grouped as Air; all other codes as Non-Air |
| `closest_overseas_port_code` | text | Code for the last/closest overseas port | Not a traveller-origin code |
| `closest_overseas_port_name` | text | Name of the last/closest overseas port | Not necessarily trip origin |
| `closest_overseas_port_country` | text | Country of the last/closest overseas port | Not residence or nationality |
| `sex_code` | text | Source sex category | Reported as provided by the source |
| `age_at_travel_range` | text | Age band at time of travel | Aggregated category |
| `total_movements` | integer | Number of traveller movements | Non-negative additive measure |

## Tableau Calculations

| Calculation | Formula | Purpose |
| --- | --- | --- |
| `Net Traveller Movements` | Arrival movements minus departure movements | Directional movement balance; not net migration |
| `Complete Month` | Month(date) is earlier than month(max date) | Removes the current partial month from comparisons |
| `COVID Period` | Pre-COVID / COVID / Post-COVID date bands | Descriptive phase segmentation |
| `Travel Mode Group` | Air vs Non-Air | Makes coded travel mode readable |
