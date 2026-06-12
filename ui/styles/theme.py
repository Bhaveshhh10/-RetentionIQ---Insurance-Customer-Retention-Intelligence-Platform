"""
Complete custom CSS theme for the Insurance Retention Platform.
Overrides all default Streamlit styling to create a premium SaaS-like dark UI.
"""
import streamlit as st


def inject_custom_css():
    """Inject the complete custom CSS theme into the Streamlit app."""
    st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)


def get_custom_css():
    """Return the complete CSS theme as a string."""
    return """
/* ============================================================
   GOOGLE FONTS
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ============================================================
   CSS CUSTOM PROPERTIES
   ============================================================ */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-elevated: #1e293b;
    --bg-glass: rgba(17, 24, 39, 0.7);
    --bg-glass-hover: rgba(30, 41, 59, 0.8);
    --accent-cyan: #06b6d4;
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-gradient: linear-gradient(135deg, #06b6d4, #3b82f6);
    --accent-gradient-purple: linear-gradient(135deg, #8b5cf6, #06b6d4);
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-tertiary: #64748b;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-light: rgba(255, 255, 255, 0.15);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.5);
    --shadow-glow-cyan: 0 0 25px rgba(6, 182, 212, 0.15);
    --shadow-glow-blue: 0 0 25px rgba(59, 130, 246, 0.15);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --transition-fast: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ============================================================
   GLOBAL RESETS & FONT
   ============================================================ */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary);
}

/* ============================================================
   HIDE STREAMLIT DEFAULTS
   ============================================================ */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

[data-testid="stHeader"] {
    background: rgba(10, 14, 26, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}

/* ============================================================
   MAIN CONTENT AREA
   ============================================================ */
.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1440px !important;
}

/* ============================================================
   SIDEBAR
   ============================================================ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #0a0e1a 50%, #0d1321 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem !important;
}

/* Sidebar radio navigation styling */
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}

[data-testid="stSidebar"] .stRadio > div > label {
    padding: 11px 18px !important;
    border-radius: var(--radius-md) !important;
    cursor: pointer !important;
    transition: var(--transition) !important;
    margin: 1px 0 !important;
    border: 1px solid transparent !important;
    background: transparent !important;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(6, 182, 212, 0.08) !important;
    border-color: rgba(6, 182, 212, 0.15) !important;
}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
    background: rgba(6, 182, 212, 0.12) !important;
    border-color: rgba(6, 182, 212, 0.25) !important;
    border-left: 3px solid var(--accent-cyan) !important;
}

[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}

[data-testid="stSidebar"] .stRadio > div > label p {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) p {
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-tertiary) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
    margin-top: 24px !important;
    margin-bottom: 8px !important;
}

[data-testid="stSidebar"] hr {
    border-color: var(--border-subtle) !important;
    margin: 16px 0 !important;
}

/* ============================================================
   TYPOGRAPHY
   ============================================================ */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: var(--text-primary) !important;
    font-size: 2rem !important;
}

h2 {
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
    font-size: 1.5rem !important;
}

h3 {
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    font-size: 1.15rem !important;
}

p, li {
    color: var(--text-secondary) !important;
    line-height: 1.65 !important;
}

a {
    color: var(--accent-cyan) !important;
}

/* ============================================================
   GLASSMORPHISM CARD CLASSES
   ============================================================ */
.glass-card {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 24px;
    transition: var(--transition);
}

.glass-card:hover {
    border-color: var(--border-light);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* ============================================================
   METRIC CARDS
   ============================================================ */
.metric-card {
    background: linear-gradient(145deg, rgba(17, 24, 39, 0.85), rgba(30, 41, 59, 0.5));
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 22px 24px;
    text-align: left;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
    min-height: 130px;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--accent-gradient);
    opacity: 0;
    transition: var(--transition);
}

.metric-card:hover {
    border-color: rgba(6, 182, 212, 0.25);
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow-cyan);
}

.metric-card:hover::before {
    opacity: 1;
}

.metric-card .metric-icon {
    font-size: 24px;
    margin-bottom: 10px;
    display: inline-block;
}

.metric-card .metric-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}

.metric-card .metric-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.metric-card .metric-delta {
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
}

.metric-card .metric-delta.positive { color: var(--success); }
.metric-card .metric-delta.negative { color: var(--danger); }
.metric-card .metric-delta.neutral { color: var(--text-tertiary); }

/* Colored accent variants */
.metric-card.accent-cyan::before { background: var(--accent-cyan); opacity: 1; }
.metric-card.accent-blue::before { background: var(--accent-blue); opacity: 1; }
.metric-card.accent-purple::before { background: var(--accent-purple); opacity: 1; }
.metric-card.accent-success::before { background: var(--success); opacity: 1; }
.metric-card.accent-warning::before { background: var(--warning); opacity: 1; }
.metric-card.accent-danger::before { background: var(--danger); opacity: 1; }

/* ============================================================
   HERO SECTION
   ============================================================ */
.hero-section {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.08), rgba(59, 130, 246, 0.06), rgba(139, 92, 246, 0.04));
    border: 1px solid rgba(6, 182, 212, 0.15);
    border-radius: var(--radius-xl);
    padding: 30px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -15%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: -10%;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-title {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #06b6d4, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 15px;
    color: var(--text-secondary);
    font-weight: 400;
    margin: 0;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
    margin-top: 10px;
}

/* ============================================================
   SECTION HEADERS
   ============================================================ */
.section-header {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 28px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-subtle);
    letter-spacing: -0.01em;
}

.section-subheader {
    font-size: 14px;
    color: var(--text-tertiary);
    font-weight: 400;
    margin-top: -8px;
    margin-bottom: 16px;
}

/* ============================================================
   RISK BADGES
   ============================================================ */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.01em;
}

.risk-high {
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.25);
}

.risk-medium {
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
}

.risk-low {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

/* ============================================================
   FORM ELEMENTS
   ============================================================ */
/* Selectbox */
.stSelectbox > div > div {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
}

.stSelectbox > div > div:hover {
    border-color: var(--border-light) !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 1px var(--accent-cyan) !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background: var(--accent-gradient) !important;
}

.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
    color: var(--text-tertiary) !important;
}

/* Number input */
.stNumberInput > div > div > input {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}

/* Checkbox / Toggle */
.stCheckbox > label {
    color: var(--text-secondary) !important;
}

/* Button */
.stButton > button {
    background: var(--accent-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 28px !important;
    font-size: 14px !important;
    transition: var(--transition) !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    opacity: 0.92 !important;
    box-shadow: var(--shadow-glow-cyan) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 24px !important;
    transition: var(--transition) !important;
}

.stDownloadButton > button:hover {
    box-shadow: 0 0 25px rgba(16, 185, 129, 0.2) !important;
    transform: translateY(-1px) !important;
}

/* ============================================================
   TABS
   ============================================================ */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(17, 24, 39, 0.6) !important;
    border-radius: var(--radius-md) !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border-subtle) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    color: var(--text-tertiary) !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: var(--transition-fast) !important;
    background: transparent !important;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(255, 255, 255, 0.04) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg-elevated) !important;
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ============================================================
   EXPANDER
   ============================================================ */
[data-testid="stExpander"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

[data-testid="stExpander"] summary:hover {
    color: var(--accent-cyan) !important;
}

/* ============================================================
   DATAFRAMES & TABLES
   ============================================================ */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden;
}

[data-testid="stDataFrame"] table {
    font-family: 'Inter', sans-serif !important;
}

/* ============================================================
   METRICS (Streamlit native)
   ============================================================ */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(30, 41, 59, 0.4));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 16px 20px;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-tertiary) !important;
}

/* ============================================================
   DIVIDER
   ============================================================ */
hr {
    border-color: var(--border-subtle) !important;
    margin: 20px 0 !important;
}

/* ============================================================
   PLOTLY CHART CONTAINERS
   ============================================================ */
.js-plotly-plot {
    border-radius: var(--radius-md) !important;
}

.stPlotlyChart {
    background: rgba(17, 24, 39, 0.4) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-lg) !important;
    padding: 12px !important;
    transition: var(--transition) !important;
}

.stPlotlyChart:hover {
    border-color: var(--border-light) !important;
}

/* ============================================================
   RECOMMENDATION CARDS
   ============================================================ */
.recommendation-card {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(6, 182, 212, 0.04));
    border: 1px solid rgba(16, 185, 129, 0.18);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin-bottom: 10px;
    font-size: 14px;
    color: var(--text-primary);
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    gap: 10px;
}

.recommendation-card:hover {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(6, 182, 212, 0.06));
    border-color: rgba(16, 185, 129, 0.3);
    transform: translateX(4px);
}

/* ============================================================
   STRATEGY CARDS (Retention Simulator)
   ============================================================ */
.strategy-card {
    background: linear-gradient(145deg, rgba(139, 92, 246, 0.08), rgba(59, 130, 246, 0.04));
    border: 1px solid rgba(139, 92, 246, 0.18);
    border-radius: var(--radius-lg);
    padding: 24px;
    margin-bottom: 16px;
}

.strategy-card:hover {
    border-color: rgba(139, 92, 246, 0.3);
}

/* ============================================================
   IMPACT METRICS (Simulator results)
   ============================================================ */
.impact-card-positive {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.03));
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: var(--radius-lg);
    padding: 20px;
    text-align: center;
}

.impact-card-neutral {
    background: linear-gradient(145deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.03));
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: var(--radius-lg);
    padding: 20px;
    text-align: center;
}

.impact-card-warning {
    background: linear-gradient(145deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.03));
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: var(--radius-lg);
    padding: 20px;
    text-align: center;
}

.impact-value {
    font-size: 32px;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.2;
}

.impact-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

/* ============================================================
   PROFILE CARDS
   ============================================================ */
.profile-card {
    background: linear-gradient(145deg, rgba(17, 24, 39, 0.85), rgba(30, 41, 59, 0.5));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 24px;
    height: 100%;
}

.profile-field {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-subtle);
}

.profile-field:last-child {
    border-bottom: none;
}

.profile-field-label {
    font-size: 13px;
    color: var(--text-tertiary);
    font-weight: 500;
}

.profile-field-value {
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 600;
}

/* ============================================================
   INFO BOXES
   ============================================================ */
.info-box {
    background: rgba(6, 182, 212, 0.08);
    border: 1px solid rgba(6, 182, 212, 0.15);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 16px;
    line-height: 1.6;
}

.info-box-warning {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.15);
    color: var(--text-secondary);
}

.info-box-danger {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.15);
    color: var(--text-secondary);
}

/* ============================================================
   FILTER BAR
   ============================================================ */
.filter-bar {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
    margin-bottom: 24px;
}

/* ============================================================
   ANIMATIONS
   ============================================================ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse-subtle {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.75; }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.animate-fade-in {
    animation: fadeIn 0.5s ease-out forwards;
}

.animate-fade-up {
    animation: fadeInUp 0.6s ease-out forwards;
}

.animate-pulse {
    animation: pulse-subtle 2.5s ease-in-out infinite;
}

/* ============================================================
   SCROLLBAR
   ============================================================ */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--bg-elevated);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}

/* ============================================================
   TEXT SELECTION
   ============================================================ */
::selection {
    background: rgba(6, 182, 212, 0.3);
    color: var(--text-primary);
}

/* ============================================================
   COLUMNS SPACING
   ============================================================ */
[data-testid="column"] {
    padding: 0 8px !important;
}

/* ============================================================
   ALERTS / ST.INFO, ST.WARNING, etc.
   ============================================================ */
.stAlert {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
}

/* ============================================================
   SPINNER
   ============================================================ */
.stSpinner > div {
    border-top-color: var(--accent-cyan) !important;
}

/* ============================================================
   TOOLTIP
   ============================================================ */
[data-testid="stTooltipContent"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
}
"""
