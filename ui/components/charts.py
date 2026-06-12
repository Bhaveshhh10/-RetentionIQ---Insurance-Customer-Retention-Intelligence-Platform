"""
Plotly chart factory — all visualization builders for the platform.
Every chart uses a consistent dark theme from config.PLOTLY_LAYOUT.
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from config import PLOTLY_LAYOUT, RISK_COLORS, CHART_COLORS


def _apply_layout(fig, **overrides):
    """Apply the standard dark layout to a figure, with optional overrides."""
    layout = {**PLOTLY_LAYOUT, **overrides}
    
    # Correctly merge title layout dictionary and prevent 'undefined' string display in Plotly.js
    if "title" not in overrides:
        layout["title"] = None
    else:
        title_override = overrides["title"]
        if isinstance(title_override, dict):
            layout["title"] = {**PLOTLY_LAYOUT.get("title", {}), **title_override}
        elif isinstance(title_override, str):
            layout["title"] = {**PLOTLY_LAYOUT.get("title", {}), "text": title_override}
            
    fig.update_layout(**layout)
    return fig


# ============================================================
# EXECUTIVE DASHBOARD CHARTS
# ============================================================

def risk_distribution_donut(df):
    """Customer risk distribution donut chart."""
    counts = df["Risk_Category"].value_counts().reindex(["High", "Medium", "Low"])
    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.68,
        marker=dict(
            colors=[RISK_COLORS[c] for c in counts.index],
            line=dict(color="rgba(10,14,26,1)", width=2),
        ),
        textinfo="label+percent",
        textfont=dict(size=12, color="#f8fafc"),
        hovertemplate="<b>%{label}</b><br>Customers: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))

    fig.add_annotation(
        text=f"<b>{len(df):,}</b><br><span style='font-size:11px;color:#94a3b8'>Total</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=22, color="#f8fafc", family="Inter"),
    )

    return _apply_layout(fig, title=dict(text="Customer Risk Distribution"),
                         showlegend=False, height=380)


def regional_churn_bar(df):
    """Churn probability by region — horizontal bar chart."""
    regional = df.groupby("region_name").agg(
        avg_risk=("Risk_Score", "mean"),
        count=("Risk_Score", "size"),
        high_risk=("Risk_Category", lambda x: (x == "High").sum()),
    ).sort_values("avg_risk", ascending=True).reset_index()

    fig = go.Figure(go.Bar(
        y=regional["region_name"],
        x=regional["avg_risk"],
        orientation="h",
        marker=dict(
            color=regional["avg_risk"],
            colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            line=dict(width=0),
            cornerradius=4,
        ),
        text=[f"{v:.1f}%" for v in regional["avg_risk"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
        hovertemplate="<b>%{y}</b><br>Avg Risk: %{x:.1f}%<br><extra></extra>",
    ))

    return _apply_layout(fig, title=dict(text="Regional Risk Analysis"),
                         xaxis_title="Average Risk Score (%)", height=380)


def policy_type_churn_bar(df):
    """Churn analysis by policy type — grouped bar chart."""
    policy = df.groupby("policy_type").agg(
        avg_risk=("Risk_Score", "mean"),
        high_count=("Risk_Category", lambda x: (x == "High").sum()),
        total=("Risk_Score", "size"),
    ).reset_index()
    policy["high_pct"] = (policy["high_count"] / policy["total"] * 100).round(1)
    policy = policy.sort_values("avg_risk", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Avg Risk Score",
        x=policy["policy_type"],
        y=policy["avg_risk"],
        marker=dict(color="#3b82f6", cornerradius=4),
        text=[f"{v:.1f}%" for v in policy["avg_risk"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
    ))
    fig.add_trace(go.Bar(
        name="High Risk %",
        x=policy["policy_type"],
        y=policy["high_pct"],
        marker=dict(color="#ef4444", cornerradius=4),
        text=[f"{v:.1f}%" for v in policy["high_pct"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
    ))

    return _apply_layout(fig, title=dict(text="Policy Type Risk Analysis"),
                         barmode="group", height=380)


def premium_impact_scatter(df):
    """Premium change vs churn probability scatter plot."""
    sample = df.sample(min(2000, len(df)), random_state=42)

    fig = go.Figure(go.Scatter(
        x=sample["premium_change_pct"] * 100,
        y=sample["Churn_Probability"] * 100,
        mode="markers",
        marker=dict(
            size=5,
            color=sample["Risk_Score"],
            colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            colorbar=dict(
                title=dict(text="Risk Score", font=dict(color="#94a3b8")),
                tickfont=dict(color="#64748b"),
                bgcolor="rgba(0,0,0,0)",
            ),
            opacity=0.6,
            line=dict(width=0),
        ),
        hovertemplate="Premium Change: %{x:.1f}%<br>Churn Prob: %{y:.1f}%<extra></extra>",
    ))

    return _apply_layout(fig, title=dict(text="Premium Increase Impact on Churn"),
                         xaxis_title="Premium Change (%)",
                         yaxis_title="Churn Probability (%)", height=380)


def complaint_impact_chart(df):
    """Complaint impact on churn — comparison bar chart."""
    no_complaint = df[df["complaint_flag"] == 0]["Churn_Probability"].mean() * 100
    has_complaint = df[df["complaint_flag"] == 1]["Churn_Probability"].mean() * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["No Complaint", "Has Complaint"],
        y=[no_complaint, has_complaint],
        marker=dict(
            color=["#10b981", "#ef4444"],
            cornerradius=6,
        ),
        text=[f"{no_complaint:.1f}%", f"{has_complaint:.1f}%"],
        textposition="outside",
        textfont=dict(color="#f8fafc", size=14, family="Inter"),
        width=0.5,
    ))

    return _apply_layout(fig, title=dict(text="Complaint Impact on Churn"),
                         yaxis_title="Avg Churn Probability (%)", height=380,
                         showlegend=False)


def payment_behavior_chart(df):
    """Payment behavior analysis — late payments vs churn."""
    bins = [-1, 0, 1, 2, 100]
    labels = ["0", "1", "2", "3+"]
    df_copy = df.copy()
    df_copy["late_bin"] = pd.cut(
        df_copy["late_payment_count_12m"],
        bins=bins,
        labels=labels,
    )

    payment = df_copy.groupby("late_bin", observed=True).agg(
        avg_churn=("Churn_Probability", "mean"),
        count=("Churn_Probability", "size"),
    ).reset_index()
    payment["avg_churn_pct"] = (payment["avg_churn"] * 100).round(1)

    fig = go.Figure(go.Bar(
        x=payment["late_bin"],
        y=payment["avg_churn_pct"],
        marker=dict(
            color=payment["avg_churn_pct"],
            colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            cornerradius=6,
        ),
        text=[f"{v}%" for v in payment["avg_churn_pct"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=12),
    ))

    return _apply_layout(fig, title=dict(text="Late Payments vs Churn Rate"),
                         xaxis_title="Late Payments (12 months)",
                         yaxis_title="Avg Churn Probability (%)", height=380,
                         showlegend=False)


# ============================================================
# CUSTOMER EXPLORER CHARTS
# ============================================================

def risk_gauge(score, category):
    """Premium risk score gauge for individual customer view."""
    color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
    bar_color = color_map.get(category, "#3b82f6")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(
            suffix="%",
            font=dict(size=42, color="#f8fafc", family="Inter"),
        ),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickwidth=1,
                tickcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#64748b", size=10),
            ),
            bar=dict(color=bar_color, thickness=0.75),
            bgcolor="rgba(30, 41, 59, 0.5)",
            borderwidth=0,
            steps=[
                dict(range=[0, 35], color="rgba(16, 185, 129, 0.1)"),
                dict(range=[35, 65], color="rgba(245, 158, 11, 0.1)"),
                dict(range=[65, 100], color="rgba(239, 68, 68, 0.1)"),
            ],
            threshold=dict(
                line=dict(color=bar_color, width=3),
                thickness=0.85,
                value=score,
            ),
        ),
    ))

    return _apply_layout(fig, height=280, margin=dict(l=30, r=30, t=30, b=10))


def shap_waterfall_chart(shap_dict, top_n=10):
    """
    SHAP feature impact chart — horizontal bar chart showing
    positive (risk-increasing) and negative (risk-decreasing) drivers.
    """
    sorted_features = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    top_features = sorted_features[:top_n]

    # Reverse for horizontal bar display (top feature at top)
    names = [f[0] for f in reversed(top_features)]
    values = [f[1] for f in reversed(top_features)]
    colors = ["#ef4444" if v > 0 else "#10b981" for v in values]

    fig = go.Figure(go.Bar(
        y=names,
        x=values,
        orientation="h",
        marker=dict(color=colors, cornerradius=4),
        hovertemplate="<b>%{y}</b><br>SHAP Impact: %{x:.4f}<extra></extra>",
    ))

    # Add zero line
    fig.add_vline(x=0, line=dict(color="rgba(255,255,255,0.2)", width=1))

    return _apply_layout(
        fig,
        title=dict(text="Feature Impact on Churn Prediction"),
        xaxis_title="SHAP Value (→ increases churn risk)",
        height=max(300, top_n * 35 + 80),
        margin=dict(l=180, r=30, t=60, b=50),
    )


# ============================================================
# MODEL INSIGHTS CHARTS
# ============================================================

def confusion_matrix_heatmap(y_true, y_pred):
    """Interactive confusion matrix heatmap."""
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true, y_pred)

    labels = ["No Churn (0)", "Churn (1)"]
    text = [[f"{cm[i][j]:,}" for j in range(2)] for i in range(2)]

    fig = go.Figure(go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        text=text,
        texttemplate="%{text}",
        textfont=dict(size=20, color="#f8fafc", family="Inter"),
        colorscale=[[0, "#0f172a"], [0.5, "#1e3a5f"], [1, "#06b6d4"]],
        showscale=False,
        hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{text}<extra></extra>",
    ))

    return _apply_layout(
        fig,
        title=dict(text="Confusion Matrix"),
        xaxis=dict(title="Predicted", side="bottom", gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(title="Actual", autorange="reversed", gridcolor="rgba(0,0,0,0)"),
        height=380,
    )


def feature_importance_bar(importances_df, top_n=15):
    """
    Feature importance horizontal bar chart.
    Expects a DataFrame with 'Feature' and 'Importance' columns.
    """
    top = importances_df.head(top_n).sort_values("Importance", ascending=True)

    fig = go.Figure(go.Bar(
        y=top["Feature"],
        x=top["Importance"],
        orientation="h",
        marker=dict(
            color=top["Importance"],
            colorscale=[[0, "#3b82f6"], [1, "#06b6d4"]],
            cornerradius=4,
        ),
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
    ))

    return _apply_layout(
        fig,
        title=dict(text="Global Feature Importance (Mean |SHAP|)"),
        xaxis_title="Mean |SHAP Value|",
        height=max(380, top_n * 28 + 80),
        margin=dict(l=200, r=30, t=60, b=50),
        showlegend=False,
    )


def shap_dependence_scatter(dep_data, feature_name):
    """SHAP dependence plot — feature value vs SHAP value scatter."""
    fig = go.Figure(go.Scatter(
        x=dep_data["feature_value"],
        y=dep_data["shap_value"],
        mode="markers",
        marker=dict(
            size=5,
            color=dep_data["shap_value"],
            colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            opacity=0.6,
            line=dict(width=0),
        ),
        hovertemplate=f"{feature_name}: %{{x:.2f}}<br>SHAP: %{{y:.4f}}<extra></extra>",
    ))

    fig.add_hline(y=0, line=dict(color="rgba(255,255,255,0.15)", width=1, dash="dash"))

    return _apply_layout(
        fig,
        title=dict(text=f"SHAP Dependence — {feature_name}"),
        xaxis_title=feature_name,
        yaxis_title="SHAP Value",
        height=380,
    )


# ============================================================
# BUSINESS INTELLIGENCE CHARTS
# ============================================================

def churn_by_age_group(df):
    """Churn analysis by age band."""
    age_order = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
    age_data = df.groupby("age_band").agg(
        avg_churn=("Churn_Probability", "mean"),
        count=("Churn_Probability", "size"),
    ).reindex(age_order).reset_index()
    age_data["avg_churn_pct"] = (age_data["avg_churn"] * 100).round(1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=age_data["age_band"],
        y=age_data["avg_churn_pct"],
        marker=dict(
            color=age_data["avg_churn_pct"],
            colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            cornerradius=6,
        ),
        text=[f"{v}%" for v in age_data["avg_churn_pct"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
        hovertemplate="<b>%{x}</b><br>Avg Churn: %{y:.1f}%<extra></extra>",
    ))

    return _apply_layout(fig, title=dict(text="Churn Rate by Age Group"),
                         xaxis_title="Age Band", yaxis_title="Avg Churn Probability (%)",
                         height=400, showlegend=False)


def churn_by_tenure(df):
    """Churn analysis by customer tenure."""
    df_copy = df.copy()
    df_copy["tenure_group"] = pd.cut(
        df_copy["customer_tenure_months"],
        bins=[0, 12, 24, 48, 72, 120, 300],
        labels=["0-12m", "12-24m", "24-48m", "48-72m", "72-120m", "120m+"],
    )

    tenure_data = df_copy.groupby("tenure_group", observed=True).agg(
        avg_churn=("Churn_Probability", "mean"),
        count=("Churn_Probability", "size"),
    ).reset_index()
    tenure_data["avg_churn_pct"] = (tenure_data["avg_churn"] * 100).round(1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tenure_data["tenure_group"],
        y=tenure_data["avg_churn_pct"],
        mode="lines+markers+text",
        line=dict(color="#06b6d4", width=3),
        marker=dict(size=10, color="#06b6d4", line=dict(width=2, color="#0a0e1a")),
        text=[f"{v}%" for v in tenure_data["avg_churn_pct"]],
        textposition="top center",
        textfont=dict(color="#94a3b8", size=11),
        fill="tozeroy",
        fillcolor="rgba(6, 182, 212, 0.08)",
    ))

    return _apply_layout(fig, title=dict(text="Churn Rate by Customer Tenure"),
                         xaxis_title="Tenure Group", yaxis_title="Avg Churn Probability (%)",
                         height=400, showlegend=False)


def churn_by_premium_change(df):
    """Churn by premium increase ranges."""
    df_copy = df.copy()
    df_copy["premium_change_group"] = pd.cut(
        df_copy["premium_change_pct"] * 100,
        bins=[-100, -5, 0, 5, 10, 20, 100],
        labels=["< -5%", "-5% to 0%", "0% to 5%", "5% to 10%", "10% to 20%", "> 20%"],
    )

    prem_data = df_copy.groupby("premium_change_group", observed=True).agg(
        avg_churn=("Churn_Probability", "mean"),
        count=("Churn_Probability", "size"),
    ).reset_index()
    prem_data["avg_churn_pct"] = (prem_data["avg_churn"] * 100).round(1)

    fig = go.Figure(go.Bar(
        x=prem_data["premium_change_group"],
        y=prem_data["avg_churn_pct"],
        marker=dict(
            color=prem_data["avg_churn_pct"],
            colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            cornerradius=6,
        ),
        text=[f"{v}%" for v in prem_data["avg_churn_pct"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
    ))

    return _apply_layout(fig, title=dict(text="Churn Rate by Premium Change"),
                         xaxis_title="Premium Change Range",
                         yaxis_title="Avg Churn Probability (%)",
                         height=400, showlegend=False)


def risk_treemap(df):
    """Treemap showing risk distribution by region and category."""
    tree_data = df.groupby(["region_name", "Risk_Category"]).agg(
        count=("Risk_Score", "size"),
        avg_risk=("Risk_Score", "mean"),
    ).reset_index()

    fig = px.treemap(
        tree_data,
        path=["region_name", "Risk_Category"],
        values="count",
        color="avg_risk",
        color_continuous_scale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
    )

    fig.update_traces(
        textfont=dict(family="Inter", size=13),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Avg Risk: %{color:.1f}%<extra></extra>",
    )

    return _apply_layout(fig, title=dict(text="Risk Distribution Treemap"),
                         height=450, margin=dict(l=10, r=10, t=60, b=10))


def churn_flow_sankey(df):
    """Sankey diagram showing flow from risk category to churn prediction."""
    # Create labels
    labels = ["Low Risk", "Medium Risk", "High Risk", "Likely Retain", "Likely Churn"]

    # Compute flows
    flows = []
    for i, risk in enumerate(["Low", "Medium", "High"]):
        subset = df[df["Risk_Category"] == risk]
        retain = len(subset[subset["Churn_Probability"] < 0.5])
        churn = len(subset[subset["Churn_Probability"] >= 0.5])
        flows.append((i, 3, retain))  # to Likely Retain
        flows.append((i, 4, churn))   # to Likely Churn

    sources = [f[0] for f in flows]
    targets = [f[1] for f in flows]
    values = [f[2] for f in flows]
    colors = [
        "rgba(16, 185, 129, 0.4)", "rgba(16, 185, 129, 0.15)",
        "rgba(245, 158, 11, 0.4)", "rgba(245, 158, 11, 0.15)",
        "rgba(239, 68, 68, 0.15)", "rgba(239, 68, 68, 0.4)",
    ]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="rgba(255,255,255,0.1)", width=1),
            label=labels,
            color=["#10b981", "#f59e0b", "#ef4444", "#3b82f6", "#ef4444"],
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors,
        ),
    ))

    return _apply_layout(fig, title=dict(text="Customer Risk → Churn Prediction Flow"),
                         height=420, font=dict(size=13, color="#94a3b8", family="Inter"))


def marital_status_chart(df):
    """Churn by marital status."""
    marital = df.groupby("marital_status").agg(
        avg_churn=("Churn_Probability", "mean"),
        count=("Churn_Probability", "size"),
    ).reset_index()
    marital["avg_churn_pct"] = (marital["avg_churn"] * 100).round(1)

    fig = go.Figure(go.Bar(
        x=marital["marital_status"],
        y=marital["avg_churn_pct"],
        marker=dict(color=["#06b6d4", "#8b5cf6"], cornerradius=6),
        text=[f"{v}%" for v in marital["avg_churn_pct"]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=13),
        width=0.4,
    ))

    return _apply_layout(fig, title=dict(text="Churn Rate by Marital Status"),
                         yaxis_title="Avg Churn Probability (%)",
                         height=380, showlegend=False)


# ============================================================
# RETENTION SIMULATOR CHARTS
# ============================================================

def before_after_distribution(original_probs, new_probs):
    """Side-by-side histogram of churn probability before/after strategy."""
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=original_probs * 100,
        nbinsx=30,
        name="Before Strategy",
        marker=dict(color="rgba(239, 68, 68, 0.5)", line=dict(color="#ef4444", width=1)),
        opacity=0.7,
    ))

    fig.add_trace(go.Histogram(
        x=new_probs * 100,
        nbinsx=30,
        name="After Strategy",
        marker=dict(color="rgba(16, 185, 129, 0.5)", line=dict(color="#10b981", width=1)),
        opacity=0.7,
    ))

    fig.add_vline(x=50, line=dict(color="rgba(255,255,255,0.3)", width=1, dash="dash"),
                  annotation_text="Churn Threshold",
                  annotation_font=dict(color="#94a3b8", size=10))

    return _apply_layout(
        fig,
        title=dict(text="Churn Probability Distribution — Before vs After"),
        xaxis_title="Churn Probability (%)",
        yaxis_title="Number of Customers",
        barmode="overlay",
        height=400,
    )


def roi_breakdown_chart(results):
    """ROI breakdown waterfall chart."""
    fig = go.Figure(go.Waterfall(
        name="Financial Impact",
        orientation="v",
        x=["Revenue at Risk", "Revenue Saved<br>(Lifetime)", "Campaign Cost", "Net Benefit"],
        y=[
            results["original_expected_loss"] * 7,
            results["revenue_saved_lifetime"],
            -results["campaign_cost"],
            results["revenue_saved_lifetime"] - results["campaign_cost"],
        ],
        measure=["absolute", "relative", "relative", "total"],
        connector=dict(line=dict(color="rgba(255,255,255,0.1)", width=1)),
        increasing=dict(marker=dict(color="#10b981")),
        decreasing=dict(marker=dict(color="#ef4444")),
        totals=dict(marker=dict(color="#06b6d4")),
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
        text=[
            f"${results['original_expected_loss'] * 7:,.0f}",
            f"+${results['revenue_saved_lifetime']:,.0f}",
            f"-${results['campaign_cost']:,.0f}",
            f"${results['revenue_saved_lifetime'] - results['campaign_cost']:,.0f}",
        ],
    ))

    return _apply_layout(
        fig,
        title=dict(text="Financial Impact Breakdown"),
        yaxis_title="Amount ($)",
        height=420,
        showlegend=False,
    )
