"""
Reusable metric card components for the dashboard.
Renders premium glassmorphism KPI cards using custom HTML/CSS.
Uses st.markdown with clean_html to bypass markdown bugs and render HTML directly in the page DOM.
"""
import streamlit as st


def clean_html(html_str):
    """Remove leading and trailing whitespaces from each line to prevent markdown bugs."""
    return "".join(line.strip() for line in html_str.split("\n"))


def render_metric_card(icon, label, value, delta=None, delta_type="neutral", accent="cyan"):
    """
    Render a single premium metric card with glassmorphism styling.
    """
    delta_html = f'<div class="metric-delta {delta_type}">{delta}</div>' if delta else ""
    html = f'<div class="metric-card accent-{accent}"><div class="metric-icon">{icon}</div><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{delta_html}</div>'
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_hero_section(title, subtitle, badge_text=None):
    """
    Render the hero section with gradient title and subtitle.
    """
    badge_html = f'<div class="hero-badge">⚡ {badge_text}</div>' if badge_text else ""
    html = f'<div class="hero-section"><div class="hero-title">{title}</div><p class="hero-subtitle">{subtitle}</p>{badge_html}</div>'
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_section_header(title, subtitle=None):
    """Render a styled section header with optional subtitle."""
    st.markdown(clean_html(f'<div class="section-header">{title}</div>'), unsafe_allow_html=True)
    if subtitle:
        st.markdown(clean_html(f'<div class="section-subheader">{subtitle}</div>'), unsafe_allow_html=True)


def render_risk_badge(risk_category):
    """Render an inline risk category badge."""
    cls_map = {"High": "risk-high", "Medium": "risk-medium", "Low": "risk-low"}
    icon_map = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    cls = cls_map.get(risk_category, "risk-low")
    icon = icon_map.get(risk_category, "⚪")

    html = f'<span class="risk-badge {cls}">{icon} {risk_category} Risk</span>'
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_profile_card(fields):
    """
    Render a customer profile card with key-value fields.
    """
    rows = ""
    for label, value in fields:
        rows += f'<div class="profile-field"><span class="profile-field-label">{label}</span><span class="profile-field-value">{value}</span></div>'

    html = f'<div class="profile-card">{rows}</div>'
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_recommendation_cards(recommendations_str):
    """
    Render retention recommendation cards from the recommendation string.
    """
    recs = str(recommendations_str).replace("[", "").replace("]", "").replace("'", "")
    rec_list = [r.strip() for r in recs.split(",") if r.strip()]

    icon_map = {
        "Offer premium discount": "💰",
        "Offer flexible payment plan": "📋",
        "Promote bundled insurance products": "📦",
        "Assign dedicated support": "🤝",
        "Prioritize complaint resolution": "⚡",
    }

    for rec in rec_list:
        icon = "✅"
        for key, emoji in icon_map.items():
            if key.lower() in rec.lower():
                icon = emoji
                break

        html = f'<div class="recommendation-card"><span style="font-size: 18px;">{icon}</span><span>{rec}</span></div>'
        st.markdown(clean_html(html), unsafe_allow_html=True)


def render_info_box(text, variant="default"):
    """Render an info box with optional variant styling."""
    cls = "info-box"
    if variant == "warning":
        cls = "info-box info-box-warning"
    elif variant == "danger":
        cls = "info-box info-box-danger"

    st.markdown(clean_html(f'<div class="{cls}">{text}</div>'), unsafe_allow_html=True)


def render_impact_card(label, value, variant="positive"):
    """Render an impact metric card for the simulator."""
    cls = f"impact-card-{variant}"
    html = f'<div class="{cls}"><div class="impact-label">{label}</div><div class="impact-value">{value}</div></div>'
    st.markdown(clean_html(html), unsafe_allow_html=True)
