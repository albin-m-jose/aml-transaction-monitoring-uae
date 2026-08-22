
# AML Transaction Monitoring and Customer Risk Analytics Project

This project builds an end to end AML monitoring framework using a synthetic banking dataset. The approach starts with data validation and understanding the structure of the data, followed by customer risk scoring, deterministic AML detection rules, and peer group based anomaly detection.

A key principle followed throughout the project is that detection logic is designed using AML and statistical reasoning first. The known ground truth is used only afterward to validate the results and is not used to design or tune the rules to artificially improve performance.

---

## Phase 1: EDA, Schema Validation and Entity Linkages

Loaded and validated the full synthetic dataset containing 10,000 customers, 11,937 accounts and 5.7 million transactions before starting the analysis. I treated data validation as an important first step rather than assuming the data was already correct.

- Built a complete data dictionary across all 7 tables, documenting the columns, data types and their meaning from an AML perspective. This included separating static onboarding information from dynamic behavioural information and creating a clear understanding of the data used throughout the project.

- Verified the relationships between customers, accounts, transactions and ground truth data. There were no orphaned records, and I also documented expected data characteristics such as around 2% missing KYC ratings and transactions without a resolvable counterparty where this was expected by design.

- Established the role of the ground truth early in the project. It identifies the small number of deliberately injected AML scenarios, including Structuring, Rapid Movement, Layering and legitimate False Positives. I used it only for validating the results after building the detection logic and never as an input when designing the rules or risk model.

- Compared expected monthly outflow based on customer information against actual transaction activity. This provided an initial descriptive baseline for understanding customer behaviour and identifying differences between declared and observed activity.

- Examined the distribution of income and transaction amounts and found that they were right skewed and closer to a lognormal distribution than a normal distribution. This influenced later decisions to use percentile based and within segment comparisons instead of relying on raw z scores.

---

## Phase 2: Customer Risk Rating CRR Engine

Designed and built a composite Customer Risk Rating model that combines both static onboarding information and dynamic transaction behaviour. The final scores were grouped into standard Low, Medium and High risk tiers to support different levels of customer due diligence.

- **Static risk** included customer segment, KYC risk rating, multi currency account exposure and employer industry. Missing KYC ratings were treated conservatively as High risk rather than being assigned a neutral value.

- **Dynamic risk** included cash intensity, exposure to high risk jurisdictions, offshore transaction ratio and a velocity ratio comparing actual outflow against declared income. These measures were calculated using appropriate segment specific and self referential baselines to avoid unfairly comparing structurally different customers such as retail, SME and corporate customers.

- Combined the static and dynamic scores into a single composite CRR using a weighting of **30% static and 70% dynamic**. I gave more weight to dynamic risk because this is intended to be a continuously monitored risk rating rather than a score based only on customer information collected during onboarding. Customers were then grouped into Low risk, Medium risk and High risk, broadly corresponding to SDD, CDD and EDD levels.

- **Risk drift analysis** showed that 45.6% of customers had current behaviour that justified a higher risk tier than their original KYC rating. This is useful from a compliance perspective because these customers can be prioritised for periodic KYC reviews or possible EDD.

- **Ground truth validation** was performed only after the model was completed. Customers involved in the injected AML scenarios had an average composite CRR almost **67% higher** than the general population, with average scores of **0.42 compared to 0.25** and minimal overlap between the distributions. This provides strong evidence that the model was able to identify higher risk customers using AML based risk factors without using the known scenario labels during its design.

---

## Phase 3: Deterministic Detection Rules

Built and validated the core AML detection rules against the transaction dataset. I designed the rules based on AML typologies and detection logic first, and only checked the results against the known ground truth afterward. I did not adjust the rules based on the results to artificially improve performance.

- **Structuring/Smurfing detection** using two severity tiers with 1-day and 7-day rolling windows achieved **94% recall and 100% precision** against the known structuring cases. The rules successfully identified customers splitting large cash deposits into multiple smaller transactions below the reporting threshold.

- **Rapid Movement detection** for funnel and pass-through account behaviour achieved **96.7% precision and 59.6% recall**. The logic uses each customer's own transaction history as a baseline, which avoids directly comparing customers with very different transaction sizes and behaviour.

- **Layering chain detection** for multi-hop fund movement through intermediary accounts achieved **100% precision and 42% recall**. The detected fund movements were also visualized using an interactive network graph to show how funds moved between accounts and eventually reached external destinations.

- **False Positive Suppression logic** was designed and implemented to downgrade alerts where there is a clear legitimate explanation, such as a loan disbursement followed by a property purchase. Suppressed alerts are retained with the reason recorded rather than being deleted, maintaining a full audit trail.

- Two genuine **data limitations** were identified during validation. One was a synthetic data generation limit affecting a structuring tier, and the other was a currency conversion issue affecting some layering chains. Both were investigated, traced to their root cause and documented rather than changing the rules to improve the results artificially.

- A total of **366 alerts** were consolidated into a single unified alert table. This will be used as the input for **Phase 4: Peer Group Anomaly Detection** and **Phase 5: Alert Triage and Prioritization**.

---

## Phase 4: Peer Group Statistical Anomaly Detection

Built a behavioural anomaly detection layer that compares each customer's monthly activity against similar customers within a defined peer group. This was designed as a complementary detection method alongside the Customer Risk Rating model and the typology specific rules, with the aim of identifying unusual behaviour that may not match any predefined AML scenario.

