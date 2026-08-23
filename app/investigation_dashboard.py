import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(
    page_title="UAE AML Transaction Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Clean Light Lavender FinTech Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Scoped font to avoid breaking native button hitboxes */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FAF8FD;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Zero dead space at top */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 1.5rem !important;
    }

    /* Ensure entire tab container and text receive direct pointer clicks */
    [data-baseweb="tab"] {
        cursor: pointer !important;
        user-select: none !important;
    }
    [data-baseweb="tab"] * {
        pointer-events: none !important;
    }

    /* Lavender Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 50%, #E9D5FF 100%);
        border: 1px solid #D8B4FE;
        border-radius: 14px;
        padding: 24px 30px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.05);
    }
    .hero-badge {
        display: inline-block;
        background: #EDE9FE;
        color: #6D28D9;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #C4B5FD;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #3B0764;
        letter-spacing: -0.025em;
        margin: 0 0 8px 0;
        line-height: 1.25;
    }
    .hero-desc {
        color: #5B21B6;
        font-size: 0.94rem;
        line-height: 1.6;
        max-width: 980px;
        margin: 0;
    }

    /* Lavender Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E9D5FF;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.08);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6B7280;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #3B0764;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .metric-card.accent-red {
        border-left: 4px solid #E11D48;
    }
    .metric-card.accent-lavender {
        border-left: 4px solid #7C3AED;
        background: linear-gradient(90deg, #FAF5FF 0%, #FFFFFF 100%);
    }
    .metric-card.accent-amber {
        border-left: 4px solid #C084FC;
    }
    .metric-card.accent-slate {
        border-left: 4px solid #8B5CF6;
    }

    /* Card Containers */
    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #F3E8FF;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.02);
        margin-bottom: 1.25rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FAF5FF !important;
        border-right: 1px solid #E9D5FF;
    }
    .sidebar-card {
        background: #FFFFFF;
        border: 1px solid #E9D5FF;
        border-radius: 10px;
        padding: 15px;
        margin-top: 14px;
        box-shadow: 0 1px 4px rgba(124, 58, 237, 0.04);
    }
    .sidebar-card a {
        color: #7C3AED !important;
        text-decoration: none;
        font-weight: 600;
    }
    .sidebar-card a:hover {
        text-decoration: underline;
    }

    /* Isolated Network Container */
    .network-container {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E9D5FF;
        background: #FFFFFF;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Lavender-aligned visualization color palette
PALETTE = {
    'Low': '#A78BFA',       # Soft Lavender Purple
    'Medium': '#7C3AED',    # Vibrant Violet
    'High': '#4C1D95',      # Deep Imperial Plum
    'P1': '#9F1239',        # Rose/Wine Alert
    'P2': '#7C3AED',        # Violet
    'P3': '#C084FC',        # Light Wisteria
    'Line': '#6D28D9',      # Deep Violet Line
    'Marker': '#3B0764'     # Dark Plum
}

CHART_LAYOUT = dict(
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#4B5563'),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=30, b=20, l=20, r=20),
    hoverlabel=dict(bgcolor="#3B0764", font_color="#FFFFFF", font_family="Plus Jakarta Sans")
)

tab1, tab2 = st.tabs(["Live Dashboard", "Methodology & Findings"])

with tab1:
    with st.sidebar:
        st.markdown("""
        <div style="display: inline-block; background: #EDE9FE; color: #6D28D9; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 6px; border: 1px solid #C4B5FD; margin-bottom: 8px;">
            Compliance Surveillance
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### System Scope")
        st.write(
            "A synthetic AML transaction monitoring system demonstrating customer risk rating, "
            "deterministic typology detection (structuring, rapid movement, layering), peer-group "
            "behavioral anomaly detection, and alert triage -built on a synthetic dataset modeling "
            "UAE retail, SME, and corporate banking activity."
        )
        
        st.markdown("""
        <div class="sidebar-card">
            <div style="font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #6B7280; margin-bottom: 4px;">System Architect</div>
            <div style="font-weight: 700; color: #3B0764; font-size: 0.95rem;">Albin M Jose</div>
            <div style="margin-top: 8px; font-size: 0.85rem;">
                🔗 <a href="https://www.linkedin.com/in/albin-mj" target="_blank">LinkedIn Profile</a><br>
                💻 <a href="https://github.com/albin-m-jose/aml-transaction-monitoring-uae" target="_blank">GitHub Repository</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-card" style="border-left: 3px solid #7C3AED; background: #FAF5FF;">
            <div style="font-weight: 700; color: #6D28D9; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 4px;">Methodology Note</div>
            <div style="font-size: 0.82rem; line-height: 1.5; color: #4B5563;">
                All detection rules were designed from AML typology reasoning first. Ground truth labels were used exclusively for post-hoc validation, never as design input.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">Surveillance & Intelligence Engine</div>
        <div class="hero-title">UAE AML Transaction Monitoring — Investigation Dashboard</div>
        <div class="hero-desc">
            This dashboard simulates how a bank's compliance team monitors customer transactions for signs of money laundering. 
            It combines a customer risk rating model, rule-based detection of known laundering patterns, and behavioral anomaly detection 
            into a single prioritized alert queue -the kind of tool an AML analyst would use to decide what to investigate first.
        </div>
    </div>
    """, unsafe_allow_html=True)

    DATA_DIR = '../data'

    triage = pd.read_csv(f'{DATA_DIR}/triage_queue.csv')
    alerts = pd.read_csv(f'{DATA_DIR}/unified_alerts.csv')
    risk_profiles = pd.read_csv(f'{DATA_DIR}/customer_risk_profiles.csv')

    alerts['alert_date'] = pd.to_datetime(
        alerts['window_start'].fillna(alerts['inflow_timestamp']).fillna(alerts['hop1_timestamp']),
        format='mixed'
    )
    alerts['alert_month'] = alerts['alert_date'].dt.to_period('M').astype(str)

    monthly_alert_counts = alerts.groupby('alert_month').size().sort_index()
    if len(monthly_alert_counts) >= 2:
        last_month_count = monthly_alert_counts.iloc[-1]
        prev_month_count = monthly_alert_counts.iloc[-2]
        delta = int(last_month_count - prev_month_count)
    else:
        last_month_count = monthly_alert_counts.iloc[-1] if len(monthly_alert_counts) else 0
        delta = None

    p1_count = (triage['triage_tier'] == 'P1 - Critical').sum()

    # Executive Summary Cards
    st.markdown("#### Executive Summary")
    st.caption("Monitoring coverage overview and active investigation caseload.")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="metric-card accent-slate">
            <div class="metric-label">Total Customers Monitored</div>
            <div class="metric-val">{len(risk_profiles):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="metric-card accent-lavender">
            <div class="metric-label">Total Alerts Generated</div>
            <div class="metric-val">{len(alerts):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="metric-card accent-amber">
            <div class="metric-label">Under Investigation</div>
            <div class="metric-val">{len(triage):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="metric-card accent-red">
            <div class="metric-label">P1 Critical Escalations</div>
            <div class="metric-val" style="color: #9F1239;">{p1_count:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Customer Risk & Case Priority")
        st.write(
            "Every customer is rated Low, Medium, or High risk based on a combination of onboarding "
            "information and observed transaction behavior (see Phase 2 of the methodology). "
            "Customers who also triggered a specific detection rule are further sorted into a "
            "priority queue -P1 being the most urgent."
        )

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Customer Risk Tier Distribution**")
            crr_counts = risk_profiles['crr_tier'].value_counts().reset_index()
            crr_counts.columns = ['Risk Tier', 'Count']
            fig1 = px.pie(
                crr_counts,
                names='Risk Tier',
                values='Count',
                color='Risk Tier',
                color_discrete_map={'Low': PALETTE['Low'], 'Medium': PALETTE['Medium'], 'High': PALETTE['High']},
                hole=0.52
            )
            fig1.update_layout(**CHART_LAYOUT)
            fig1.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            st.markdown("**Triage Tier Distribution**")
            tier_counts = triage['triage_tier'].value_counts().reset_index()
            tier_counts.columns = ['Triage Tier', 'Count']
            fig2 = px.bar(
                tier_counts,
                x='Triage Tier',
                y='Count',
                color='Triage Tier',
                color_discrete_map={'P1 - Critical': PALETTE['P1'], 'P2 - High': PALETTE['P2'], 'P3 - Standard': PALETTE['P3']}
            )
            fig2.update_layout(**CHART_LAYOUT)
            fig2.update_layout(
                xaxis_title="",
                yaxis_title="Customer Count",
                showlegend=False,
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='#F3E8FF')
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Monthly Alert Trend")
        st.write(
            "Tracks how many alerts were generated each month across all detection rules. A rising "
            "trend can reflect genuine increases in suspicious activity, seasonal effects, or "
            "detection rules becoming more sensitive -worth investigating either way."
        )

        trend_col1, trend_col2 = st.columns([3, 1])

        with trend_col1:
            trend_df = monthly_alert_counts.reset_index()
            trend_df.columns = ['Month', 'Alert Count']
            fig3 = px.line(trend_df, x='Month', y='Alert Count', markers=True)
            fig3.update_traces(
                line_color=PALETTE['Line'],
                line_width=3,
                marker=dict(size=8, color=PALETTE['Marker'])
            )
            fig3.update_layout(**CHART_LAYOUT)
            fig3.update_layout(
                xaxis_title="Surveillance Period",
                yaxis_title="Generated Alerts",
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='#F3E8FF')
            )
            st.plotly_chart(fig3, use_container_width=True)

        with trend_col2:
            st.markdown("**Latest Period Summary**")
            delta_str = f"{delta:+d} vs prior month" if delta is not None else "Baseline period"
            st.markdown(f"""
            <div style="background: #FAF5FF; border: 1px solid #E9D5FF; border-radius: 10px; padding: 20px; text-align: center; margin-top: 15px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #6D28D9; text-transform: uppercase;">
                    {monthly_alert_counts.index[-1] if len(monthly_alert_counts) else 'Current Month'}
                </div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #3B0764; margin: 6px 0;">
                    {int(last_month_count)}
                </div>
                <div style="font-size: 0.82rem; font-weight: 600; color: {'#9F1239' if (delta or 0) > 0 else '#6D28D9'};">
                    {delta_str}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Alert Triage Queue")
        st.write(
            "Every customer who triggered at least one detection rule, ranked by a combined "
            "priority score (rule severity + risk rating + behavioral anomaly signals). Use the "
            "filters below to focus on specific tiers."
        )

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            tier_filter = st.multiselect(
                "Filter by Triage Tier",
                options=triage['triage_tier'].unique(),
                default=triage['triage_tier'].unique()
            )

        with filter_col2:
            crr_filter = st.multiselect(
                "Filter by CRR Tier",
                options=triage['crr_tier'].dropna().unique(),
                default=triage['crr_tier'].dropna().unique()
            )

        filtered_triage = triage[
            (triage['triage_tier'].isin(tier_filter)) &
            (triage['crr_tier'].isin(crr_filter))
        ]

        st.caption(f"Showing {len(filtered_triage)} of {len(triage)} customers")
        st.dataframe(
            filtered_triage.sort_values('priority_score', ascending=False),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Layering Chain Network Topology")
        st.write(
            "Layering is a laundering technique where funds are moved through several intermediary "
            "accounts to obscure their origin before reaching a final destination. The graph below "
            "shows every layering chain this system detected, tracing money from a source account, "
            "through one or two intermediary accounts, to an offshore destination. Hover over any "
            "node or connection for transaction details."
        )

        try:
            with open('../notebooks/layering_network.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.markdown('<div class="network-container">', unsafe_allow_html=True)
            components.html(html_content, height=750, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("Layering network visualization file not found. Run the Phase 3 notebook to generate it.")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Customer 360 — Investigation Profile")
        st.write(
            "Select any customer from the priority queue to see their full risk profile, alert "
            "history, and whether independent behavioral analysis corroborates the alert -the "
            "kind of consolidated view an analyst would pull up before deciding on next steps."
        )

        sorted_customers = triage.sort_values('priority_score', ascending=False)['customer_id'].tolist()
        selected_customer = st.selectbox(
            "Select a Customer ID to Investigate",
            options=sorted_customers
        )

        if selected_customer:
            cust_risk = risk_profiles[risk_profiles['customer_id'] == selected_customer].iloc[0]
            cust_triage = triage[triage['customer_id'] == selected_customer].iloc[0]
            cust_alerts = alerts[alerts['customer_id'] == selected_customer]

            st.markdown(f"#### Entity: `{selected_customer}` — Segment: **{cust_risk['segment'].title()}**")

            detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
            detail_col1.metric("CRR Tier", cust_risk['crr_tier'])
            detail_col2.metric("Composite CRR Score", f"{cust_risk['composite_crr']:.3f}")
            detail_col3.metric("Triage Priority", cust_triage['triage_tier'])
            detail_col4.metric("Number of Alerts", cust_triage['num_triggers'])

            if cust_triage['anomaly_same_month']:
                st.warning("Corroborating Signal: Customer was independently flagged by peer-group behavioral anomaly detection in the same month as an alert.")
            else:
                st.info("Notice: No same-month behavioral anomaly overlap detected for this customer.")

            st.write("**Alert History**")
            st.dataframe(cust_alerts, use_container_width=True, hide_index=True)


with tab2:
    st.header("Project Methodology, Design Decisions & Limitations")

    st.markdown("""
### Why This Project Exists

Most AML portfolio projects apply a generic machine learning model to a labeled dataset and then report an accuracy score. I wanted to do something a little different.

Instead of treating AML as a simple classification problem, I wanted to build something that feels more like how a real financial institution would actually approach transaction monitoring. There are different types of risk, different detection methods, different levels of alerts, and at the end of all of this, an analyst still has to sit down and decide which customer is actually worth investigating.

So this project is basically my attempt to build that entire pipeline step by step.

---

### Phase 1: Data Validation & Exploration

Before doing any actual modeling, I wanted to make sure I understood the data properly. I asked a friend who works in AML to create a synthetic dataset for me. All the analysis was done on this dataset. We discussed the scope of the project, and he wrote the code to generate the data. Because this is synthetic data, it comes with its own set of caveats, which I'll discuss along the way.

The dataset contains 10,000 customers, 11,937 accounts, and around 5.7 million transactions. I checked the relationships between the different tables and made sure the data was joining together the way I expected.

I was also very careful about the ground truth. The dataset contains deliberately injected AML scenarios, but I didn't want to use those labels to build my detection rules -that would make the results look artificially good. Instead, I treated the ground truth as something to check against at the very end to see if my logic worked, rather than using it as an input while designing the logic.

One of the most important things I found during EDA was that income and transaction amounts were heavily right-skewed. They followed something much closer to a lognormal distribution than a normal distribution. This became crucial later, because it meant simply calculating a standard deviation across the entire population wasn't going to make sense. I ended up using percentile-based approaches and peer group comparisons instead.

---

### Phase 2: Customer Risk Rating (CRR)

Every customer comes with some level of risk. The important thing for a financial institution is deciding whether a customer is worth the risk and, more importantly, how much attention that customer deserves.

For this, I split customer risk into two parts:

* **Static Risk:** Information that doesn't change very often, such as KYC rating, customer segment, and industry.
* **Dynamic Risk:** Looking at what the customer is actually doing with their money over time.

While building the static risk model, I explored joining the customer table with the accounts table to count how many accounts each customer holds, assuming more accounts might mean higher risk. But after looking at it, I chose not to include it. I couldn't find a clear relationship between a high number of accounts and higher AML risk in the data, and any weight I would assign to it would be negligible. It didn't make sense to add a feature just for the sake of having it.

I did, however, join the customer table with the employer table to bring in the customer's industry. This made immediate sense from an AML perspective -someone working in a government entity carries a very different baseline risk compared to someone working in precious metals, currency exchange, or casinos.

For the dynamic model, I used one of my favorite statistical concepts: **standard deviation** (which basically measures how much a value deviates from what's expected). I created several ratios and rolling metrics -such as **cash intensity, high-risk jurisdiction exposure, and spend-to-income velocity** -and measured how much each customer deviated from their expected profile.

I combined the static and dynamic components using a **30% static / 70% dynamic** weighting. I chose this balance because I don't want the risk rating to rely primarily on information collected when the account was first opened. If someone's actual financial behavior changes significantly, that should have a much bigger impact on their score.

When I finally validated the scores against the ground truth, customers involved in the injected AML scenarios had an average composite CRR of **0.42** compared to **0.25** for the general population -around **67% higher**, even though the model never saw those ground truth labels during design.

---

### Phase 3: Deterministic Typology Detection

At this point I had a way to answer: *"How risky does this customer look?"*

But that isn't quite the same question as: *"Is this customer actually doing something suspicious right now?"*

To answer that, I built deterministic rules for three classic AML typologies:

* **Structuring / Smurfing (94% recall, 100% precision):** Detected multiple sub-threshold cash deposits that individually stay below reporting limits but collectively exceed them within rolling 1-day and 7-day windows.
* **Rapid Movement (59.6% recall, 96.7% precision):** Looked for large inflows followed by almost all the money leaving again within 24 hours. Rather than picking an arbitrary dollar threshold, I used each customer's own historical transaction baseline.
* **Layering (42% recall, 100% precision):** Detected money moving through multiple hops (A → B → C → offshore destination) using graph traversal, visualized via the interactive network graph in Tab 1.

I also built **False Positive Suppression** logic. An alert shouldn't automatically disappear just because there is a legitimate explanation (like a customer receiving a large loan and immediately routing it to a property purchase). Instead of deleting the alert, the system downgrades it while preserving the full rationale in an audit trail.

---

### Phase 4: Peer-Group Behavioral Anomaly Detection

Next, I wanted to answer: *"Is this customer behaving unusually compared to people who are actually similar to them?"*

A large corporate account moving millions every month is normal; a retail customer doing the same is not. I created peer groups based on customer segment (and industry for retail clients) and scored customer-month activity across transaction volume, velocity, and counterparty entropy.

Because Phase 1 showed the distributions were heavily right-skewed, I log-transformed these variables and calculated z-scores *within each peer group* rather than across the entire customer base.

This produced a completely different signal from the typology rules, showing an 11%–20% overlap with ground truth. That is expected: the whole point of this layer is to catch novel, unmodeled behavioral outliers that don't fit into the three hardcoded typology rules.

---

### Phase 5: Alert Scoring & Triage

Now I had multiple signals telling me different things: some customers had high CRRs, some had typology alerts, and some looked anomalous compared to their peers. But banks have finite compliance resources and cannot investigate every alert with equal urgency.

To solve this, I built a weighted composite priority score:

$$\\text{Base Priority} = (0.50 \\times \\text{Alert Severity}) + (0.35 \\times \\text{Composite CRR}) + (0.15 \\times \\text{Same-Month Anomaly})$$

* **Alert Severity (50%):** The strongest immediate operational signal that something specific happened.
* **Customer Risk Rating (35%):** Customer context matters -a high-risk customer triggering an alert warrants faster review than a low-risk customer triggering the same rule.
* **Peer Anomaly Co-occurrence (15%):** An unusual month alone might not mean much, but if it happens alongside an active typology alert, it acts as valuable corroborating evidence.

#### Multi-Typology Corroboration Boost
What happens if all three alert types (Structuring, Rapid Movement, and Layering) trigger for the same customer? Having three independent detection mechanisms all flag the same entity indicates a significantly elevated risk.

When all three distinct alert types fire for a customer, the score receives a **3% boost**:

$$\\text{Final Priority Score} = \\text{Base Priority} \\times 1.03$$

I deliberately kept this boost small so it wouldn't distort the baseline scoring, while still acknowledging that multi-signal agreement is meaningful. I also focused specifically on **distinct alert types** rather than raw alert count, avoiding situations where multiple rolling-window triggers from a single rule artificially inflate a customer's priority.

---

### Known Limitations

I think it's important to document limitations clearly rather than pretend a model is flawless:

* **30-Day Structuring Ceiling:** The synthetic data generator capped scenario injections below the 8-deposit threshold required for the 30-day rule to fire. This was a dataset generation ceiling rather than a logic error.
* **Layering Recall:** Roughly half of the missed layering chains traced to currency conversion handling in how the generator passed amounts across non-AED accounts.
* **Suppression Testing:** The suppression logic is implemented and works, but wasn't exercised against genuine overlapping scenarios because the synthetic False Positive and Rapid Movement generators ran independently.
* **Anomaly Validation:** Comparing the peer anomaly layer against ground truth is a proxy check because the synthetic labels only mark specific typologies, not generic behavioral anomalies.
* **Corroboration Boost:** The 3% boost is an operational business decision, not a statistically calibrated probability.

---

### A Note on Methodology

Throughout this project, my approach has been: **design the logic from AML principles first, then evaluate against ground truth.**

I avoided tweaking thresholds after the fact just to produce prettier precision and recall metrics. When something didn't perform as expected, I traced the root cause -whether it was the rule threshold, an artifact of the data generator, or a detection layer doing its intended job of finding unmodeled behavior.

The goal wasn't just to maximize an accuracy metric on a synthetic dataset; it was to build a transparent, explainable monitoring pipeline where every risk score, alert trigger, suppression decision, and prioritization rank can be clearly defended.
""")