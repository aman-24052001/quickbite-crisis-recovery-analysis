# QuickBite Express — Crisis Recovery Analysis

[![Dashboard](https://img.shields.io/badge/Live_Dashboard-View_Here-FFE500?style=for-the-badge&logo=html5&logoColor=black)](https://aman-24052001.github.io/quickbite-crisis-recovery-analysis/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Challenge](https://img.shields.io/badge/Codebasics-RPC_%2318-4A90E2?style=flat-square)](https://codebasics.io)

> **Codebasics Resume Project Challenge #18** — Intermediate · Food & Beverages · Strategy

---

## Problem Statement

QuickBite Express is a Bengaluru-based food delivery startup (founded 2020). In **June 2025**, a viral food safety incident combined with a week-long monsoon delivery outage triggered a platform-wide crisis:

- Daily orders fell **63%** overnight
- Customer satisfaction collapsed from **4.5★ → 2.3★**
- **87.8% of the active customer base disengaged**
- Partner restaurants began migrating to competitors

The management allocated a recovery budget and overhauled food safety protocols. **This analysis quantifies the true scale of the crisis, identifies what isn't working in recovery, and builds a prioritised, ROI-backed roadmap to restore pre-crisis performance.**

---

## Dataset

| Table | Rows | Description |
|-------|------|-------------|
| `fact_orders` | 149,166 | Orders Jan–Sep 2025 with amounts, timestamps, cancellation status |
| `fact_order_items` | 342,994 | Line-item detail per order |
| `fact_ratings` | 68,842 | Customer ratings and review text with sentiment scores |
| `fact_delivery_performance` | 149,166 | Actual vs expected delivery times, distance |
| `dim_customer` | 107,776 | Signup date, city, acquisition channel |
| `dim_restaurant` | 19,995 | Cuisine type, partner type, prep time, active flag |
| `dim_delivery_partner` | 15,000 | Vehicle type, employment, avg rating |
| `dim_menu_item` | 342,671 | Menu items with category, veg flag, price |

**Period:** January 2025 – September 2025 · **8 cities** (Bengaluru, Mumbai, Delhi, Chennai, Hyderabad, Pune, Ahmedabad, Kolkata)

**Phase definitions used in this analysis:**

| Phase | Period | Orders |
|-------|--------|--------|
| Pre-Crisis | Jan–May 2025 | 113,806 |
| Crisis | Jun 2025 | 9,293 |
| Recovery | Jul–Sep 2025 | 26,067 |

---

## Key Findings

### 1. Recovery is not recovering
Orders and revenue plateaued at ~8,600/month from July through September — showing no improvement trend. This is structural loss, not temporary churn.

```
Pre-Crisis avg:  22,761 orders/month  ·  ₹75.2L revenue/month
Recovery avg:     8,689 orders/month  ·  ₹26.8L revenue/month
Gap:             −63%                  ·  −₹48.4L/month persisting
```

### 2. Delivery infrastructure is still broken
The "infrastructure overhaul" management announced has not shown up in data through September 2025.

| Metric | Pre-Crisis | Recovery | Change |
|--------|-----------|----------|--------|
| Avg delivery time | 39.5 min | 60.0 min | **+52%** |
| SLA breach rate | 56.4% | 87.7% | **+31 pp** |
| Cancellation rate | 6.1% | 12.1% | **+2×** |

### 3. Loyalty was wiped out uniformly
RFM segmentation of 86,824 pre-crisis customers reveals all segments returned at near-identical ~12% rate. Champions (highest LTV) came back at 11.9% — same as Lost customers at 12.3%. The crisis erased loyalty advantage entirely.

### 4. Sentiment is getting worse, not better
Average rating fell from **2.63★ (Crisis)** to **2.31★ (September)** — the lowest month on record. Recovery sentiment score: −0.27 vs crisis −0.19. Customers who stayed are more frustrated than those who left.

### 5. VIP customers represent the highest-ROI recovery target
- 4,342 VIP customers (top 5% by spend) averaged ₹1,128 pre-crisis spend
- Only 519 (12%) returned — 3,823 VIPs still lost
- Monthly VIP revenue: ₹9.9L pre-crisis → ₹60K now (**−94%**)
- Recovering 25% of lost VIPs = **+₹2.16L/month**

### 6. Data quality bug found
**4,867 churned restaurants are still flagged `is_active = "Y"`** in `dim_restaurant` despite placing zero orders in recovery. This inflates active partner counts in management reporting.

### 7. Keyword analysis reveals unresolved product failures
Top complaints in negative reviews (rating < 3): Quality (2,226), Issue (2,073), Packaging (1,627), Safety (1,076), Stale (971), Late (904). Every complaint category grew 2.7–3.2× from Crisis to Recovery — confirming food quality and safety issues are unresolved.

---

## Analysis Modules

```
analysis/
├── 01_phase_overview.py        # Revenue, orders, cancellation by phase
├── 02_customer_retention.py    # Cohort retention, pre→crisis→recovery flow
├── 03_rfm_segmentation.py      # RFM scoring + segment recovery rates
├── 04_delivery_performance.py  # SLA breach, delivery time trends
├── 05_restaurant_analysis.py   # Churn by cuisine, data quality check
├── 06_sentiment_keywords.py    # Review text frequency analysis
├── 07_vip_segment.py           # Top 5% spender deep-dive
└── 08_roi_model.py             # Recovery budget + scenario modelling
```

---

## Dashboard

An **interactive 8-tab HTML dashboard** built with Chart.js — open `dashboard/quickbite_recovery_dashboard.html` in any browser, no server required.

| Tab | Content |
|-----|---------|
| Overview | KPI cards, monthly orders/revenue/customers trend |
| Customers | RFM segmentation, retention funnel, acquisition channel |
| Delivery | SLA breach, delivery time, cancellation trends |
| Restaurants | Cuisine churn, data quality alert |
| Sentiment | Rating trends, distribution shifts |
| Keywords | Review text frequency — negative vs positive by phase |
| VIP Segment | Top 5% spender analysis, scenario modelling |
| ROI Model | 4-pillar investment plan, revenue projection, reactivation scenarios |
| Recommendations | 8 prioritised actions with targets and owners |

---

## Recommendations Summary

| Priority | Action | Target | Timeline |
|----------|--------|--------|----------|
| 🔴 Urgent | Fix delivery routing — 60 min → ≤45 min | SLA breach ≤65%, cancel ≤8% | Immediate |
| 🔴 Urgent | Fix `is_active` data quality (4,867 restaurants) | Accurate ops reporting | Immediate |
| 🟡 High | VIP win-back campaign (₹200 credit + priority SLA) | 25% return = +₹2.16L/mo | Month 1–2 |
| 🟡 High | Champion reactivation (24,783 customers) | 25% return = +₹7.3L/mo | Month 1–3 |
| 🟡 High | Restaurant re-onboarding — North Indian + Biryani first | Recover 2,000+ partners | Month 2–5 |
| 🔵 Medium | Shift acquisition: Paid (41%) → Referral | Lower CAC, higher retention | Month 2–4 |
| 🔵 Medium | Publish FSSAI audit scores in-app | Safety mentions ↓, trust ↑ | Month 1–3 |
| 🟢 Long | North Star metric: 30,000 MAU by Mar 2026 | Currently 8,479 MAU | Mar 2026 |

**Critical sequencing:** Fix delivery first → Fix food safety → Then reactivate customers. Running win-back campaigns before fixing 60-min delivery produces immediate re-churn.

---

## ROI Model

| Pillar | Investment | Expected Output | ROI |
|--------|-----------|-----------------|-----|
| VIP Win-Back | ₹8–10L | +₹2.16L/month (956 customers) | ~3× in 6mo |
| Champion Reactivation | ₹15–20L | +₹7.3L/month (6,195 customers) | ~4× in 9mo |
| Delivery Infrastructure | ₹25–30L | Cancel 12%→8%, Rating 2.3→3.5★ | Enabler |
| Restaurant Re-onboarding | ₹10–15L | +2,000 partners restored | Supply-side |
| Food Safety Certification | ₹8–12L | Safety mentions ↓, brand moat | Prevents recurrence |
| **Total** | **₹66–87L** | **₹47L+/month by Month 9** | **2.5–3×** |

---

## Tech Stack

```
Language:      Python 3.12
Analysis:      pandas · numpy
Visualisation: Chart.js (dashboard) · HTML/CSS (no frameworks)
Environment:   Jupyter-compatible scripts
Data format:   CSV (8 tables, star schema)
```

---

## How to Run

```bash
git clone https://github.com/aman-24052001/quickbite-crisis-recovery-analysis
cd quickbite-crisis-recovery-analysis

pip install pandas numpy

# Run any analysis module
python analysis/01_phase_overview.py

# Open dashboard (no server needed)
open dashboard/quickbite_recovery_dashboard.html
```

---

## Project Structure

```
quickbite-crisis-recovery-analysis/
├── README.md
├── dashboard/
│   └── quickbite_recovery_dashboard.html   # Interactive 8-tab dashboard
├── analysis/
│   ├── 01_phase_overview.py
│   ├── 02_customer_retention.py
│   ├── 03_rfm_segmentation.py
│   ├── 04_delivery_performance.py
│   ├── 05_restaurant_analysis.py
│   ├── 06_sentiment_keywords.py
│   ├── 07_vip_segment.py
│   └── 08_roi_model.py
└── data/
    └── README.md                           # Data not included (Codebasics IP)
```

> **Note:** Raw datasets are not included as they are property of Codebasics. Download them from the [RPC #18 challenge page](https://codebasics.io/challenge/codebasics-resume-project-challenge).

---

## About

**Aman Kumar** · ML Engineer · [github.com/aman-24052001](https://github.com/aman-24052001) · [LinkedIn](https://www.linkedin.com/in/aman-kumar-0863351b4)

This project was completed as part of **Codebasics Resume Project Challenge #18**. The analysis goes beyond the provided primary/secondary questions to surface a data quality issue, perform keyword sentiment extraction, build a VIP segment model, and construct a financially-grounded ROI roadmap — intended to demonstrate what a production-grade data analyst would deliver, not just a challenge submission.
