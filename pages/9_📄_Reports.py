import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image, ImageDraw

# =========================================================
# 1. PAGE CONFIGURATION & DARK THEME STYLING
# =========================================================
st.set_page_config(
    page_title="AI Inspection Report | CONSTRUCTVISION AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Theme (#0B0F19 Base, #1E293B Cards, #F8FAFC Text)
st.markdown("""
<style>
    /* Global Text Styling */
    .stApp, .stApp *, div, p, span, h1, h2, h3, h4, h5, h6, li, td, th, label {
        color: #F8FAFC !important;
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Main Background - Deep Slate/Black */
    .stApp {
        background-color: #0B0F19;
    }
    
    /* Header Container Styling */
    .report-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Universal Card Styling (Dark Slate, Border, Shadow) */
    .report-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid #334155;
        border-top: 4px solid #3B82F6;
        transition: all 0.3s ease-in-out;
    }
    .report-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
        border-top-color: #60A5FA;
    }

    /* Input Field Customization for Dark Theme */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        color: #F8FAFC !important;
        background-color: #0F172A !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    /* Badges & Status Tags */
    .badge-blue {
        background-color: #2563EB;
        color: #FFFFFF !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-warning {
        background-color: #D97706;
        color: #FFFFFF !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .badge-success {
        background-color: #16A34A;
        color: #FFFFFF !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    /* Material Chips */
    .material-chip {
        display: inline-block;
        background-color: #0F172A;
        color: #60A5FA !important;
        border: 1.5px solid #3B82F6;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Step Timeline Styling */
    .timeline-item {
        border-left: 3px solid #3B82F6;
        padding-left: 18px;
        margin-bottom: 16px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background-color: #60A5FA;
    }

    /* Footer Banner */
    .report-footer {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. SESSION STATE & SAMPLE DATA
# =========================================================
if "report_history" not in st.session_state:
    st.session_state.report_history = [
        {"id": "CV-2026-8942", "date": "2026-08-07 14:30", "location": "Tower A, Solapur Site", "engineer": "Er. Ritika Bhumkar", "severity": "Medium", "status": "Approved"},
        {"id": "CV-2026-8939", "date": "2026-08-06 11:15", "location": "Bridge Pier 4, Pune Site", "engineer": "Er. Laiba Mulani", "severity": "High", "status": "Under Repair"},
        {"id": "CV-2026-8910", "date": "2026-08-04 09:45", "location": "Highway Sector 12", "engineer": "Er. Ritika Bhumkar", "severity": "Low", "status": "Closed"},
    ]

def get_sample_image():
    img = Image.new('RGB', (800, 500), color='#1E293B')
    d = ImageDraw.Draw(img)
    d.rectangle([100, 100, 700, 400], fill='#334155')
    d.line([250, 150, 450, 380], fill='#EF4444', width=5)
    d.line([450, 380, 520, 320], fill='#EF4444', width=4)
    d.text((20, 20), "INSPECTION IMAGE - FACADE WALL REGION", fill='#F8FAFC')
    return img

# =========================================================
# 3. HEADER SECTION
# =========================================================
st.markdown("""
<div class="report-header">
    <div>
        <h1 style="margin:0; font-size: 2.2rem; font-weight: 800; color: #F8FAFC !important;">
            📄 AI Inspection Report
        </h1>
        <p style="margin: 4px 0 0 0; font-size: 1.05rem; font-weight: 500; color: #94A3B8 !important;">
            CONSTRUCTVISION AI — Site Intelligence Platform
        </p>
    </div>
    <div style="text-align: right;">
        <span class="badge-blue">Developers</span>
        <p style="margin: 4px 0 0 0; font-size: 0.95rem; font-weight: 600; color: #F8FAFC !important;">
            Ritika Bhumkar & Laiba Mulani
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# PART 1: PROJECT & LOCATION INFORMATION
# =========================================================
st.markdown("### 📌 Part 1: Project & Location Identification")

col_proj, col_img = st.columns([1.2, 1])

with col_proj:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">🏗️ Site & Engineer Metadata</h3>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        proj_name = st.selectbox(
            "Project Name", 
            ["Site A - High-Rise Building", "Site B - Cable Bridge Project", "Site C - Expressway Paving"]
        )
        inspection_id = st.text_input("Inspection ID", "CV-2026-8942")
        date_time = st.text_input("Date & Time", datetime.now().strftime("%Y-%m-%d %H:%M"))
        
    with c2:
        site_location = st.text_input(
            "Project Location / Zone", 
            "Block B, Tower 4, Solapur Site, MH"
        )
        lead_engineer = st.selectbox(
            "Site Engineer Handling Project",
            ["Er. Ritika Bhumkar", "Er. Laiba Mulani", "Er. Sarah Chen", "Er. David Miller"]
        )
        client_name = st.text_input("Client / Contractor", "Mulani & Bhumkar Infra Corp")

    st.markdown("</div>", unsafe_allow_html=True)

with col_img:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">📸 Inspection Image Evidence</h3>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Surface Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        display_img = Image.open(uploaded_file)
    else:
        display_img = get_sample_image()
        
    st.image(display_img, caption=f"Captured Image at {site_location}", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# =========================================================
# PART 2: AI DETECTION & DIAGNOSTICS
# =========================================================
st.markdown("### 🤖 Part 2: AI Detection & Structural Diagnostics")

col_ai, col_summary = st.columns([1, 1])

with col_ai:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">🔍 AI Detection Results</h3>
        <table style="line-height: 2.2; width:100%;">
            <tr style="border-bottom: 1px solid #334155;">
                <td><strong>Component Detected</strong></td>
                <td><span class="badge-blue">Load-Bearing Wall</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #334155;">
                <td><strong>Crack Type</strong></td>
                <td>Vertical Structural Defect</td>
            </tr>
            <tr style="border-bottom: 1px solid #334155;">
                <td><strong>Severity Level</strong></td>
                <td><span class="badge-warning">Medium</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #334155;">
                <td><strong>AI Model Confidence</strong></td>
                <td><strong style="color:#60A5FA !important;">98.4%</strong></td>
            </tr>
            <tr>
                <td><strong>Assigned Engineer</strong></td>
                <td><strong>""" + lead_engineer + """</strong></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_summary:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">📋 Damage Summary Metrics</h3>
        <ul style="list-style: none; padding-left: 0; line-height: 2.2;">
            <li>🔹 <strong>Crack Length:</strong> 1.45 meters</li>
            <li>🔹 <strong>Crack Width:</strong> 1.8 mm (Exceeds IS 456 permissible limits)</li>
            <li>🔹 <strong>Damaged Surface Area:</strong> 0.35 sq.m</li>
            <li>🔹 <strong>Location Coordinates:</strong> """ + site_location + """</li>
            <li>🔹 <strong>Root Cause Analysis:</strong> Thermal expansion & curing shrinkage</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# PART 3: REPAIR & COSTING
# =========================================================
st.markdown("### 🛠️ Part 3: Repair Strategy, Gauges & Costs")

c_mat, c_steps, c_cost = st.columns([1, 1, 1])

with c_mat:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">🧱 Recommended Materials</h3>
        <p style="font-size:0.9rem; color:#94A3B8 !important;">Approved civil repair compounds:</p>
        <div>
            <span class="material-chip">Epoxy Injection</span>
            <span class="material-chip">Polymer Mortar</span>
            <span class="material-chip">Micro Concrete</span>
            <span class="material-chip">Fiber Reinforcement</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_steps:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">📋 Repair Steps</h3>
        <div class="timeline-item">
            <strong>Step 1: Surface Preparation</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8 !important;">Pressure wash substrate.</span>
        </div>
        <div class="timeline-item">
            <strong>Step 2: Epoxy Grouting</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8 !important;">Inject low-viscosity epoxy resin.</span>
        </div>
        <div class="timeline-item" style="border-left:none;">
            <strong>Step 3: Quality Audit</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8 !important;">Verification by """ + lead_engineer + """.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_cost:
    st.markdown("""
    <div class="report-card">
        <h3 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">💰 Estimated Cost</h3>
        <table style="line-height: 2.2; width:100%;">
            <tr style="border-bottom: 1px solid #334155;">
                <td>Material Cost</td>
                <td style="text-align:right;"><strong>₹ 4,500</strong></td>
            </tr>
            <tr style="border-bottom: 1px solid #334155;">
                <td>Labour Charges</td>
                <td style="text-align:right;"><strong>₹ 2,200</strong></td>
            </tr>
            <tr style="border-bottom: 1px solid #334155;">
                <td>Equipment Rental</td>
                <td style="text-align:right;"><strong>₹ 1,800</strong></td>
            </tr>
            <tr style="font-size:1.1rem; border-top: 2px solid #3B82F6;">
                <td><strong>Total Cost</strong></td>
                <td style="text-align:right; color:#60A5FA !important;"><strong>₹ 8,500</strong></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Dark Gauge Visualizations
col_gauge, col_health = st.columns([1, 1])

with col_gauge:
    st.markdown("""
    <div class="report-card">
        <h4 style="color:#F8FAFC !important; margin-top:0; text-align:center; font-weight:700;">🎯 AI Model Confidence Gauge</h4>
    """, unsafe_allow_html=True)
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=98.4,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%", 'font': {'color': "#F8FAFC", 'size': 36}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': "#3B82F6"},
            'bgcolor': "#0F172A",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 50], 'color': '#7F1D1D'},
                {'range': [50, 85], 'color': '#78350F'},
                {'range': [85, 100], 'color': '#064E3B'}
            ]
        }
    ))
    fig_gauge.update_layout(
        height=220, 
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_health:
    st.markdown("""
    <div class="report-card">
        <h4 style="color:#F8FAFC !important; margin-top:0; font-weight:700;">📊 Structural Integrity Health Bar</h4>
        <p style="margin-bottom:8px;">Overall Structural Health Score: <strong style="color:#4ADE80 !important;">91% (Healthy)</strong></p>
    """, unsafe_allow_html=True)
    
    st.progress(0.91)
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; margin-top:15px;">
        <span class="badge-success">91% Healthy</span>
        <span style="font-size:0.85rem; color:#94A3B8 !important;">Location: {site_location}</span>
    </div>
    <br>
    <p style="font-size:0.9rem; color:#94A3B8 !important;">
        Site verified by <strong>{lead_engineer}</strong>. Structural integrity meets IS-456 standards post-grouting.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# PART 4: EXPORT & AUDIT HISTORY
# =========================================================
st.markdown("### 💾 Part 4: Actions & Historical Audit Logs")

b1, b2, b3 = st.columns(3)

report_text = f"""
============================================================
CONSTRUCTVISION AI - STRUCTURAL INSPECTION REPORT
============================================================
Project Name    : {proj_name}
Inspection ID   : {inspection_id}
Date & Time     : {date_time}
Location        : {site_location}
Site Engineer   : {lead_engineer}
Client          : {client_name}
Developers      : Ritika Bhumkar & Laiba Mulani

DIAGNOSTIC RESULTS:
- Component     : Load-Bearing Wall
- Defect Type   : Vertical Structural Crack
- Severity      : Medium
- AI Confidence : 98.4%
- Total Cost    : ₹ 8,500
============================================================
"""

with b1:
    st.download_button(
        label="📄 Download Inspection Summary (TXT)",
        data=report_text,
        file_name=f"{inspection_id}_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

with b2:
    if st.button("💾 Save Record to Local Log", use_container_width=True):
        st.session_state.report_history.insert(0, {
            "id": inspection_id,
            "date": date_time,
            "location": site_location,
            "engineer": lead_engineer,
            "severity": "Medium",
            "status": "Saved"
        })
        st.success("✅ Record added to audit log!")

with b3:
    if st.button("🖨️ Buffer for Site Printing", use_container_width=True):
        st.toast("🖨️ Document sent to printer buffer.", icon="ℹ️")

st.write("")

# Audit History Table
st.markdown("#### 📜 Inspection Audit Trail")
history_df = pd.DataFrame(st.session_state.report_history)
st.dataframe(history_df, use_container_width=True)

# =========================================================
# FOOTER SECTION
# =========================================================
st.markdown("""
<div class="report-footer">
    <h3 style="color:#F8FAFC !important; margin:0; font-weight:800;">CONSTRUCTVISION AI</h3>
    <p style="color:#94A3B8 !important; margin:4px 0;">AI Powered Residential & Commercial Construction Inspection Platform</p>
    <p style="font-size:0.95rem; margin-top:12px; color:#F8FAFC !important;">
        Developed By: <strong style="color:#60A5FA !important;">Ritika Bhumkar</strong> & <strong style="color:#60A5FA !important;">Laiba Mulani</strong><br>
        🎓 Civil Engineering Site Intelligence System
    </p>
</div>
""", unsafe_allow_html=True)
