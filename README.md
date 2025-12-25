# 🇳🇿 New Zealand Border Movements Analytics Dashboard (2019–2025)
**Business-Focused Travel & Migration Insights for Tourism and Policy Stakeholders**  
📊 Tableau Dashboard | 📁 Stats NZ Data | 🧭 Actionable Business Insights

---

## 1️⃣ Executive Summary
This project presents a **business-oriented analytics dashboard** built to support organisations involved in **tourism, immigration, labour mobility, and international education** in New Zealand.

Using 7 years of border movement data (2019–2025), the dashboard uncovers how COVID-19 reshaped international mobility and identifies **which traveller groups and markets are driving recovery**, helping stakeholders prioritise investments and policy focus.

👉 **Live Interactive Dashboard:**  
https://public.tableau.com/app/profile/yang.li7346/viz/nz-border-movements/ImpactofCOVID-19onNewZealandBorderMovements20192025?publish=yes

---

## 2️⃣ Business Problem
New Zealand relies heavily on international travel for:

- Tourism revenue
- Workforce supply (hospitality, agriculture, healthcare)
- International students
- Net population growth

Border closures caused a collapse in international arrivals, generating **economic losses and labour shortages**. Today, stakeholders need data to answer:

| Key Business Questions |
|------------------------|
| Which traveller segments are recovering fastest? |
| Should tourism marketing budgets prioritise Australia, US, China or other markets? |
| Is the rebound temporary or long-term? |
| Has NZ’s labour-related mobility (18–39 age arrivals) returned to pre-COVID levels? |

---

## 3️⃣ Solution Overview
This project delivers:

✔️ A multi-layer Tableau dashboard  
✔️ Segmentation across age, citizenship, mode, region, and time  
✔️ Commercial-grade insights that support investment & policy decisions  

**Dashboard Design Goals**
- Make complex trends digestible for non-technical business users
- Enable quick comparison between pre-COVID, COVID and post-COVID phases
- Provide actionable context to guide planning and investment

---

## 4️⃣ Data Source & Preparation
| Item | Details |
|------|---------|
| Source | Stats NZ – International Travel (Provisional) |
| Time Span | Jan 2019 – Dec 2025 |
| Files Used | Three CSV snapshots downloaded directly from Stats NZ |
| Preparation Method | Tableau Wildcard Union + data model + calculated fields |

No programming language was required — **data preparation took place inside Tableau**, including:
- Wildcard CSV union to merge multi-file datasets
- Field selection and data cleaning
- Derived fields such as:
  - Net border movement (Arrivals – Departures)
  - Period category (Pre-COVID, COVID, Post-COVID)

This models real-world analyst workflows where data often arrives as flat files and analysts must **clean, structure, and derive meaning directly inside BI tools**.

---

## 5️⃣ Key Insights & Commercial Implications

| Finding | Business / Policy Action |
|---------|--------------------------|
| Recovery is almost entirely driven by **air travel**, cruise remains structurally small | Tourism NZ should prioritise airline partnerships → cruise-based campaigns deliver low ROI |
| **Non-NZ citizens** drive most of the post-COVID recovery | Marketing and visa improvements should target inbound tourism, workers, and students |
| Recovery peaked in 2023, **2024–25 stabilises** | Do not overestimate long-term rebound — labour/education planning must assume stable baseline |
| Working-age groups (18–39, 40–69) dominate mobility | Labour shortages can be relieved through attracting these cohorts, especially 18–39 |
| Arrivals geographically remain **highly concentrated (AU, US, CN)** | Marketing budgets should reinforce existing proven markets rather than expand prematurely |

---

## 6️⃣ Dashboard Features
| Feature | Value |
|--------|-------|
| Year comparison (pre-COVID vs recovery) | Enables long-term trend evaluation |
| Age segmentation | Supports labour supply / workforce planning |
| Citizenship view | Tourism vs returning NZ resident patterns |
| Net movement metric | Quick proxy for migration / population change |
| Geographic heat map | Helps decide which regions warrant promotional spending |

---

## 7️⃣ Limitations & Next Steps
**Limitations**
- Dataset is aggregated; no purpose-of-trip attributes
- Does not incorporate economic or visa policy drivers

**Future Enhancements**
- Integrate labour market / visa / GDP indicators
- Add forecasting (e.g., Tableau trend lines or ML model)
- Deploy dashboard inside a business-facing web UI

---

## 8️⃣ About the Analyst
👋 **Yang Li – Data Analyst (Auckland)**  
Experienced in Tableau, SQL, Python (ETL), AWS fundamentals, business analytics, and dashboard storytelling.

---

