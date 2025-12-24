# New Zealand Border Movements Analysis

## 1. Business Context
International travel plays a critical role in New Zealand’s tourism sector, population change, and labour supply. Border movements are influenced not only by overall travel demand, but also by traveller characteristics, travel modes, and entry or exit points.

Following the COVID-19 pandemic, New Zealand experienced significant border restrictions and a gradual reopening process. Understanding how border movements have changed across different time periods, traveller groups, and travel modes is essential for assessing recovery patterns and structural shifts in international travel.

This project analyses detailed daily border movement data to examine how arrivals and departures vary by time, citizenship, travel mode, port, and demographic characteristics, with a focus on comparing pre-COVID, COVID, and post-COVID periods.

---

## 2. Project Objective
The objective of this project is to analyse daily international border movement data from 2019 to 2025 in order to identify long-term trends, recovery patterns, and structural differences in New Zealand’s border activity across different time periods, traveller groups, and travel characteristics.

---

## 3. Key Analysis Questions
This project seeks to answer the following questions:

1. How have border arrivals and departures changed over time from 2019 to 2025, particularly across pre-COVID, COVID, and post-COVID periods?
2. Is New Zealand experiencing net population inflow or outflow, and how does this vary across different time periods?
3. Are there clear seasonal patterns in border movements, and do these patterns differ by travel mode (air, cruise ship, other sea)?
4. How do border movements differ by traveller characteristics such as citizenship, age group, and sex?

---

## 4. Data Source
- **Source**: Stats NZ – International travel (provisional)
- **Website**: https://www.stats.govt.nz/indicators/international-travel-provisional/
- **Time period**: January 2019 – December 2025
- **Data granularity**: Daily border movements

The dataset includes detailed variables describing each border crossing, including date components (year, month, day), travel direction (arrival or departure), traveller citizenship, travel mode (air, cruise ship, other sea), port of movement, closest overseas port and country, and demographic attributes such as age group and sex.

The time span of the data allows comparison across three key phases:
- Pre-COVID period (2019)
- COVID and border restriction period (2020–2022)
- Post-COVID recovery period (2023–2025)

## 5. Data Understanding & Preparation (Overview)

The dataset records daily international border movements from January 2019 to December 2025. Each record represents aggregated traveller movements by date and characteristics such as travel direction, citizenship, travel mode, port of movement, and selected demographic attributes.

Given the daily granularity and the presence of significant volatility during the COVID period, the analysis design defines two levels of temporal analysis:
- Daily data is used to examine short-term fluctuations and abnormal movements, particularly during periods of border restrictions.
- Monthly aggregated data will be created in later stages of the project to identify long-term trends, seasonal patterns, and recovery dynamics across different years.

To support meaningful comparison, derived fields will be created, including net border movement (arrivals minus departures) and a period classification (Pre-COVID, COVID, and Post-COVID). This enables border activity to be analysed consistently across different policy and travel phases.

Variables with high cardinality, such as individual ports and overseas connections, are reviewed and selectively aggregated or filtered to maintain clarity and interpretability in visualisations. Variables are selected based on analytical relevance, granularity, and their ability to support the project’s key research questions.

## 6. Key Findings

Based on exploratory analysis of New Zealand’s international border movement data from 2019 to 2025, several key patterns and structural changes were identified across time periods, traveller groups, travel modes, and overseas connections.

### 6.1 Overall Border Movement Trends
The monthly arrivals and departures chart shows a clear and immediate structural break beginning in early 2020. Prior to COVID-19, arrivals and departures followed relatively stable seasonal fluctuations, with monthly volumes consistently exceeding 400,000 travellers.

From 2020 through most of 2021, both arrivals and departures dropped to near-zero levels. This confirms the significant impact of border closures and strict travel restrictions during the COVID period. The recovery phase begins in early 2022, where a rapid and sustained increase in both arrivals and departures is visible.

By 2023–2024, monthly border movements return to levels comparable to, and in some months exceeding, pre-COVID volumes, indicating a strong rebound in international travel activity.

### 6.2 Net Arrivals and Population Flow Dynamics

The yearly net arrivals chart highlights meaningful differences across the three periods.

- In 2019, New Zealand experienced a positive net inflow.

- During 2020 and 2021, net arrivals turned negative, indicating that departures exceeded arrivals during the height of border restrictions.

- A strong positive net inflow appears in 2022 and peaks in 2023, suggesting a period of population rebound and increased inbound movement following border reopening.

- In 2024 and 2025, net arrivals decline again, approaching zero or turning slightly negative, indicating a more balanced or stabilising flow between arrivals and departures.

This pattern suggests that post-COVID recovery involved an initial surge of inbound movement, followed by a gradual normalisation rather than continuous growth.
