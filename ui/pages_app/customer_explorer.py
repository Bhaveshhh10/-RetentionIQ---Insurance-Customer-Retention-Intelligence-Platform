"""
Page 2 — Customer Explorer
Advanced customer intelligence page with individual customer profiling,
risk gauge, SHAP-based explainability, and retention recommendations.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import load_risk_data, load_model, compute_clv
from utils.shap_engine import get_customer_shap
from ui.components.metrics import (
    render_hero_section, render_section_header, render_metric_card,
    render_risk_badge, render_profile_card, render_recommendation_cards,
    render_info_box, clean_html,
)
from ui.components.charts import risk_gauge, shap_waterfall_chart


def render():
    """Render the Customer Explorer page."""
    df = load_risk_data()
    model = load_model()

    # ── Hero ──
    render_hero_section(
        title="Customer Explorer",
        subtitle="Deep-dive into individual customer profiles with AI-powered risk explanations and retention strategies.",
    )

    # ── Customer Selector ──
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col_filter, col_search = st.columns([1, 2])
    with col_filter:
        risk_filter = st.selectbox(
            "Filter by Risk",
            ["All", "High", "Medium", "Low"],
            index=0,
        )

    # Filter dataframe for search list
    filtered_df = df.copy()
    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["Risk_Category"] == risk_filter]

    with col_search:
        # Create a display-friendly customer list
        customer_options = []
        customer_indices = []
        for idx in filtered_df.index:
            row = filtered_df.loc[idx]
            label = f"Customer #{idx} — {row['region_name']} | {row['policy_type']} | Risk: {row['Risk_Score']:.0f}%"
            customer_options.append(label)
            customer_indices.append(idx)

        if len(customer_options) > 0:
            selected_label = st.selectbox(
                "🔍 Search & Select Customer",
                customer_options,
                index=0,
            )
            customer_idx = customer_indices[customer_options.index(selected_label)]
            customer_positional_idx = df.index.get_loc(customer_idx)
        else:
            st.error("No customers found matching the filter.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

    st.markdown('</div>', unsafe_allow_html=True)

    customer = df.loc[customer_idx]

    # ── Customer Profile Row ──
    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        render_section_header("👤 Customer Profile")
        render_profile_card([
            ("Age", f"{customer['age']} years ({customer['age_band']})"),
            ("Region", customer['region_name']),
            ("Marital Status", customer['marital_status']),
            ("Tenure", f"{customer['customer_tenure_months']} months"),
            ("Policy Type", customer['policy_type']),
            ("Policies", f"{customer['num_policies']}"),
            ("Payment", customer['payment_frequency']),
            ("Auto-Pay", "✅ Enabled" if customer['autopay_enabled'] else "❌ Disabled"),
        ])

    with c2:
        render_section_header("⚡ Risk Assessment")
        fig_gauge = risk_gauge(
            customer["Risk_Score"],
            customer["Risk_Category"],
        )
        st.plotly_chart(fig_gauge, use_container_width=True, key="risk_gauge")
        render_risk_badge(customer["Risk_Category"])

        # CLV
        clv = compute_clv(customer)
        st.markdown(clean_html(f"""
        <div style="margin-top: 16px; padding: 14px 18px;
                    background: rgba(59, 130, 246, 0.08);
                    border: 1px solid rgba(59, 130, 246, 0.15);
                    border-radius: 12px;">
            <div style="font-size: 12px; color: #64748b; text-transform: uppercase;
                        letter-spacing: 0.05em; font-weight: 600;">
                Estimated Lifetime Value
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #f8fafc; margin-top: 4px;">
                ${clv:,.0f}
            </div>
            <div style="font-size: 12px; color: #64748b; margin-top: 2px;">
                Churn Probability: {customer['Churn_Probability'] * 100:.1f}%
            </div>
        </div>
        """), unsafe_allow_html=True)

    with c3:
        render_section_header("💰 Financial Summary")
        render_profile_card([
            ("Current Premium", f"${customer['current_premium']:,.2f}"),
            ("Last Year Premium", f"${customer['premium_last_year']:,.2f}"),
            ("Premium Change", f"{customer['premium_change_pct'] * 100:.1f}%"),
            ("Coverage Amount", f"${customer['coverage_amount']:,.0f}"),
            ("Claims (12m)", f"{customer['num_claims_12m']}"),
            ("Approved Claims", f"{customer['num_approved_claims_12m']}"),
            ("Total Payout", f"${customer['total_payout_amount_12m']:,.0f}"),
            ("Late Payments", f"{customer['late_payment_count_12m']}"),
        ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SHAP Analysis & Recommendations ──
    tab1, tab2, tab3 = st.tabs([
        "🧠 Why Is This Customer At Risk?",
        "📊 Risk Driver Details",
        "🎯 Retention Recommendations",
    ])

    with tab1:
        with st.spinner("Computing SHAP explanations..."):
            try:
                shap_dict, base_value = get_customer_shap(customer_positional_idx, model, df)

                col_shap, col_drivers = st.columns([3, 2])
                with col_shap:
                    fig_shap = shap_waterfall_chart(shap_dict, top_n=12)
                    st.plotly_chart(fig_shap, use_container_width=True, key="shap_waterfall")

                with col_drivers:
                    render_section_header("Top Risk Drivers")

                    # Split into positive (risk-increasing) and negative (risk-decreasing)
                    sorted_features = sorted(shap_dict.items(), key=lambda x: x[1], reverse=True)
                    positive = [(k, v) for k, v in sorted_features if v > 0][:5]
                    negative = [(k, v) for k, v in sorted_features if v < 0][-5:]

                    if positive:
                        st.markdown(clean_html("""
                        <div style="font-size: 13px; font-weight: 600; color: #ef4444;
                                    margin-bottom: 8px; text-transform: uppercase;
                                    letter-spacing: 0.05em;">
                            ⬆️ Increasing Risk
                        </div>
                        """), unsafe_allow_html=True)
                        for name, val in positive:
                            pct = abs(val) / max(abs(v) for _, v in sorted_features) * 100
                            st.markdown(clean_html(f"""
                            <div style="margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between;
                                            margin-bottom: 3px;">
                                    <span style="font-size: 12px; color: #94a3b8;">{name}</span>
                                    <span style="font-size: 12px; color: #ef4444; font-weight: 600;">
                                        +{val:.4f}
                                    </span>
                                </div>
                                <div style="background: rgba(239,68,68,0.1); border-radius: 4px;
                                            height: 6px; overflow: hidden;">
                                    <div style="background: #ef4444; height: 100%;
                                                 width: {pct:.0f}%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            """), unsafe_allow_html=True)

                    if negative:
                        st.markdown(clean_html("""
                        <div style="font-size: 13px; font-weight: 600; color: #10b981;
                                    margin: 16px 0 8px 0; text-transform: uppercase;
                                    letter-spacing: 0.05em;">
                            ⬇️ Reducing Risk
                        </div>
                        """), unsafe_allow_html=True)
                        for name, val in negative:
                            pct = abs(val) / max(abs(v) for _, v in sorted_features) * 100
                            st.markdown(clean_html(f"""
                            <div style="margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between;
                                            margin-bottom: 3px;">
                                    <span style="font-size: 12px; color: #94a3b8;">{name}</span>
                                    <span style="font-size: 12px; color: #10b981; font-weight: 600;">
                                        {val:.4f}
                                    </span>
                                </div>
                                <div style="background: rgba(16,185,129,0.1); border-radius: 4px;
                                            height: 6px; overflow: hidden;">
                                    <div style="background: #10b981; height: 100%;
                                                 width: {pct:.0f}%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            """), unsafe_allow_html=True)

            except Exception as e:
                render_info_box(
                    f"⚠️ SHAP analysis could not be computed for this customer. Error: {str(e)}",
                    variant="warning",
                )

    with tab2:
        render_section_header("📋 Complete Risk Factor Analysis")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Pricing Factors**")
            render_profile_card([
                ("Premium Change", f"{customer['premium_change_pct'] * 100:.1f}%"),
                ("Price Increases (3yr)", f"{customer['num_price_increases_last_3y']}"),
                ("Premium/Coverage Ratio", f"{customer['premium_to_coverage_ratio']:.4f}"),
                ("Coverage Downgrade", "Yes" if customer['coverage_downgrade_flag'] else "No"),
            ])

        with col_b:
            st.markdown("**Engagement Factors**")
            render_profile_card([
                ("Customer Contacts (12m)", f"{customer['num_contacts_12m']}"),
                ("Has Complaint", "Yes ⚠️" if customer['complaint_flag'] else "No ✅"),
                ("Complaint Resolution (days)", f"{customer['complaint_resolution_days']}"),
                ("Quote Requested", "Yes ⚠️" if customer['quote_requested_flag'] else "No"),
            ])

    with tab3:
        render_section_header("🎯 AI-Generated Retention Recommendations")
        render_info_box(
            "These recommendations are generated by our retention engine based on the customer's "
            "risk profile, behavioral patterns, and policy characteristics."
        )
        render_recommendation_cards(customer["Recommendations"])
