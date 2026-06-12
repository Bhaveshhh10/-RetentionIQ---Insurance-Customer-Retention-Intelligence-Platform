"""
Sidebar component — branded navigation and platform info.
"""
import streamlit as st
from config import PAGES, APP_TITLE


def clean_html(html_str):
    """Remove leading and trailing whitespaces from each line to prevent markdown bugs."""
    return "".join(line.strip() for line in html_str.split("\n"))


def render_sidebar():
    """
    Render the branded sidebar with navigation.
    Returns the selected page name.
    """
    with st.sidebar:
        # Branding header
        st.markdown(clean_html("""
        <div style="padding: 16px 0 8px 0; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 4px;">🛡️</div>
            <div style="font-size: 18px; font-weight: 800; color: #f8fafc;
                        letter-spacing: -0.02em; font-family: 'Inter', sans-serif;">
                RetentionIQ
            </div>
            <div style="font-size: 11px; color: #64748b; font-weight: 500;
                        letter-spacing: 0.05em; text-transform: uppercase;">
                Insurance Intelligence
            </div>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("---")

        # Navigation
        st.markdown("### Navigation")

        # Build the radio options with icons
        options = [f"{p['icon']}  {p['name']}" for p in PAGES]

        selected = st.radio(
            "nav",
            options=options,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Platform info
        st.markdown("### Platform Info")
        st.markdown(clean_html("""
        <div style="padding: 0 0 8px 0;">
            <div style="display: flex; justify-content: space-between; padding: 6px 0;
                        border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span style="color: #64748b; font-size: 12px;">Model</span>
                <span style="color: #94a3b8; font-size: 12px; font-weight: 600;">XGBoost v3.2</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0;
                        border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span style="color: #64748b; font-size: 12px;">ROC-AUC</span>
                <span style="color: #10b981; font-size: 12px; font-weight: 600;">0.785</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0;
                        border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span style="color: #64748b; font-size: 12px;">Dataset</span>
                <span style="color: #94a3b8; font-size: 12px; font-weight: 600;">10,000 customers</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0;">
                <span style="color: #64748b; font-size: 12px;">Explainability</span>
                <span style="color: #94a3b8; font-size: 12px; font-weight: 600;">SHAP v0.52</span>
            </div>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("---")

        # Footer
        st.markdown(clean_html("""
        <div style="text-align: center; padding: 8px 0;">
            <div style="font-size: 11px; color: #475569;">
                Built with ❤️ using Streamlit
            </div>
            <div style="font-size: 10px; color: #334155; margin-top: 4px;">
                © 2025 RetentionIQ Platform
            </div>
        </div>
        """), unsafe_allow_html=True)

    # Extract the page name (remove icon prefix)
    page_name = selected.split("  ", 1)[1] if "  " in selected else selected
    return page_name
