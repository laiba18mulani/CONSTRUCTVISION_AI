import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# 1. PAGE CONFIGURATION & CYBER-DARK CSS THEME
# =========================================================
st.set_page_config(
    page_title="Damage Analysis Dashboard | CONSTRUCTVISION AI",
    page_icon="📊",
    layout="wide"
)

# Custom High-Contrast Dark Theme CSS
st.markdown("""
<style>
    /* Main Background & Text Color */
    .stApp {
        background-color: #0E1117;
        color: #E2E8F0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Dark Cards & Container Boxes */
    .dark-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #161B22 0%, #1F2937 100%);
        border: 1px solid #374151;
        border-left: 4px solid #00F2FE;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }

    /* Custom Metric Text */
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 4px 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Severity Badges */
    .badge-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid #EF4444;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid #F59E0B;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }

    /* Clean Streamlit Headers */
    h1, h2, h3, h4 {
        color: #F8FAFC !important;
        font-weight: 700;
    }
    
    /* Divider */
    hr {
        border-color: #30363D !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. DATA SOURCE & DATA ENGINE
# =========================================================
raw_damage_data = pd.DataFrame([
    {
        "ID": "DEF-001",
        "Damage Type": "Hairline Crack",
        "Severity": "Low",
        "Confidence (%)": 98,
        "Repair Material": "Crack Sealant Polymer",
        "Estimated Cost (₹)": 8500,
        "Structural Risk": "Minimal",
        "Urgency": "Scheduled",
        "IS Standard": "IS 456 Clause 12.3",
        "Area (sq.ft)": 15
    },
    {
        "ID": "DEF-002",
        "Damage Type": "Corrosion",
        "Severity": "Medium",
        "Confidence (%)": 94,
        "Repair Material": "Anti-Corrosion Zinc Coating",
        "Estimated Cost (₹)": 25000,
        "Structural Risk": "Moderate",
        "Urgency": "High Priority",
        "IS Standard": "IS 9077 / IS 13620",
        "Area (sq.ft)": 35
    },
    {
        "ID": "DEF-003",
        "Damage Type": "Leakage",
        "Severity": "High",
        "Confidence (%)": 91,
        "Repair Material": "Crystalline Waterproof Slurry",
        "Estimated Cost (₹)": 12000,
        "Structural Risk": "High",
        "Urgency": "Immediate Action",
        "IS Standard": "IS 2645",
        "Area (sq.ft)": 20
    },
    {
        "ID": "DEF-004",
        "Damage Type": "Spalling",
        "Severity": "Medium",
        "Confidence (%)": 89,
        "Repair Material": "Polymer Modified Repair Mortar",
        "Estimated Cost (₹)": 18000,
        "Structural Risk": "Moderate",
        "Urgency": "High Priority",
        "IS Standard": "IS 516 / SP 23",
        "Area (sq.ft)": 28
    },
    {
        "ID": "DEF-005",
        "Damage Type": "Honeycombing",
        "Severity": "Low",
        "Confidence (%)": 86,
        "Repair Material": "Non-Shrink Epoxy Grout",
        "Estimated Cost (₹)": 6000,
        "Structural Risk": "Low",
        "Urgency": "Scheduled",
        "IS Standard": "IS 2250",
        "Area (sq.ft)": 10
    }
])

# =========================================================
# 3. SIDEBAR CONTROLS & FILTERS
# =========================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/structural.png", width=60)
    st.title("⚙️ Filter Controls")
    st.markdown("---")
    
    # Severity Multiselect Filter
    selected_severities = st.multiselect(
        "Filter by Severity",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )
    
    # Confidence Slider
    min_confidence = st.slider(
        "Min AI Confidence Threshold (%)",
        min_value=50,
        max_value=100,
        value=80,
        step=1
    )
    
    st.markdown("---")
    st.caption("🤖 **AI Model Version:** Vision-Net v3.2")
    st.caption("📅 **Last Inspection:** Today")

# Apply Filters
filtered_data = raw_damage_data[
    (raw_damage_data["Severity"].isin(selected_severities)) &
    (raw_damage_data["Confidence (%)"] >= min_confidence)
]

# =========================================================
# 4. DASHBOARD HEADER & TOP KPI CARDS
# =========================================================
st.title("📊 AI Structural Damage Analysis")
st.caption("Real-time computer vision defect classification, structural risk metrics, and engineering intervention logs.")
st.markdown("---")

# Calculate Dynamic Summary Metrics
total_defects = len(filtered_data)
avg_conf = filtered_data["Confidence (%)"].mean() if not filtered_data.empty else 0
total_cost = filtered_data["Estimated Cost (₹)"].sum() if not filtered_data.empty else 0
high_risk_count = len(filtered_data[filtered_data["Severity"] == "High"])

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Damages</div>
        <div class="metric-value">{total_defects}</div>
        <small style="color:#9CA3AF;">Detected Defect Count</small>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10B981;">
        <div class="metric-label">Avg Confidence</div>
        <div class="metric-value">{avg_conf:.1f}%</div>
        <small style="color:#10B981;">Model Precision</small>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #EF4444;">
        <div class="metric-label">Critical Defects</div>
        <div class="metric-value" style="color:#EF4444;">{high_risk_count}</div>
        <small style="color:#EF4444;">Immediate Action Needed</small>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #F59E0B;">
        <div class="metric-label">Total Est. Repair</div>
        <div class="metric-value">₹ {total_cost:,.0f}</div>
        <small style="color:#F59E0B;">Budget Requirement</small>
    </div>
    """, unsafe_allow_html=True)

