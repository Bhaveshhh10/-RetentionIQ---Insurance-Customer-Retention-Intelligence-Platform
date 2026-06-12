"""
RetentionIQ — Insurance Customer Retention Intelligence Platform
================================================================
Main entry point for the Streamlit application.
Routes to the appropriate page module based on sidebar navigation.
"""
import streamlit as st

# ── Page Configuration (must be first Streamlit call) ──
st.set_page_config(
    page_title="RetentionIQ — Insurance Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Custom Theme ──
from ui.styles.theme import inject_custom_css
inject_custom_css()

# ── Sidebar Navigation ──
from ui.components.sidebar import render_sidebar
selected_page = render_sidebar()

# ── Page Router ──
from ui.pages_app import (
    executive_dashboard,
    customer_explorer,
    high_risk_center,
    model_insights,
    business_intelligence,
    retention_simulator,
)

PAGE_MAP = {
    "Executive Dashboard": executive_dashboard,
    "Customer Explorer": customer_explorer,
    "High Risk Center": high_risk_center,
    "Model Insights": model_insights,
    "Business Intelligence": business_intelligence,
    "Retention Simulator": retention_simulator,
}

# ── Render Selected Page ──
page_module = PAGE_MAP.get(selected_page)
if page_module:
    page_module.render()
else:
    st.error(f"Page '{selected_page}' not found.")