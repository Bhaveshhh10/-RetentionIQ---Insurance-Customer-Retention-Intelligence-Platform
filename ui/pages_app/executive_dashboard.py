"""
Page 1 — Executive Dashboard
The primary overview page with portfolio health score, KPI metrics,
and six analysis charts covering risk distribution, regional analysis,
policy type analysis, premium impact, complaints, and payment behavior.
"""
import streamlit as st
from utils.data_loader import load_risk_data, compute_portfolio_metrics
from ui.components.metrics import render_metric_card, render_hero_section, render_section_header
from ui.components.charts import (
    risk_distribution_donut,
    regional_churn_bar,
    policy_type_churn_bar,
    premium_impact_scatter,
    complaint_impact_chart,
    payment_behavior_chart,
)


def render():
    """Render the Executive Dashboard page."""
    df = load_risk_data()
    metrics = compute_portfolio_metrics(df)

    # ── Hero Section ──
    render_hero_section(
        title="Executive Dashboard",
        subtitle="Real-time portfolio health monitoring and churn risk analytics across 10,000 insurance customers.",
        badge_text=f"Portfolio Health: {metrics['health_score']}%",
    )

    # ── KPI Metrics Row ──
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        render_metric_card(
            "📊", "Portfolio Health",
            f"{metrics['health_score']}%",
            accent="cyan",
        )
    with c2:
        render_metric_card(
            "🚨", "High Risk",
            f"{metrics['high_risk']:,}",
            delta=f"{metrics['high_risk'] / metrics['total_customers'] * 100:.1f}% of portfolio",
            delta_type="negative",
            accent="danger",
        )
    with c3:
        render_metric_card(
            "📉", "Churn Rate",
            f"{metrics['churn_rate']}%",
            accent="warning",
        )
    with c4:
        render_metric_card(
            "💰", "Revenue at Risk",
            f"${metrics['revenue_at_risk']:,.0f}",
            delta="High-risk customer premiums",
            delta_type="neutral",
            accent="danger",
        )
    with c5:
        render_metric_card(
            "📊", "Predicted Loss",
            f"${metrics['predicted_loss']:,.0f}",
            delta="Annual expected loss",
            delta_type="negative",
            accent="warning",
        )
    with c6:
        render_metric_card(
            "🧠", "Model Confidence",
            f"{metrics['model_confidence']}%",
            delta="ROC-AUC Score",
            delta_type="positive",
            accent="success",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row 1 ──
    render_section_header(
        "📊 Risk Analytics",
        "Comprehensive analysis of customer risk distribution and regional patterns",
    )

    col1, col2 = st.columns(2)
    with col1:
        fig1 = risk_distribution_donut(df)
        st.plotly_chart(fig1, use_container_width=True, key="risk_donut")
    with col2:
        fig2 = regional_churn_bar(df)
        st.plotly_chart(fig2, use_container_width=True, key="regional_bar")

    # ── Charts Row 2 ──
    col3, col4 = st.columns(2)
    with col3:
        fig3 = policy_type_churn_bar(df)
        st.plotly_chart(fig3, use_container_width=True, key="policy_bar")
    with col4:
        fig4 = premium_impact_scatter(df)
        st.plotly_chart(fig4, use_container_width=True, key="premium_scatter")

    # ── Charts Row 3 ──
    render_section_header(
        "🔍 Behavioral Drivers",
        "How customer behavior patterns correlate with churn probability",
    )

    col5, col6 = st.columns(2)
    with col5:
        fig5 = complaint_impact_chart(df)
        st.plotly_chart(fig5, use_container_width=True, key="complaint_chart")
    with col6:
        fig6 = payment_behavior_chart(df)
        st.plotly_chart(fig6, use_container_width=True, key="payment_chart")
