import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Insurance Retention Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
    return pd.read_csv("customer_risk_scores.csv")

df = load_data()
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.metric-card {
    background: linear-gradient(
        135deg,
        #1e293b,
        #0f172a
    );

    padding: 20px;

    border-radius: 15px;

    border: 1px solid #334155;

    text-align: center;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #38bdf8;
}

.metric-label {
    font-size: 16px;
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------

st.markdown("""
# 🛡️ Insurance Customer Retention Intelligence Platform

### AI-Powered Churn Analytics & Retention Recommendations

Identify high-risk customers before they leave and take proactive retention actions.
""")

# -------------------------
# SIDEBAR
# -------------------------

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Overview",
        "Customer Explorer",
        "High Risk Customers"
    ]
)

st.sidebar.markdown("---")

st.sidebar.title(
    "🛡️ Retention Intelligence"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### Platform Features

    ✅ Churn Prediction

    ✅ Risk Scoring

    ✅ Retention Recommendations

    ✅ Customer Analytics

    ✅ Explainable AI
    """
)

# ==================================================
# OVERVIEW PAGE
# ==================================================

if page == "Overview":

    total_customers = len(df)

    high_risk = len(
        df[df["Risk_Category"] == "High"]
    )

    medium_risk = len(
        df[df["Risk_Category"] == "Medium"]
    )

    low_risk = (
        total_customers
        - high_risk
        - medium_risk
    )

    avg_risk = round(
        df["Risk_Score"].mean(),
        2
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{total_customers}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Risk</div>
            <div class="metric-value">{high_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Medium Risk</div>
            <div class="metric-value">
                    {medium_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Low Risk</div>
            <div class="metric-value">{low_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Risk</div>
            <div class="metric-value">{avg_risk}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ROC-AUC</div>
            <div class="metric-value">0.785</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        risk_counts = (
            df["Risk_Category"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Category",
            "Count"
        ]

        fig = px.pie(
            risk_counts,
            names="Risk Category",
            values="Count",
            hole=0.65,
            title="Customer Risk Distribution",
            color="Risk Category",
            color_discrete_map={
                "High":"#ef4444",
                "Medium":"#f59e0b",
                "Low":"#22c55e"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig2 = px.histogram(
            df,
            x="Risk_Score",
            nbins=30,
            title="Risk Score Distribution"
        )

        fig2.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ==================================================
# CUSTOMER EXPLORER PAGE
# ==================================================

elif page == "Customer Explorer":

    st.markdown(
    "## 👤 Customer Explorer"
)

    customer_index = st.selectbox(
        "Select Customer",
        df.index
    )

    customer = df.loc[customer_index]

    col1, col2, col3 = st.columns(3)

    # -------------------------
    # CUSTOMER PROFILE
    # -------------------------

    with col1:

        st.write("### Customer Profile")

        st.write(
            f"**Age:** {customer['age']}"
        )

        st.write(
            f"**Region:** {customer['region_name']}"
        )

        st.write(
            f"**Policy Type:** {customer['policy_type']}"
        )

        st.write(
            f"**Tenure:** {customer['customer_tenure_months']} months"
        )

        st.write(
            f"**Policies:** {customer['num_policies']}"
        )

    # -------------------------
    # RISK ANALYSIS
    # -------------------------

    with col2:

        st.write("### Risk Analysis")

        st.metric(
            "Risk Score",
            f"{customer['Risk_Score']:.2f}%"
        )

        risk = customer["Risk_Category"]

        if risk == "High":
            st.error("🔴 HIGH RISK")

        elif risk == "Medium":
            st.warning("🟡 MEDIUM RISK")

        else:
            st.success("🟢 LOW RISK")

    # -------------------------
    # RISK DRIVERS
    # -------------------------

    with col3:

        st.write("### Risk Drivers")

        st.write(
            f"Premium Change: {customer['premium_change_pct']:.2f}"
        )

        st.write(
            f"Late Payments: {customer['late_payment_count_12m']}"
        )

        st.write(
            f"Complaints: {customer['complaint_flag']}"
        )

        st.write(
            f"Quote Requested: {customer['quote_requested_flag']}"
        )

    st.divider()

    # -------------------------
    # RECOMMENDATIONS
    # -------------------------

    st.subheader(
        "🎯 Retention Recommendations"
    )

    recommendations = str(
        customer["Recommendations"]
    )

    recommendations = (
        recommendations
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )

    for rec in recommendations.split(","):

        rec = rec.strip()

        if rec:
            st.markdown(
                f"✅ {rec}"
            )

# ==================================================
# HIGH RISK PAGE
# ==================================================

elif page == "High Risk Customers":

    st.subheader(
        "🚨 High Risk Customers"
    )

    high_risk_df = df[
        df["Risk_Category"] == "High"
    ].sort_values(
        by="Risk_Score",
        ascending=False
    )

    st.dataframe(
        high_risk_df[
            [
                "Risk_Score",
                "policy_type",
                "age",
                "customer_tenure_months",
                "Recommendations"
            ]
        ],
        use_container_width=True
    )