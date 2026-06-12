"""
Application configuration and constants for the Insurance Retention Platform.
Centralizes all color palettes, feature definitions, business constants, and Plotly theming.
"""

# ============================================================
# APP METADATA
# ============================================================

APP_TITLE = "RetentionIQ — Insurance Intelligence Platform"
APP_ICON = "🛡️"
APP_SUBTITLE = "AI-Powered Churn Analytics & Retention Strategy"

# ============================================================
# PAGE CONFIGURATION
# ============================================================

PAGES = [
    {"name": "Executive Dashboard", "icon": "📊"},
    {"name": "Customer Explorer", "icon": "🔍"},
    {"name": "High Risk Center", "icon": "🚨"},
    {"name": "Model Insights", "icon": "🧠"},
    {"name": "Business Intelligence", "icon": "📈"},
    {"name": "Retention Simulator", "icon": "🎯"},
]

PAGE_NAMES = [p["name"] for p in PAGES]
PAGE_ICONS = {p["name"]: p["icon"] for p in PAGES}

# ============================================================
# COLOR PALETTE
# ============================================================

COLORS = {
    "bg_primary": "#0a0e1a",
    "bg_secondary": "#111827",
    "bg_elevated": "#1e293b",
    "bg_glass": "rgba(17, 24, 39, 0.7)",
    "accent_cyan": "#06b6d4",
    "accent_blue": "#3b82f6",
    "accent_purple": "#8b5cf6",
    "accent_indigo": "#6366f1",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#38bdf8",
    "text_primary": "#f8fafc",
    "text_secondary": "#94a3b8",
    "text_tertiary": "#64748b",
    "border_subtle": "rgba(255, 255, 255, 0.08)",
    "border_light": "rgba(255, 255, 255, 0.12)",
}

RISK_COLORS = {
    "High": "#ef4444",
    "Medium": "#f59e0b",
    "Low": "#10b981",
}

CHART_COLORS = [
    "#06b6d4", "#3b82f6", "#8b5cf6", "#f59e0b",
    "#10b981", "#ef4444", "#ec4899", "#6366f1",
    "#14b8a6", "#f97316",
]

# ============================================================
# FEATURE DEFINITIONS
# ============================================================

FEATURE_COLUMNS = [
    'region_name', 'age', 'age_band', 'marital_status', 'customer_tenure_months',
    'multi_policy_flag', 'num_policies', 'policy_type', 'renewal_month',
    'current_premium', 'premium_last_year', 'premium_change_pct',
    'num_price_increases_last_3y', 'coverage_amount', 'premium_to_coverage_ratio',
    'payment_frequency', 'autopay_enabled', 'late_payment_count_12m',
    'missed_payment_flag', 'payment_method_change_flag', 'num_claims_12m',
    'num_approved_claims_12m', 'num_rejected_claims_12m', 'num_pending_claims_12m',
    'avg_claim_amount', 'total_claim_amount_12m', 'total_payout_amount_12m',
    'payout_ratio_12m', 'avg_settlement_time_days', 'days_since_last_claim',
    'num_contacts_12m', 'complaint_flag', 'complaint_resolution_days',
    'quote_requested_flag', 'coverage_downgrade_flag',
]

CATEGORICAL_COLUMNS = [
    'region_name', 'age_band', 'marital_status', 'policy_type', 'payment_frequency',
]

FEATURE_DISPLAY_NAMES = {
    'age': 'Age',
    'customer_tenure_months': 'Customer Tenure',
    'multi_policy_flag': 'Multi-Policy Holder',
    'num_policies': 'Number of Policies',
    'renewal_month': 'Renewal Month',
    'current_premium': 'Current Premium ($)',
    'premium_last_year': 'Last Year Premium ($)',
    'premium_change_pct': 'Premium Change %',
    'num_price_increases_last_3y': 'Price Increases (3yr)',
    'coverage_amount': 'Coverage Amount ($)',
    'premium_to_coverage_ratio': 'Premium / Coverage Ratio',
    'autopay_enabled': 'Auto-Pay Enabled',
    'late_payment_count_12m': 'Late Payments (12m)',
    'missed_payment_flag': 'Missed Payment',
    'payment_method_change_flag': 'Payment Method Changed',
    'num_claims_12m': 'Claims Filed (12m)',
    'num_approved_claims_12m': 'Approved Claims (12m)',
    'num_rejected_claims_12m': 'Rejected Claims (12m)',
    'num_pending_claims_12m': 'Pending Claims (12m)',
    'avg_claim_amount': 'Avg Claim Amount ($)',
    'total_claim_amount_12m': 'Total Claims (12m)',
    'total_payout_amount_12m': 'Total Payout (12m)',
    'payout_ratio_12m': 'Payout Ratio',
    'avg_settlement_time_days': 'Avg Settlement Time (days)',
    'days_since_last_claim': 'Days Since Last Claim',
    'num_contacts_12m': 'Customer Contacts (12m)',
    'complaint_flag': 'Has Complaint',
    'complaint_resolution_days': 'Complaint Resolution (days)',
    'quote_requested_flag': 'Quote Requested',
    'coverage_downgrade_flag': 'Coverage Downgraded',
    'region_name': 'Region',
    'age_band': 'Age Band',
    'marital_status': 'Marital Status',
    'policy_type': 'Policy Type',
    'payment_frequency': 'Payment Frequency',
}

# ============================================================
# BUSINESS CONSTANTS
# ============================================================

AVG_CUSTOMER_LIFETIME_YEARS = 7
MODEL_ROC_AUC = 0.785
CHURN_THRESHOLD = 0.5

# Cost assumptions for retention simulator
RETENTION_COSTS = {
    "premium_discount_per_pct": 0.01,      # 1% of premium per 1% discount
    "flexible_payment_cost": 25,            # $25 per customer admin cost
    "multi_policy_discount_per_pct": 0.01,  # 1% of premium per 1% bundle discount
    "dedicated_support_cost": 150,          # $150 per customer per year
}

# ============================================================
# PLOTLY TEMPLATE
# ============================================================

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
    title=dict(
        font=dict(color="#f8fafc", size=16, family="Inter, sans-serif"),
        x=0, xanchor="left", y=0.98,
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)",
        title_font=dict(color="#94a3b8", size=12),
        tickfont=dict(color="#64748b", size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)",
        title_font=dict(color="#94a3b8", size=12),
        tickfont=dict(color="#64748b", size=11),
    ),
    margin=dict(l=50, r=20, t=60, b=50),
    legend=dict(
        font=dict(color="#94a3b8", size=11),
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.05)",
    ),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font=dict(color="#f8fafc", family="Inter, sans-serif", size=13),
        bordercolor="rgba(255,255,255,0.1)",
    ),
    colorway=CHART_COLORS,
)
