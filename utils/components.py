import streamlit as st
from utils.charts import create_sparkline

def render_kpi_card_with_sparkline(title: str, value: str, description: str, sparkline_data: list, icon: str = "📊", status: str = "NORMAL"):
    """Renders a metric card with an embedded micro-sparkline."""
    badge_class = "badge-success" if status == "NORMAL" else "badge-warning"
    
    col_text, col_chart = st.columns([1.6, 1])
    
    with col_text:
        st.markdown(
            f"""
            <div class="cv-card" style="margin-bottom:0px;">
                <div style="display:flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.1rem;">{icon}</span>
                    <span class="{badge_class}">● {status}</span>
                </div>
                <div class="kpi-title" style="margin-top: 8px;">{title}</div>
                <div class="kpi-value mono-value">{value}</div>
                <div class="kpi-desc">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_chart:
        fig = create_sparkline(sparkline_data)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})