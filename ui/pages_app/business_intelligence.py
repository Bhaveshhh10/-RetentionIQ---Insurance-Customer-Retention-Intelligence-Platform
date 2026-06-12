"""
Page 5 — Business Intelligence
Advanced executive analytics with tabbed views covering regional analysis,
demographics, product analysis, tenure, pricing, and service quality.
"""
import streamlit as st
from utils.data_loader import load_risk_data
from ui.components.metrics import (
    render_hero_section, render_section_header, render_metric_card,
    render_info_box,
)
from ui.components.charts import (
    regional_churn_bar,
    churn_by_age_group,
    churn_by_tenure,
    churn_by_premium_change,
    policy_type_churn_bar,
    risk_treemap,
    churn_flow_sankey,
    marital_status_chart,
    complaint_impact_chart,
    payment_behavior_chart,
)


def render():
    """Render the Business Intelligence page."""
    df = load_risk_data()

    # ── Hero ──
    render_hero_section(
        title="Business Intelligence",
        subtitle="Executive-level analytics to identify churn patterns, segment risks, and uncover strategic retention opportunities.",
        badge_text="Advanced Analytics Suite",
    )

    # ── Tabs ──
    tab_regional, tab_demo, tab_product, tab_tenure, tab_pricing, tab_service = st.tabs([
        "🌍 Regional",
        "👥 Demographics",
        "📋 Product",
        "📅 Tenure",
        "💰 Pricing",
        "📞 Service",
    ])

    # ── REGIONAL TAB ──
    with tab_regional:
        render_section_header(
            "🌍 Regional Churn Analysis",
            "Compare churn risk patterns across all 7 regions",
        )

        col1, col2 = st.columns(2)
        with col1:
            fig = regional_churn_bar(df)
            st.plotly_chart(fig, use_container_width=True, key="bi_regional_bar")

        with col2:
            fig_tree = risk_treemap(df)
            st.plotly_chart(fig_tree, use_container_width=True, key="bi_treemap")

        # Regional summary table
        render_section_header("📊 Regional Summary Table")
        regional_summary = df.groupby("region_name").agg(
            customers=("Risk_Score", "size"),
            avg_risk=("Risk_Score", "mean"),
            high_risk=("Risk_Category", lambda x: (x == "High").sum()),
            avg_premium=("current_premium", "mean"),
            total_premium=("current_premium", "sum"),
        ).round(1).reset_index()
        regional_summary.columns = [
            "Region", "Customers", "Avg Risk (%)", "High Risk Count",
            "Avg Premium ($)", "Total Premium ($)",
        ]
        regional_summary = regional_summary.sort_values("Avg Risk (%)", ascending=False)

        st.dataframe(
            regional_summary,
            use_container_width=True,
            column_config={
                "Avg Risk (%)": st.column_config.ProgressColumn(
                    min_value=0, max_value=100, format="%.1f%%",
                ),
                "Avg Premium ($)": st.column_config.NumberColumn(format="$%.0f"),
                "Total Premium ($)": st.column_config.NumberColumn(format="$%.0f"),
            },
            hide_index=True,
        )

    # ── DEMOGRAPHICS TAB ──
    with tab_demo:
        render_section_header(
            "👥 Demographic Analysis",
            "How age, marital status, and demographics influence churn risk",
        )

        col1, col2 = st.columns(2)
        with col1:
            fig_age = churn_by_age_group(df)
            st.plotly_chart(fig_age, use_container_width=True, key="bi_age")

        with col2:
            fig_marital = marital_status_chart(df)
            st.plotly_chart(fig_marital, use_container_width=True, key="bi_marital")

        # Insights
        age_data = df.groupby("age_band")["Churn_Probability"].mean().sort_values(ascending=False)
        highest_age = age_data.index[0]
        lowest_age = age_data.index[-1]

        render_info_box(
            f"<strong>Key Insight:</strong> The <strong>{highest_age}</strong> age group shows the "
            f"highest average churn probability at <strong>{age_data.iloc[0]*100:.1f}%</strong>, "
            f"while the <strong>{lowest_age}</strong> group is most stable at "
            f"<strong>{age_data.iloc[-1]*100:.1f}%</strong>. "
            f"Consider age-specific retention campaigns targeting younger demographics."
        )

    # ── PRODUCT TAB ──
    with tab_product:
        render_section_header(
            "📋 Product Analysis",
            "Churn patterns across policy types and cross-sell opportunities",
        )

        col1, col2 = st.columns(2)
        with col1:
            fig_policy = policy_type_churn_bar(df)
            st.plotly_chart(fig_policy, use_container_width=True, key="bi_policy")

        with col2:
            fig_sankey = churn_flow_sankey(df)
            st.plotly_chart(fig_sankey, use_container_width=True, key="bi_sankey")

        # Multi-policy analysis
        render_section_header("🔗 Multi-Policy Impact")
        single = df[df["multi_policy_flag"] == 0]["Churn_Probability"].mean() * 100
        multi = df[df["multi_policy_flag"] == 1]["Churn_Probability"].mean() * 100

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            render_metric_card("📄", "Single Policy Churn", f"{single:.1f}%", accent="warning")
        with mc2:
            render_metric_card("📦", "Multi-Policy Churn", f"{multi:.1f}%", accent="success")
        with mc3:
            diff = single - multi
            render_metric_card(
                "📉", "Churn Reduction",
                f"{diff:.1f}pp",
                delta="Multi-policy advantage",
                delta_type="positive",
                accent="cyan",
            )

    # ── TENURE TAB ──
    with tab_tenure:
        render_section_header(
            "📅 Customer Tenure Analysis",
            "How customer longevity correlates with churn risk",
        )

        fig_tenure = churn_by_tenure(df)
        st.plotly_chart(fig_tenure, use_container_width=True, key="bi_tenure")

        # Tenure insights
        render_info_box(
            "<strong>Business Insight:</strong> Customers in their first 12 months show the highest "
            "churn risk, indicating the critical importance of onboarding experience. "
            "Long-tenured customers (120+ months) have the lowest churn rates — loyalty builds retention. "
            "Focus early-tenure engagement programs to maximize long-term value."
        )

    # ── PRICING TAB ──
    with tab_pricing:
        render_section_header(
            "💰 Pricing Impact Analysis",
            "How premium changes influence customer retention decisions",
        )

        fig_prem = churn_by_premium_change(df)
        st.plotly_chart(fig_prem, use_container_width=True, key="bi_premium")

        render_info_box(
            "<strong>Key Finding:</strong> Customers experiencing premium increases above 10% "
            "show dramatically elevated churn probability. "
            "Implementing graduated price increases (max 5% per year) could significantly reduce "
            "price-driven churn while maintaining revenue growth."
        )

        # Autopay analysis
        render_section_header("💳 Auto-Pay Impact")
        no_auto = df[df["autopay_enabled"] == 0]["Churn_Probability"].mean() * 100
        has_auto = df[df["autopay_enabled"] == 1]["Churn_Probability"].mean() * 100

        ac1, ac2 = st.columns(2)
        with ac1:
            render_metric_card("❌", "No Auto-Pay Churn", f"{no_auto:.1f}%", accent="warning")
        with ac2:
            render_metric_card("✅", "Auto-Pay Churn", f"{has_auto:.1f}%", accent="success")

    # ── SERVICE TAB ──
    with tab_service:
        render_section_header(
            "📞 Service Quality Analysis",
            "Impact of complaints, contact frequency, and service interactions on churn",
        )

        col1, col2 = st.columns(2)
        with col1:
            fig_complaint = complaint_impact_chart(df)
            st.plotly_chart(fig_complaint, use_container_width=True, key="bi_complaint")

        with col2:
            fig_payment = payment_behavior_chart(df)
            st.plotly_chart(fig_payment, use_container_width=True, key="bi_payment")

        # Quote request impact
        render_section_header("🔍 Quote Request Impact")
        no_quote = df[df["quote_requested_flag"] == 0]["Churn_Probability"].mean() * 100
        has_quote = df[df["quote_requested_flag"] == 1]["Churn_Probability"].mean() * 100

        qc1, qc2 = st.columns(2)
        with qc1:
            render_metric_card("✅", "No Quote Request", f"{no_quote:.1f}%", accent="success")
        with qc2:
            render_metric_card(
                "⚠️", "Quote Requested", f"{has_quote:.1f}%",
                delta="Actively comparing providers",
                delta_type="negative",
                accent="danger",
            )

        render_info_box(
            f"<strong>Warning:</strong> Customers who have requested competitor quotes show a churn "
            f"probability of <strong>{has_quote:.1f}%</strong> — "
            f"<strong>{has_quote - no_quote:.1f} percentage points</strong> higher than those who haven't. "
            f"Implement proactive outreach when a quote request is detected."
        )
