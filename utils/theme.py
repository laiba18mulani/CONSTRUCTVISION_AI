import streamlit as st

def apply_premium_theme():
    """Injects sub-pixel borders, JetBrains Mono micro-typography, and high-density SaaS styling."""
    css = """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global Viewport & Blueprint Grid */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #020812 !important;
        color: #F5F7FA !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(0, 200, 255, 0.05) 0%, transparent 60%),
            linear-gradient(rgba(0, 200, 255, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 200, 255, 0.025) 1px, transparent 1px) !important;
        background-size: 100% 100%, 28px 28px, 28px 28px !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #06111F !important;
        border-right: 1px solid rgba(0, 200, 255, 0.15) !important;
    }

    /* Sub-Pixel Glassmorphic Panels */
    .cv-card {
        background: rgba(10, 23, 40, 0.65);
        border: 1px solid rgba(0, 200, 255, 0.18);
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cv-card:hover {
        border-color: rgba(0, 200, 255, 0.45);
        box-shadow: 0 6px 24px -2px rgba(0, 200, 255, 0.12);
        transform: translateY(-1px);
    }

    /* Monospace Typography for Numbers & Data */
    .mono-value {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .kpi-title {
        color: #94A3B8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    .kpi-value {
        color: #00C8FF;
        font-size: 1.85rem;
        line-height: 1.1;
    }
    .kpi-desc {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 6px;
    }

    /* Micro Status Badges */
    .badge-success {
        background: rgba(57, 255, 136, 0.08);
        color: #39FF88;
        border: 1px solid rgba(57, 255, 136, 0.25);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-warning {
        background: rgba(255, 176, 32, 0.08);
        color: #FFB020;
        border: 1px solid rgba(255, 176, 32, 0.25);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Section Divider */
    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F5F7FA;
        letter-spacing: 0.02em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(0, 200, 255, 0.12);
        padding-bottom: 6px;
    }

    /* Form Controls & Inputs */
    .stSelectbox > div > div, .stTextInput > div > div {
        background-color: #0A1728 !important;
        border: 1px solid rgba(0, 200, 255, 0.2) !important;
        color: #F5F7FA !important;
        border-radius: 6px !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str, status_text: str = "ALL SYSTEMS OPERATIONAL"):
    """Renders top header banner with live system status indicator."""
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                <div>
                    <h1 style="margin:0; font-size: 1.9rem; font-weight: 700; color: #F5F7FA; letter-spacing: -0.01em;">{title}</h1>
                    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 0.88rem;">{subtitle}</p>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span class="badge-success">● {status_text}</span>
                    <span style="color: #64748B; font-family: 'JetBrains Mono'; font-size: 0.75rem;">v2.4.0-PROD</span>
                </div>
            </div>
            <hr style="border: none; height: 1px; background: linear-gradient(90deg, rgba(0,200,255,0.3) 0%, rgba(0,200,255,0.05) 100%); margin-top: 14px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    