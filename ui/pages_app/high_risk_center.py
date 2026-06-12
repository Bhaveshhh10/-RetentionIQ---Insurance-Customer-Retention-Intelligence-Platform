"""
Page 3 — High Risk Customer Center
Dedicated retention operations page with filters, priority tiers,
interactive tables, and downloadable reports.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_risk_data
from ui.components.metrics import (
    render_hero_section, render_section_header, render_metric_card,
    render_info_box,
)


def render():
    """Render the High Risk Customer Center page."""
    df = load_risk_data()

    # ── Hero ──
    render_hero_section(
        title="High Risk Customer Center",
        subtitle="Prioritized retention operations — identify, analyze, and act on at-risk customers before they churn.",
        badge_text="Retention Operations Hub",
    )

    # ── Filters ──
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns([1, 1, 1, 1])

    with fc1:
        region_filter = st.multiselect(
            "🌍 Region",
            options=sorted(df["region_name"].unique()),
            default=[],
            placeholder="All Regions",
        )
    with fc2:
        policy_filter = st.multiselect(
            "📋 Policy Type",
            options=sorted(df["policy_type"].unique()),
            default=[],
            placeholder="All Types",
        )
    with fc3:
        risk_range = st.slider(
            "⚡ Risk Score Range",
            min_value=0,
            max_value=100,
            value=(50, 100),
            step=1,
        )
    with fc4:
        category_filter = st.multiselect(
            "🏷️ Risk Category",
            options=["High", "Medium", "Low"],
            default=["High"],
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Apply Filters ──
    filtered = df.copy()
    if region_filter:
        filtered = filtered[filtered["region_name"].isin(region_filter)]
    if policy_filter:
        filtered = filtered[filtered["policy_type"].isin(policy_filter)]
    if category_filter:
        filtered = filtered[filtered["Risk_Category"].isin(category_filter)]
    filtered = filtered[
        (filtered["Risk_Score"] >= risk_range[0]) &
        (filtered["Risk_Score"] <= risk_range[1])
    ]

    filtered = filtered.sort_values("Risk_Score", ascending=False)

    # ── Summary Metrics ──
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("👥", "Filtered Customers", f"{len(filtered):,}", accent="cyan")
    with m2:
        avg_risk = filtered["Risk_Score"].mean() if len(filtered) > 0 else 0
        render_metric_card("⚡", "Avg Risk Score", f"{avg_risk:.1f}%", accent="warning")
    with m3:
        rev_risk = filtered["current_premium"].sum() if len(filtered) > 0 else 0
        render_metric_card("💰", "Revenue at Risk", f"${rev_risk:,.0f}", accent="danger")
    with m4:
        immediate = len(filtered[filtered["Risk_Score"] >= 85]) if len(filtered) > 0 else 0
        render_metric_card("🔴", "Immediate Action", f"{immediate}", accent="danger")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Priority Tiers ──
    if len(filtered) > 0:
        tab1, tab2, tab3, tab4 = st.tabs([
            f"🔴 Immediate Action ({len(filtered[filtered['Risk_Score'] >= 85])})",
            f"🟠 Urgent Review ({len(filtered[(filtered['Risk_Score'] >= 70) & (filtered['Risk_Score'] < 85)])})",
            f"🟡 Monitor ({len(filtered[(filtered['Risk_Score'] >= 50) & (filtered['Risk_Score'] < 70)])})",
            f"📋 All Filtered ({len(filtered)})",
        ])

        display_cols = [
            "Risk_Score", "Risk_Category", "region_name", "policy_type",
            "age", "customer_tenure_months", "current_premium",
            "premium_change_pct", "late_payment_count_12m",
            "complaint_flag", "Churn_Probability", "Recommendations",
        ]

        col_config = {
            "Risk_Score": st.column_config.ProgressColumn(
                "Risk Score",
                min_value=0, max_value=100,
                format="%.1f%%",
            ),
            "Churn_Probability": st.column_config.ProgressColumn(
                "Churn Prob",
                min_value=0, max_value=1,
                format="%.1f%%",
            ),
            "current_premium": st.column_config.NumberColumn(
                "Premium",
                format="$%.2f",
            ),
            "premium_change_pct": st.column_config.NumberColumn(
                "Premium Change",
                format="%.1f%%",
            ),
            "Risk_Category": "Risk",
            "region_name": "Region",
            "policy_type": "Policy",
            "customer_tenure_months": "Tenure (months)",
            "late_payment_count_12m": "Late Payments",
            "complaint_flag": "Complaint",
        }

        with tab1:
            immediate_df = filtered[filtered["Risk_Score"] >= 85]
            if len(immediate_df) > 0:
                render_info_box(
                    f"🚨 <strong>{len(immediate_df)}</strong> customers with risk scores above 85% "
                    "require immediate retention intervention. Total revenue at risk: "
                    f"<strong>${immediate_df['current_premium'].sum():,.0f}</strong>",
                    variant="danger",
                )
                st.dataframe(
                    immediate_df[display_cols],
                    use_container_width=True,
                    column_config=col_config,
                    height=400,
                )
            else:
                st.info("No customers in this tier with current filters.")

        with tab2:
            urgent_df = filtered[(filtered["Risk_Score"] >= 70) & (filtered["Risk_Score"] < 85)]
            if len(urgent_df) > 0:
                render_info_box(
                    f"⚠️ <strong>{len(urgent_df)}</strong> customers require urgent review. "
                    f"Revenue at risk: <strong>${urgent_df['current_premium'].sum():,.0f}</strong>",
                    variant="warning",
                )
                st.dataframe(
                    urgent_df[display_cols],
                    use_container_width=True,
                    column_config=col_config,
                    height=400,
                )
            else:
                st.info("No customers in this tier with current filters.")

        with tab3:
            monitor_df = filtered[(filtered["Risk_Score"] >= 50) & (filtered["Risk_Score"] < 70)]
            if len(monitor_df) > 0:
                render_info_box(
                    f"📊 <strong>{len(monitor_df)}</strong> customers should be monitored. "
                    f"Revenue at risk: <strong>${monitor_df['current_premium'].sum():,.0f}</strong>",
                )
                st.dataframe(
                    monitor_df[display_cols],
                    use_container_width=True,
                    column_config=col_config,
                    height=400,
                )
            else:
                st.info("No customers in this tier with current filters.")

        with tab4:
            st.dataframe(
                filtered[display_cols],
                use_container_width=True,
                column_config=col_config,
                height=500,
            )

        # ── Download Section ──
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("📥 Export Report")

        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])
        with col_dl1:
            csv = filtered[display_cols].to_csv(index=False)
            st.download_button(
                "📥 Download Filtered CSV",
                data=csv,
                file_name="high_risk_customers.csv",
                mime="text/csv",
            )
        with col_dl2:
            immediate_csv = filtered[filtered["Risk_Score"] >= 85][display_cols].to_csv(index=False)
            st.download_button(
                "🔴 Download Immediate Actions",
                data=immediate_csv,
                file_name="immediate_action_customers.csv",
                mime="text/csv",
            )

    else:
        render_info_box("No customers match the selected filters. Try adjusting your criteria.", variant="warning")
