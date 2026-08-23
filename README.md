# UAE AML Transaction Monitoring System

**🔗 Live Dashboard:** [https://albin-aml-project.streamlit.app/](https://albin-aml-project.streamlit.app/)

An end-to-end Anti-Money Laundering (AML) transaction monitoring system built to demonstrate
real-world compliance analytics — customer risk rating, deterministic typology detection,
peer-group behavioral anomaly detection, and alert triage — on a synthetic dataset modeling
UAE retail, SME, and corporate banking activity.

This project was built to reflect how a real bank's transaction monitoring function actually
works: layered, risk-aware, and built around analyst workflow, rather than a single black-box
model reporting an accuracy score.

## What This Project Demonstrates

- Understanding of core AML typologies (structuring/smurfing, rapid movement/pass-through,
  layering) and how to translate regulatory red flags into detection logic
- A risk-based approach to customer due diligence (CDD/EDD), combining static onboarding data
  with dynamic transaction behavior
- Statistically sound handling of real-world data characteristics (right-skewed distributions,
  peer-group comparison, self-normalizing baselines)
- Honest, rigorous validation methodology — every detection rule was designed from AML domain
  reasoning first and validated against ground truth only afterward, never the reverse
- The operational reality of alert triage and false positive suppression, addressing
  "alert fatigue," a widely cited pain point in real compliance teams
- End-to-end delivery: from raw data through analysis to a deployed, interactive dashboard

## Live Dashboard

**[https://albin-aml-project.streamlit.app/](https://albin-aml-project.streamlit.app/)**

The dashboard includes:
- An executive summary with key monitoring metrics
- Customer risk tier and alert triage distribution charts
- A monthly alert trend view
- A filterable, sortable alert triage queue
- An interactive network graph visualizing detected layering chains
- A Customer 360 investigation view
- A full methodology & findings tab documenting every design decision and known limitation

## Project Structure
aml-transaction-monitoring-uae/
├── app/
│ └── investigation_dashboard.py # Streamlit dashboard
├── data/ # Synthetic datasets + processed outputs
├── notebooks/
│ ├── 00_synthetic_data_generator.ipynb
│ ├── 01_eda_and_data_quality.ipynb
│ ├── 02_customer_risk_scoring.ipynb
│ ├── 03_detection_rules.ipynb
│ ├── 04_peer_comparison.ipynb
│ ├── 05_alert_triage_metrics.ipynb
│ └── layering_network.html
├── reports/
│ └── executive_summary.md # Phase-by-phase written summary
├── requirements.txt
└── README.md


## Methodology & Results Summary

### Phase 1 — Data Validation & Exploration
Validated referential integrity across all 7 synthetic tables (10,000 customers, 11,937
accounts, 5.7M transactions). Established that income and transaction amounts are right-skewed
(lognormal), which shaped every later statistical decision in the project toward percentile-
and peer-group-based comparisons rather than raw z-scores on the full population.

### Phase 2 — Customer Risk Rating (CRR) Engine
Built a composite risk score (30% static onboarding factors / 70% dynamic behavioral factors),
mapped to Low/Medium/High (SDD/CDD/EDD) tiers. Customers involved in ground-truth AML scenarios
scored **67% higher on average** (0.42 vs. 0.25) than the general population — despite the
model never seeing those labels during design. Risk drift analysis found 45.6% of customers
show behavior warranting a higher tier than their original KYC rating.

### Phase 3 — Deterministic Typology Detection
| Typology | Recall | Precision |
|---|---|---|
| Structuring/Smurfing | 94.0% | 100.0% |
| Rapid Movement (funnel accounts) | 59.6% | 96.7% |
| Layering (multi-hop chains) | 42.0% | 100.0% |

Detection logic was designed from AML typology reasoning first, then validated against ground
truth. Two genuine data limitations were identified, root-caused, and documented rather than
tuned around: a synthetic data generation ceiling affecting one structuring severity tier, and
a currency-conversion artifact affecting a subset of layering chains. False Positive
Suppression logic was also implemented to correctly downgrade alerts with a legitimate
explanation (e.g. loan-funded property purchases), preserving a full audit trail.

### Phase 4 — Peer-Group Statistical Anomaly Detection
A complementary layer scoring customer-months against peer norms across transaction volume,
velocity, and counterparty entropy. Deliberately designed to catch different, previously-
unmodeled behavior rather than replicate the typology rules above — validated with a modest,
honestly-reported overlap against ground truth (11–20%), consistent with its intended role as
a broader safety net rather than a precision instrument.

### Phase 5 — Alert Scoring & Triage
Combined all prior signals into a single weighted priority score (50% alert severity, 35%
customer risk rating, 15% behavioral anomaly co-occurrence), tiered into P1/P2/P3 triage
categories. During development, a real design flaw was identified and corrected: an initial
trigger-count boost unintentionally rewarded repetitive alerts from a single rule over genuine
corroboration across multiple different rules.

### Phase 6 — Investigation Dashboard
All outputs delivered as a live, interactive Streamlit dashboard — see link above.

Full phase-by-phase writeup: [`reports/executive_summary.md`](reports/executive_summary.md)

## Tech Stack

- **Python** — pandas, numpy for data processing
- **NetworkX / PyVis** — layering chain graph construction and visualization
- **Plotly** — dashboard charts
- **Streamlit** — interactive dashboard, deployed on Streamlit Community Cloud
- **Jupyter Notebooks** — phase-by-phase analysis

## Data

The dataset is fully synthetic, generated via `notebooks/00_synthetic_data_generator.ipynb`,
simulating 10,000 customers across retail, SME, and corporate segments with deliberately
injected AML typology scenarios (structuring, rapid movement, layering, and legitimate false
positives) for validation purposes. No real customer data is used anywhere in this project.

## Running Locally

```bash
git clone https://github.com/albin-m-jose/aml-transaction-monitoring-uae.git
cd aml-transaction-monitoring-uae
pip install -r requirements.txt
streamlit run app/investigation_dashboard.py
```

## Known Limitations

Documented in full in the dashboard's "Methodology & Findings" tab and in
`reports/executive_summary.md`. Briefly: the 30-day structuring detection tier could not be
exercised due to a synthetic data generation ceiling; a currency-conversion artifact in the
data generator affected roughly half of missed layering chains; False Positive Suppression
logic is implemented and correct but was never exercised against a genuine overlapping case in
this dataset; peer anomaly detection's ground truth validation is a proxy check rather than a
direct precision/recall comparison.

## Author

**Albin M Jose**
[LinkedIn] (https://www.linkedin.com/in/albin-mj/) · [GitHub](https://github.com/albin-m-jose)