- **Peer group definition:** Customer segment was used as the primary grouping, with retail, SME and corporate customers compared mainly against others in the same segment. Industry was used as an additional level of grouping for retail customers where the information was available. SME and corporate customers were grouped by segment only because this dataset does not contain industry classifications for them. This is a dataset limitation rather than a design issue.

- **Behavioural dimensions:** The anomaly score combines three monthly behavioural measures: transaction volume, transaction count or velocity, and counterparty entropy. Counterparty entropy measures how concentrated or spread out a customer's transactions are across different counterparties. This adds another dimension beyond volume and transaction count, as a customer can have high transaction activity with one regular counterparty or spread similar activity across many different counterparties.

- **Log transformed z score approach:** Transaction volume and transaction count were heavily right skewed, as identified during Phase 1, so both were log transformed before calculating z scores. Counterparty entropy was z scored directly because it is already a bounded metric. A log transform was initially applied to entropy as well, but this caused distortion at the lower end of the distribution and was identified and corrected during development.

- **Anomaly threshold:** The 97.5th percentile of the composite anomaly score was used as the threshold for flagging unusual customer months. This resulted in **1,013 unique customers** being flagged across **3,000 customer months**.

- **Peer group size limitation:** Smaller peer groups, particularly SME and corporate customers, produced a disproportionately high number of extreme z scores. This happens because smaller groups provide less stable estimates of the mean and standard deviation, which can produce more extreme scores. This was documented as a statistical limitation and does not necessarily mean SME or corporate customers are genuinely more anomalous.

- **Low activity bias:** The composite score was more likely to flag unusually low activity, such as dormant or suddenly quiet accounts, rather than unusually high activity. This is a different type of behaviour from the high value transaction patterns represented by the injected AML scenarios in the ground truth data.

- **Ground truth validation:** The anomaly detection results were compared against customers involved in the known injected AML scenarios. This resulted in **11.4% precision and 19.8% recall**, with 115 of the 580 scenario involved customers also being identified among the anomaly flagged population. This validation should be interpreted carefully because the ground truth contains no separate label for general behavioural anomalies. The comparison is therefore a proxy check to see whether the method captures known scenario customers, rather than a direct precision and recall test against a matching anomaly label.

- **CRR comparison:** The anomaly flagged customers were also compared against the High CRR population from Phase 2. A total of **81 out of 707 High CRR customers, or 11.5%**, were also flagged by the peer anomaly detection model. This shows a modest overlap between the independently calculated customer risk rating and the anomaly detection results.

- **Overall interpretation:** The validation results were weaker than the typology specific detection rules in Phase 3, but this is expected because this layer is designed to detect a different type of behaviour. Instead of looking for specific patterns such as Structuring, Rapid Movement or Layering, it identifies customers whose transaction volume, activity level or counterparty behaviour differs significantly from similar customers. The ground truth scenarios were deliberately generated around specific AML typologies, so overlap with this broader anomaly detection approach cannot fully measure its usefulness.

Overall, Phase 4 acts as an additional safety net alongside the Customer Risk Rating model in Phase 2 and the deterministic AML detection rules in Phase 3. Its main value is in identifying unusual or potentially new behavioural patterns that existing rules were not specifically designed to detect, rather than replacing the existing risk scoring or typology based detection methods.

### Phase 5 Summary: Alert Scoring, Prioritization and Triage

Combined the outputs from Phase 2, customer risk ratings, Phase 3, typology detection alerts, and Phase 4, peer anomaly detection, into a single customer level triage table. The aim was to address alert fatigue, where a large number of alerts and limited analyst capacity require a clear and defensible way to decide which customers should be investigated first.

**Methodology:**

* 220 unique customers with at least one Phase 3 alert were combined into one row per customer. The table captures trigger count, distinct alert types, highest alert severity, CRR tier, and same month anomaly co occurrence from Phase 4.

* A weighted priority score combined alert severity at 50 percent, customer CRR at 35 percent, and anomaly co occurrence at 15 percent. Alert severity received the highest weight because a direct match to a specific detection rule is the strongest evidence, while CRR and anomaly signals provide additional risk context.

* A trigger diversity boost was added for customers flagged by multiple distinct detection rules. This corrected an initial design flaw where using the total alert count unfairly favored Structuring, since its rolling window logic can naturally generate multiple alerts from the same underlying pattern. Using distinct alert types instead better rewards customers with supporting signals from different detection rules.

* Customers were assigned to P1 Critical, P2 High, and P3 Standard tiers using the 85th and 50th percentile cutoffs of the final priority score. This follows the same data driven threshold approach used throughout the project.

**Validation and limitations:**

The ground truth True and False label was not useful for directly validating the ranking. This is because all customers in the triage table had already triggered a Phase 3 detection rule, and most were already true positive cases regardless of their priority tier.

A second check looked at the number of distinct ground truth scenario types linked to each customer. This showed only a weak difference between higher and lower priority tiers. The main reason was a limitation of the synthetic dataset, where scenarios were mostly generated as independent and self contained events. Very few customers were involved in multiple scenario types, leaving limited variation for this test.

The more meaningful validation was therefore checking whether the scoring logic behaved as intended. P3 mainly isolates customers with single, lower severity Structuring alerts, while P1 contains a more balanced mix of alert types. This is expected because the final score does not depend on severity alone. It combines severity with customer risk rating and behavioral anomaly context, allowing customers with multiple supporting risk signals to rank higher even when their individual alert type is not the most severe.

The final output from this phase is the prioritized customer alert queue used directly in Phase 6 to power the Streamlit investigation dashboard.
