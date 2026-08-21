## Phase 3: Deterministic Detection Rules

Built and validated three core AML detection typologies against the transaction dataset,
using a strict methodology of designing rules from regulatory/typology reasoning first,
then checking results against ground truth only afterward — never the reverse.

- **Structuring/Smurfing detection** (two severity tiers: 1-day and 7-day rolling windows)
  achieved **94% recall and 100% precision** against known structuring cases — successfully
  identifying customers splitting large cash deposits into smaller sub-threshold transactions.
- **Rapid Movement detection** (funnel/pass-through accounts) achieved 96.7% precision and
  59.6% recall, using a self-normalizing baseline that compares each customer's inflows only
  against their own transaction history — avoiding unfair comparison across customer segments.
- **Layering chain detection** (multi-hop fund movement through intermediary accounts to
  offshore destinations) achieved 100% precision and 42% recall, visualized as an interactive
  network graph showing fund flow across accounts to jurisdictions including BVI, Cayman
  Islands, Panama, and Seychelles.
- **False Positive Suppression logic** was designed and implemented to correctly downgrade
  alerts triggered by legitimate large transactions (e.g. loan-funded property purchases),
  preserving a full audit trail rather than silently deleting flagged activity.
- Two genuine data limitations were identified through rigorous validation rather than masked:
  a synthetic data generation ceiling limiting one structuring tier, and a currency-conversion
  artifact affecting a subset of layering chains — both diagnosed to root cause and documented
  transparently rather than tuned around to inflate results.
- All alerts consolidated into a single 366-record unified alert table, feeding directly into
  Phase 4 (peer-group anomaly detection) and Phase 5 (alert triage and prioritization).