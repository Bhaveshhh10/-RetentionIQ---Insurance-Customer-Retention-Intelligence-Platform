"""
Page 6 — Retention Strategy Simulator ⭐
THE STANDOUT FEATURE — allows users to configure retention strategies,
re-runs the actual XGBoost model with modified features, and shows
real impact predictions, ROI analysis, and customer-level outcomes.
"""
import streamlit as st
import numpy as np
from utils.data_loader import load_risk_data, load_model
from utils.retention_engine import simulate_retention_strategy
from ui.components.metrics import (
    render_hero_section, render_section_header, render_metric_card,
    render_info_box, render_impact_card, clean_html,
)
from ui.components.charts import before_after_distribution, roi_breakdown_chart


def render():
    """Render the Retention Strategy Simulator page."""
    df = load_risk_data()
    model = load_model()

    # ── Hero ──
    render_hero_section(
        title="Retention Strategy Simulator",
        subtitle="Configure retention strategies and see their predicted impact on churn, revenue, and ROI — powered by the actual XGBoost model.",
        badge_text="Interactive What-If Analysis",
    )

    render_info_box(
        "💡 <strong>How it works:</strong> This simulator modifies customer features based on your strategy "
        "choices and re-runs predictions through the trained XGBoost model. The results show the actual "
        "predicted impact — not estimates or heuristics. This is the feature that separates prediction from "
        "<strong>actionable intelligence</strong>."
    )

    # ── Strategy Configuration ──
    col_config, col_results = st.columns([2, 3])

    with col_config:
        render_section_header("⚙️ Configure Strategy")

        # Target segment selector
        st.markdown("""
        <div style="font-size: 13px; font-weight: 600; color: #64748b;
                    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
            Target Segment
        </div>
        """, unsafe_allow_html=True)

        target_segment = st.selectbox(
            "Target",
            ["High Risk Only", "High + Medium Risk", "Top 100 Highest Risk", "All Customers"],
            index=0,
            label_visibility="collapsed",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Strategy 1: Premium Discount
        st.markdown(clean_html("""
        <div class="strategy-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 24px;">💰</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #f8fafc;">Premium Discount</div>
                    <div style="font-size: 12px; color: #64748b;">Reduce premium to retain price-sensitive customers</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        premium_discount = st.slider(
            "Premium Discount %",
            min_value=0, max_value=25, value=0, step=1,
            format="%d%%",
            help="Percentage discount on current premium",
        )

        # Strategy 2: Flexible Payment
        st.markdown(clean_html("""
        <div class="strategy-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 24px;">📋</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #f8fafc;">Flexible Payment Plan</div>
                    <div style="font-size: 12px; color: #64748b;">Enable auto-pay & monthly billing flexibility</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        flexible_payment = st.toggle("Enable Flexible Payment Plan", value=False)

        # Strategy 3: Multi-Policy Bundle
        st.markdown(clean_html("""
        <div class="strategy-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 24px;">📦</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #f8fafc;">Multi-Policy Bundle</div>
                    <div style="font-size: 12px; color: #64748b;">Discount for bundling multiple policy types</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        bundle_discount = st.slider(
            "Bundle Discount %",
            min_value=0, max_value=15, value=0, step=1,
            format="%d%%",
            help="Percentage discount for multi-policy bundles",
        )

        # Strategy 4: Dedicated Support
        st.markdown(clean_html("""
        <div class="strategy-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 24px;">🤝</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #f8fafc;">Dedicated Support Specialist</div>
                    <div style="font-size: 12px; color: #64748b;">Assign a personal account manager for complaints</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        dedicated_support = st.toggle("Enable Dedicated Support", value=False)

        any_strategy = (premium_discount > 0 or flexible_payment or
                       bundle_discount > 0 or dedicated_support)

        # Live-updating status indicator
        if any_strategy:
            st.markdown(clean_html("""
            <div style="background: rgba(6, 182, 212, 0.08);
                        border: 1px solid rgba(6, 182, 212, 0.15);
                        border-radius: 12px;
                        padding: 12px 16px;
                        font-size: 13px;
                        color: #06b6d4;
                        font-weight: 500;
                        display: flex;
                        align-items: center;
                        gap: 8px;">
                <span class="animate-pulse">⚡</span> Live Predicting: Results are updating in real-time.
            </div>
            """), unsafe_allow_html=True)
        else:
            st.markdown(clean_html("""
            <div style="background: rgba(100, 116, 139, 0.08);
                        border: 1px solid rgba(100, 116, 139, 0.15);
                        border-radius: 12px;
                        padding: 12px 16px;
                        font-size: 13px;
                        color: #64748b;
                        font-weight: 500;">
                ⚙️ Adjust parameters above to start simulation.
            </div>
            """), unsafe_allow_html=True)

    # ── Results Panel ──
    with col_results:
        if any_strategy:
            with st.spinner("🧠 Running simulation through XGBoost model..."):
                results = simulate_retention_strategy(
                    df=df,
                    model=model,
                    premium_discount_pct=premium_discount,
                    enable_flexible_payment=flexible_payment,
                    multi_policy_discount_pct=bundle_discount,
                    enable_dedicated_support=dedicated_support,
                    target_segment=target_segment,
                )

            if results["target_count"] > 0:
                # ── Impact KPIs ──
                render_section_header("📊 Simulation Results")

                r1, r2, r3, r4 = st.columns(4)
                with r1:
                    render_impact_card(
                        "Customers Saved",
                        f"{results['customers_saved']:,}",
                        variant="positive",
                    )
                with r2:
                    render_impact_card(
                        "Revenue Retained (Annual)",
                        f"${results['revenue_saved_annual']:,.0f}",
                        variant="positive",
                    )
                with r3:
                    render_impact_card(
                        "Campaign Cost",
                        f"${results['campaign_cost']:,.0f}",
                        variant="warning",
                    )
                with r4:
                    roi_color = "positive" if results["roi"] > 0 else "warning"
                    render_impact_card(
                        "ROI",
                        f"{results['roi']:,.0f}%",
                        variant=roi_color,
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # Additional metrics row
                r5, r6, r7 = st.columns(3)
                with r5:
                    render_impact_card(
                        "Lifetime Revenue Saved",
                        f"${results['revenue_saved_lifetime']:,.0f}",
                        variant="positive",
                    )
                with r6:
                    render_impact_card(
                        "Avg Churn Reduction",
                        f"{results['avg_prob_reduction'] * 100:.1f}pp",
                        variant="neutral",
                    )
                with r7:
                    render_impact_card(
                        "Customers Targeted",
                        f"{results['target_count']:,}",
                        variant="neutral",
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Before/After Distribution Chart ──
                if len(results["original_probs"]) > 0:
                    fig_dist = before_after_distribution(
                        results["original_probs"],
                        results["new_probs"],
                    )
                    st.plotly_chart(fig_dist, use_container_width=True, key="before_after")

                # ── ROI Breakdown ──
                fig_roi = roi_breakdown_chart(results)
                st.plotly_chart(fig_roi, use_container_width=True, key="roi_breakdown")

                # ── Customer-Level Impact Table ──
                render_section_header("📋 Customer-Level Impact")

                detail = results["customer_detail"]
                st.dataframe(
                    detail.head(50),
                    use_container_width=True,
                    column_config={
                        "Risk_Score": st.column_config.ProgressColumn(
                            "Risk Score", min_value=0, max_value=100, format="%.0f%%",
                        ),
                        "Original_Churn_Prob": st.column_config.NumberColumn(
                            "Before (%)", format="%.1f%%",
                        ),
                        "New_Churn_Prob": st.column_config.NumberColumn(
                            "After (%)", format="%.1f%%",
                        ),
                        "Prob_Reduction": st.column_config.NumberColumn(
                            "Reduction (pp)", format="%.1f",
                        ),
                        "current_premium": st.column_config.NumberColumn(
                            "Premium", format="$%.0f",
                        ),
                    },
                    height=400,
                )

                # ── Executive Summary ──
                render_section_header("📝 Executive Summary")

                strategies_used = []
                if premium_discount > 0:
                    strategies_used.append(f"{premium_discount}% premium discount")
                if flexible_payment:
                    strategies_used.append("flexible payment plans")
                if bundle_discount > 0:
                    strategies_used.append(f"{bundle_discount}% multi-policy bundle discount")
                if dedicated_support:
                    strategies_used.append("dedicated support specialists")

                strategy_text = ", ".join(strategies_used)

                net_benefit = results['revenue_saved_lifetime'] - results['campaign_cost']

                st.markdown(clean_html(f"""
                <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.08), rgba(59, 130, 246, 0.04));
                            border: 1px solid rgba(6, 182, 212, 0.15); border-radius: 16px;
                            padding: 28px; line-height: 1.8; color: #94a3b8; font-size: 14px;">
                    <div style="font-size: 18px; font-weight: 700; color: #f8fafc; margin-bottom: 12px;">
                        📊 Strategy Impact Report
                    </div>
                    <p>
                        By implementing <strong style="color: #06b6d4;">{strategy_text}</strong>
                        targeting <strong style="color: #f8fafc;">{results['target_count']:,}</strong>
                        customers in the <strong>{target_segment}</strong> segment:
                    </p>
                    <ul style="margin: 12px 0;">
                        <li>Predicted to save <strong style="color: #10b981;">{results['customers_saved']:,}</strong>
                            customers from churning</li>
                        <li>Average churn probability reduced by
                            <strong style="color: #10b981;">{results['avg_prob_reduction'] * 100:.1f} percentage points</strong></li>
                        <li>Annual revenue retained: <strong style="color: #10b981;">${results['revenue_saved_annual']:,.0f}</strong></li>
                        <li>Lifetime revenue retained: <strong style="color: #10b981;">${results['revenue_saved_lifetime']:,.0f}</strong></li>
                        <li>Campaign investment: <strong style="color: #f59e0b;">${results['campaign_cost']:,.0f}</strong></li>
                        <li>Net benefit: <strong style="color: {'#10b981' if net_benefit > 0 else '#ef4444'};">
                            ${net_benefit:,.0f}</strong></li>
                        <li>Return on investment: <strong style="color: {'#10b981' if results['roi'] > 0 else '#ef4444'};">
                            {results['roi']:,.0f}%</strong></li>
                    </ul>
                </div>
                """), unsafe_allow_html=True)

            else:
                render_info_box(
                    "No customers matched the target segment. Try a different segment.",
                    variant="warning",
                )

        else:
            # Empty state
            st.markdown(clean_html("""
            <div style="text-align: center; padding: 80px 40px;
                        color: #475569; font-size: 15px;">
                <div style="font-size: 56px; margin-bottom: 20px; opacity: 0.4;">🎯</div>
                <div style="font-size: 20px; font-weight: 700; color: #64748b; margin-bottom: 8px;">
                    Configure a Retention Strategy
                </div>
                <div style="max-width: 400px; margin: 0 auto; color: #475569; line-height: 1.6;">
                    Use the controls on the left to set up your retention strategy.
                    The simulator will re-run the XGBoost model with modified features
                    and show you the predicted impact.
                </div>
            </div>
            """), unsafe_allow_html=True)
