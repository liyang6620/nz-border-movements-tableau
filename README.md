# New Zealand Border Movements – Tableau Analytics Dashboard (2019–2025)

**Business-focused analytics for tourism, labour mobility, and population recovery planning**

🔗 **Live Interactive Dashboard:**  
https://public.tableau.com/app/profile/yang.li7346/viz/nz-border-movements/ImpactofCOVID-19onNewZealandBorderMovements20192025?publish=yes

---

## Executive Summary

This Tableau analytics project examines New Zealand’s international border movements across three structural phases — **pre-COVID, COVID restrictions, and post-COVID recovery (2019–2025)** — and translates the findings into **actionable business insights** for tourism, immigration, and labour-market stakeholders.

**Top findings at a glance:**
- Recovery is **led by non-NZ citizens** and **working-age arrivals (18–39)**.
- Air travel accounts for **nearly all inbound volume**; cruise-based recovery is negligible.
- 2023 surge represents a **temporary rebound**, while **2024–25 trends flatten**, signaling stabilization rather than continuous growth.

---

## Business Problem

New Zealand’s economy depends heavily on:
| Area | Why it matters |
|------|----------------|
| Tourism | Major GDP and regional employment contributor |
| Labour supply | Hospitality, agriculture, and healthcare rely on migrant inflows |
| International students | Strong influence on rental market, spending, and population |
| Net migration | Shapes labour force and long-term population growth |

After border closures, stakeholders need to know:

- Which traveller groups are returning fastest?
- Is post-COVID growth sustainable or a one-off spike?
- Which countries deserve tourism marketing budget?
- Has inbound labour supply returned enough to relieve shortages?

---

## Solution Overview

This project delivers an **interactive Tableau dashboard** that allows users to:
- Compare yearly trends pre-/during-/post-COVID  
- Filter by age, citizenship, sex, travel mode, and country  
- View net migration movement as a simple population-change proxy  
- Interpret insights without needing technical or database skills  

**Dashboard Design Goals**
- Business-first: enable decisions, not just charts
- Reduce cognitive load: visual clarity > complexity
- Support self-exploration by non-technical users

---

## Data & Preparation

| Item | Details |
|------|---------|
| Data Source | Stats NZ – International travel (provisional) |
| Range | Jan 2019 – Dec 2025 |
| Raw Files | 3 × CSV snapshots downloaded directly from Stats NZ |
| Preparation Method | Tableau Wildcard Union + data cleaning inside Tableau |

**Derived fields created**
- `Net Movement = Arrivals – Departures`
- `Period Phase = Pre-COVID / COVID / Post-COVID`
- Monthly aggregation fields for trend comparison

No Python or ETL tooling was required — data modelling occurred **inside Tableau**, reflecting how BI analysts often work with spreadsheet-based datasets in the real world.

---

## Key Insights & Commercial Implications

| Insight | What It Means for Business |
|--------|-----------------------------|
| Recovery almost entirely driven by **air travel** | Partner with airlines; cruise promotions deliver low ROI |
| **Non-NZ citizens** drive inbound recovery | Target tourism, study, and work visa marketing at overseas audiences |
| Post-COVID rebound **peaks in 2023, then stabilises** | Avoid over-forecasting; plan workforce & enrolment on stable baselines |
| Strongest recovery among **18–39 working-age group** | Young-talent and labour-visa programs can relieve shortages |
| Arrivals remain concentrated (AU, US, CN) | Marketing should reinforce proven markets before expanding |

---
### Business Value 
- Help NZ tourism board decide which origin markets deserve most marketing budget
- Inform labour-market immigration forecast (student vs worker inflow)
- Assist government or airports with planning seasonal resource allocation

## Dashboard Features

| Feature | What It Helps You Answer |
|--------|---------------------------|
| **Overall Trend View (2019–2025)** | Shows how border movements changed before, during, and after COVID restrictions |
| **Arrivals vs Departures Comparison** | Reveals whether NZ experienced net positive or negative movement in a selected timeframe |
| **Citizenship Filter (NZ vs Non-NZ)** | Separates returning residents from inbound tourists to identify who drives recovery |
| **Age Group Breakdown (18–39, 40+, etc.)** | Indicates whether working-age travellers or older demographics contribute most to movement |
| **Travel Mode Selector – Air vs No-Air** | Compares the scale of air-travel recovery vs cruise-based recovery |
| **Top Origin Countries Ranking** | Highlights which countries (AU, US, CN, etc.) are key sources of arrivals |
| **Net Movement Metric (Arrivals – Departures)** | Provides a lightweight population-change proxy without demographic modelling |
| **Interactive Origin Map (global filter)** | Selecting a country on the map updates the entire dashboard to focus on that origin group |

---

## Limitations & Next Steps

**Limitations**
- Dataset is aggregated; no purpose-of-travel metadata
- Cannot distinguish student vs worker vs tourist

**Possible Enhancements**
- Incorporate visa, GDP, and unemployment datasets
- Use Tableau forecasting or ML to predict future trends
- Deploy dashboard into a business-facing web app (AWS + Tableau Embed)

---

## About the Analyst

**Yang Li – Data Analyst (Auckland, NZ)**  
Skills: Tableau, SQL, Python (ETL), AWS fundamentals, dashboard storytelling  