with c5:
    # Calculated Health Index (Simple baseline logic)
    health_score = max(0, 100 - (high_risk_count * 20 + (total_defects - high_risk_count) * 8))
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #3B82F6;">
        <div class="metric-label">Health Index</div>
        <div class="metric-value" style="color:#3B82F6;">{health_score}/100</div>
        <small style="color:#9CA3AF;">Structural Integrity</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# 5. MAIN TABBED INTERFACE
# =========================================================
tab_overview, tab_charts, tab_protocol, tab_export = st.tabs([
    "📋 Inspection Master Log",
    "📈 Analytics & Visualizations",
    "🛠️ Method Statement & Standards",
    "💾 Export & Reports"
])

# ---------------------------------------------------------
# TAB 1: INSPECTION MASTER LOG
# ---------------------------------------------------------
with tab_overview:
    if filtered_data.empty:
        st.warning("⚠️ No damages match the selected filters. Please adjust the sidebar controls.")
    else:
        st.markdown("""
        <div class="dark-card">
            <h3 style="margin-top:0;">📋 Defect Inspection Table</h3>
        """, unsafe_allow_html=True)
        
        # Display Styled Dataframe
        st.dataframe(
            filtered_data,
            column_config={
                "Confidence (%)": st.column_config.ProgressColumn(
                    "AI Confidence (%)",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
                "Estimated Cost (₹)": st.column_config.NumberColumn(
                    "Est. Cost (₹)",
                    format="₹ %d"
                ),
                "Area (sq.ft)": st.column_config.NumberColumn(
                    "Area (sq.ft)",
                    format="%d sq.ft"
                )
            },
            use_container_width=True,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: ANALYTICS & PLOTLY VISUALIZATIONS
# ---------------------------------------------------------
with tab_charts:
    if not filtered_data.empty:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("""
            <div class="dark-card">
                <h4 style="margin-top:0;">💰 Cost Distribution by Damage Type</h4>
            """, unsafe_allow_html=True)
            
            fig_cost = px.bar(
                filtered_data,
                x="Damage Type",
                y="Estimated Cost (₹)",
                color="Severity",
                color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"},
                text_auto='.2s',
                template="plotly_dark"
            )
            fig_cost.update_layout(
                paper_bgcolor="#161B22",
                plot_bgcolor="#161B22",
                font_color="#E2E8F0",
                height=320,
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig_cost, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_chart2:
            st.markdown("""
            <div class="dark-card">
                <h4 style="margin-top:0;">🚨 Defect Severity Breakdown</h4>
            """, unsafe_allow_html=True)
            
            fig_donut = px.pie(
                filtered_data,
                names="Severity",
                values="Estimated Cost (₹)",
                hole=0.5,
                color="Severity",
                color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"},
                template="plotly_dark"
            )
            fig_donut.update_layout(
                paper_bgcolor="#161B22",
                plot_bgcolor="#161B22",
                font_color="#E2E8F0",
                height=320,
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Confidence Horizontal Bar
        st.markdown("""
        <div class="dark-card">
            <h4 style="margin-top:0;">🎯 AI Detection Confidence Scores</h4>
        """, unsafe_allow_html=True)
        
        fig_conf = px.bar(
            filtered_data,
            x="Confidence (%)",
            y="Damage Type",
            orientation='h',
            color="Confidence (%)",
            color_continuous_scale="Viridis",
            text="Confidence (%)",
            template="plotly_dark"
        )
        fig_conf.update_layout(
            paper_bgcolor="#161B22",
            plot_bgcolor="#161B22",
            font_color="#E2E8F0",
            height=250,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig_conf, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: METHOD STATEMENT & STANDARDS DRILL-DOWN
# ---------------------------------------------------------
with tab_protocol:
    st.markdown("""
    <div class="dark-card">
        <h3 style="margin-top:0;">🛠️ Recommended Action Plan & Engineering Protocol</h3>
    """, unsafe_allow_html=True)
    
    selected_damage = st.selectbox(
        "Select Damage Type for In-Depth Technical Specification:",
        raw_damage_data["Damage Type"].unique()
    )
    
    row = raw_damage_data[raw_damage_data["Damage Type"] == selected_damage].iloc[0]
    
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.info(f"**Material:** {row['Repair Material']}")
    col_p2.warning(f"**IS Code Reference:** {row['IS Standard']}")
    col_p3.error(f"**Action Urgency:** {row['Urgency']}")
    
    st.markdown("---")
    st.markdown("#### 📋 Step-by-Step Engineering Execution Protocol")
    
    # Detailed procedures per defect type
    protocols = {
        "Hairline Crack": [
            "Clean crack surface thoroughly using wire brush and compressed air.",
            "V-groove crack along the length to a depth of 5-10mm.",
            "Apply low-viscosity polymer sealant using a pressurized nozzle.",
            "Allow 24-hour ambient curing before painting/plastering."
        ],
        "Corrosion": [
            "Chisel concrete around corroded rebar to expose at least 20mm clean steel all around.",
            "Sandblast steel to remove rust scale (SA 2.5 finish).",
            "Apply 2 coats of zinc-rich anti-corrosion primer to exposed rebar.",
            "Apply polymer-modified mortar patch with bonding agent."
        ],
        "Leakage": [
            "Identify origin point of dampness / pressure leak.",
            "Drill injection ports at 45-degree angles to intercept crack path.",
            "Inject crystalline slurry or polyurethane foam grouting under 5 bar pressure.",
            "Seal surface ports with waterproof quick-setting plug mortar."
        ],
        "Spalling": [
            "Remove all loose or delaminated concrete until sound aggregate is exposed.",
            "Apply acrylic bonding slurry over SSD (Saturated Surface Dry) substrate.",
            "Trowel-apply polymer-modified repair mortar (PMM) in layers not exceeding 20mm.",
            "Wet cure for 3 to 5 days."
        ],
        "Honeycombing": [
            "Hack out uncompacted aggregate until solid, dense concrete is reached.",
            "Blow clean with oil-free compressed air and thoroughly wet the cavity.",
            "Form shuttering and pressure-inject non-shrink high-strength epoxy grout.",
            "De-shutter after 24 hours and finish flush with surrounding concrete."
        ]
    }
    
    for idx, step in enumerate(protocols.get(selected_damage, []), 1):
        st.markdown(f"**Step {idx}:** {step}")
        
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: EXPORT & REPORTS
# ---------------------------------------------------------
with tab_export:
    st.markdown("""
    <div class="dark-card">
        <h3 style="margin-top:0;">💾 Export Analysis Logs & Reports</h3>
        <p>Download structured inspection logs for integration into AutoCAD, Revit, or ERP systems.</p>
    """, unsafe_allow_html=True)
    
    col_ex1, col_ex2 = st.columns(2)
    
    with col_ex1:
        st.subheader("📄 Export Filtered CSV Data")
        st.download_button(
            label="📥 Download Damage Data (CSV)",
            data=filtered_data.to_csv(index=False),
            file_name=f"Structural_Damage_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with col_ex2:
        st.subheader("📄 Export JSON Summary")
        st.download_button(
            label="📥 Download Inspection Brief (JSON)",
            data=filtered_data.to_json(orient="records", indent=2),
            file_name=f"Damage_Inspection_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
        
    st.markdown("</div>", unsafe_allow_html=True)
    