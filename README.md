# UAE AML Transaction Monitoring System

An end-to-end Anti-Money Laundering (AML) transaction monitoring and triage engine aligned with UAE regulatory frameworks (Central Bank of the UAE / CBUAE & FIU goAML guidelines).

## Project Structure

```text
aml-transaction-monitoring-uae/
├── .gitignore
├── README.md
├── requirements.txt
├── data/                            # Synthetic transaction & customer datasets (Git-ignored)
├── src/                             # Core Python analytical engines
│   ├── __init__.py
│   ├── data_loader.py               # Ingestion, validation, and schema standardization
│   ├── risk_engine.py               # Dynamic Customer Risk Rating (CRR)
│   ├── rules_engine.py              # Rule-based typologies (Structuring, Velocity, Corridors)
│   ├── peer_analyzer.py             # Peer group anomaly detection
│   ├── network_detector.py          # Layering & graph/network community detection
│   └── alert_manager.py             # Alert scoring, deduplication, and triage
├── notebooks/                       # Exploratory & validation notebooks (01 to 06)
├── app/
│   └── investigation_dashboard.py   # Streamlit alert triage dashboard
└── reports/
    └── executive_summary.md         # Typology breakdown & executive findings
