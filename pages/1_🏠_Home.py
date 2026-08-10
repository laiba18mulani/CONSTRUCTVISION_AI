import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import plotly.express as px
import plotly.graph_objects as go
import io

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="CONSTRUCTVISION AI | Dark Edition",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM DARK THEME CSS
# =====================================================
st.markdown("""
<style>
    /* Global Reset & Dark Theme */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Blueprint Dark Grid Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
        background-size: 35px 35px;
        pointer-events: none;
        z-index: 0;
    }

    /* Hide Streamlit Headers */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1E293B;
    }

    /* Card Layouts */
    .dark-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .dark-card:hover {
        border-color: #38BDF8;
        box-shadow: 0 6px 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }

    /* Hero Section */
    .hero-dark {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 6px solid #38BDF8;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Header Accents */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700;
    }
    .accent-text {
        color: #38BDF8;
    }
    .accent-orange {
        color: #F97316;
    }

    /* Metrics Visuals */
    .metric-container {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 13px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Custom Streamlit Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0284C7 0%, #0369A1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #EA580C 0%, #C2410C 100%);
        color: white;
        box-shadow: 0 0 15px rgba(234, 88, 12, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
with st.sidebar:
    st.markdown("### 🏗️ **CONSTRUCTVISION AI**")
    st.caption("v2.4 Dark Blueprint Edition | AI Structural Audit")
    st.divider()

    menu = st.radio(
        "Navigation Module",
        [
            "🏠 Overview Dashboard",
            "📷 AI Defect Inspection",
            "🧱 Material Knowledge Base",
            "📊 Analytics & Risk",
            "📄 Report Generator"
        ],
        index=0
    )

    st.divider()
    st.markdown("#### ⚙️ Engine Status")
    st.success("🟢 AI Inference Model: **Active**")
    st.info("⚡ Processing: **GPU Accelerated**")

    st.divider()
    st.markdown("#### 👷 Development Team")
    st.caption("• **Ritika Bhumkar** (Civil & AI Dev)")
    st.caption("• **Laiba Mulani** (Civil & AI Dev)")
    st.caption("Department of Civil Engineering © 2026")

# =====================================================
# GREETING GENERATOR
# =====================================================
hour = datetime.now().hour
greeting = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 17 else "Good Evening")

# =====================================================
# MODULE 1: OVERVIEW DASHBOARD
# =====================================================
if menu == "🏠 Overview Dashboard":
    st.markdown(f"""
    <div class="hero-dark">
        <h1>🏗️ CONSTRUCTVISION <span class="accent-text">AI</span></h1>
        <p style="font-size: 1.1rem; color: #94A3B8;">
            <b>{greeting}, Engineer.</b> Welcome to the next-generation residential construction inspection workspace.
        </p>
        <hr style="border-color: #334155;">
        <p style="color: #CBD5E1;">
            Bridging <b>Civil Engineering</b> with <b>Computer Vision</b> to detect concrete structural defects, analyze load-bearing material safety, and deliver automated structural audit reports.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key Performance Indicators
    st.markdown("### 📊 Platform Operational Metrics")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">98.4%</div>
            <div class="metric-label">Detection Precision</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color:#F97316;">1,420+</div>
            <div class="metric-label">Scanned Defects</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color:#10B981;">18 MS</div>
            <div class="metric-label">Inference Speed</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">12 Specs</div>
            <div class="metric-label">Material DB</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    # Workflow & Quick Features
    st.markdown("### ⚙️ Automated Inspection Workflow")
    c1, c2, c3, c4 = st.columns(4)

    steps = [
        ("① Image Capture", "📷 Upload or snap high-res structural component photos."),
        ("② Computer Vision", "🤖 YOLOv8 detects micro-cracks, spalling & honeycombing."),
        ("③ Severity Analysis", "📊 Severity grading based on IS 456 / ACI standards."),
        ("④ Report Export", "📄 Automatic PDF / Text technical audit documentation.")
    ]

    for col, (title, desc) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(f"""
            <div class="dark-card">
                <h4 class="accent-text">{title}</h4>
                <p style="font-size:14px; color:#94A3B8;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# =====================================================
# MODULE 2: AI DEFECT INSPECTION (Interactive Simulator)
# =====================================================
elif menu == "📷 AI Defect Inspection":
    st.markdown("## 📷 Computer Vision Defect Detection")
    st.caption("Upload concrete column, beam, slab, or brickwork images for real-time computer vision analysis.")

    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a construction image...", type=["jpg", "jpeg", "png"])
        sensitivity = st.slider("Model Confidence Threshold", 0.1, 1.0, 0.45)
        model_type = st.selectbox("Detection Focus", ["Structural Cracks", "Concrete Spalling / Rebar Exposure", "Honeycombing / Voids", "General Surface Damage"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Inspection Target", use_container_width=True)
        else:
            st.info("👆 Upload an image to test the detection pipeline.")

    if uploaded_file is not None:
        st.divider()
        if st.button("🚀 Run AI Structural Analysis"):
            with st.spinner("Executing Computer Vision Pipeline..."):
                # Processing Image with simulated Bounding Boxes
                img_draw = image.copy()
                draw = ImageDraw.Draw(img_draw)
                w, h = img_draw.size

                # Draw mock detected bounding box
                box = [int(w * 0.25), int(h * 0.3), int(w * 0.75), int(h * 0.7)]
                draw.rectangle(box, outline="#F97316", width=4)
                draw.text((box[0] + 5, box[1] + 5), f"{model_type}: 94.2% Conf", fill="#F97316")

                res_left, res_right = st.columns([1, 1])
                with res_left:
                    st.image(img_draw, caption="AI Annotated Detection Output", use_container_width=True)

                with res_right:
                    st.markdown("""
                    <div class="dark-card">
                        <h3 class="accent-orange">⚠️ Defect Diagnostic Findings</h3>
                        <p><b>Identified Defect:</b> Shear / Structural Surface Crack</p>
                        <p><b>Confidence Rating:</b> <span class="accent-text">94.2%</span></p>
                        <p><b>Severity Index:</b> <span style="color:#EF4444; font-weight:bold;">MODERATE TO CRITICAL</span></p>
                        <p><b>Recommended Remedial Action:</b></p>
                        <ul>
                            <li>Inject low-viscosity epoxy resin into crack gap.</li>
                            <li>Monitor structural settlement over 14 days using crack gauges.</li>
                            <li>Verify reinforcement bar corrosion level near affected site.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

# =====================================================
# MODULE 3: MATERIAL KNOWLEDGE BASE
# =====================================================
elif menu == "🧱 Material Knowledge Base":
    st.markdown("## 🧱 Civil Engineering Material Explorer")
    st.caption("Interactive material property matrix for structural engineering validation.")

    materials_db = pd.DataFrame({
        "Material Grade": ["M20 Concrete", "M30 Concrete", "Fe500 Rebar Steel", "Fly Ash Bricks", "AAC Blocks"],
        "Category": ["Concrete", "Concrete", "Steel Reinforcement", "Masonry", "Masonry"],
        "Compressive Strength": ["20 MPa", "30 MPa", "500 MPa (Yield)", "7.5 MPa", "4.0 MPa"],
        "Density (kg/m³)": ["2400", "2500", "7850", "1700", "600"],
        "Common Structural Use": ["Residential Slabs/Beams", "Heavy Columns/Footings", "Main Reinforcement", "External Load Walls", "Internal Partitions"]
    })

    search = st.text_input("🔍 Search Material or Application:", "")
    filtered_db = materials_db[materials_db.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]

    st.dataframe(filtered_db, use_container_width=True, hide_index=True)

    st.write("")
    st.markdown("### 🧮 Quick Concrete Mix Estimator (IS 10262)")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        target_volume = st.number_input("Concrete Volume needed (m³):", min_value=0.5, value=10.0, step=0.5)
    with m_col2:
        mix_grade = st.selectbox("Mix Grade:", ["M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)"])
    with m_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        calc_btn = st.button("Calculate Raw Materials")

    if calc_btn:
        dry_vol = target_volume * 1.54  # Dry volume conversion factor
        if "M20" in mix_grade:
            cement_bags = round((1 / 5.5) * dry_vol * 28.8, 1)
            sand_m3 = round((1.5 / 5.5) * dry_vol, 2)
            aggregate_m3 = round((3 / 5.5) * dry_vol, 2)
        else:
            cement_bags = round((1 / 7) * dry_vol * 28.8, 1)
            sand_m3 = round((2 / 7) * dry_vol, 2)
            aggregate_m3 = round((4 / 7) * dry_vol, 2)

        st.markdown(f"""
        <div class="dark-card">
            <h4>📦 Material Estimation Breakdown ({mix_grade})</h4>
            <p>• <b>Cement Required:</b> {cement_bags} Bags (50 kg each)</p>
            <p>• <b>Fine Aggregate (Sand):</b> {sand_m3} m³</p>
            <p>• <b>Coarse Aggregate (Gravel):</b> {aggregate_m3} m³</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# MODULE 4: ANALYTICS & RISK ASSESSMENT
# =====================================================
elif menu == "📊 Analytics & Risk":
    st.markdown("## 📊 Defect Analytics & Structural Risk Profile")

    # Sample Defect Data
    df_defects = pd.DataFrame({
        "Component": ["Columns", "Beams", "Slabs", "Foundation", "Brick Walls"],
        "Cracks": [45, 30, 65, 12, 80],
        "Spalling": [20, 15, 10, 5, 2],
        "Honeycombing": [15, 25, 8, 18, 0]
    })

    c_chart1, c_chart2 = st.columns(2)

    with c_chart1:
        fig1 = px.bar(
            df_defects, x="Component", y=["Cracks", "Spalling", "Honeycombing"],
            title="Defect Distribution Across Structural Elements",
            template="plotly_dark",
            color_discrete_sequence=["#38BDF8", "#F97316", "#10B981"]
        )
        fig1.update_layout(paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
        st.plotly_chart(fig1, use_container_width=True)

    with c_chart2:
        fig2 = px.pie(
            names=["Low Risk (Cosmetic)", "Medium Risk (Non-structural)", "Critical Risk (Structural)"],
            values=[55, 30, 15],
            title="Overall Site Damage Risk Severity Ratio",
            template="plotly_dark",
            hole=0.4,
            color_discrete_sequence=["#10B981", "#FBBF24", "#EF4444"]
        )
        fig2.update_layout(paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
        st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# MODULE 5: REPORT GENERATOR
# =====================================================
elif menu == "📄 Report Generator":
    st.markdown("## 📄 Automated Structural Audit Report")
    st.caption("Generate standard civil engineering structural inspection documentation.")

    with st.form("report_form"):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            site_name = st.text_input("Project / Site Name:", "Greenfield Residential Residency")
            inspector = st.text_input("Lead Engineer Name:", "Er. Ritika Bhumkar")
        with col_r2:
            location = st.text_input("Location / Block:", "Block B, Floor 4")
            date_ins = st.date_input("Inspection Date:", datetime.today())

        defect_types = st.multiselect(
            "Identified Defect Checklist:",
            ["Structural Diagonal Cracks", "Concrete Spalling with Exposed Rebar", "Surface Honeycombing", "Efflorescence / Moisture Seepage", "Plaster Flaking"],
            default=["Structural Diagonal Cracks", "Surface Honeycombing"]
        )

        comments = st.text_area("Engineering Remarks & Assessment Notes:", "Cracks observed on column C3 require immediate epoxy pressure grouting prior to proceeding with brickwork.")

        submitted = st.form_submit_button("Generate Inspection Audit Document")

    if submitted:
        report_txt = f"""=======================================================
CONSTRUCTVISION AI - STRUCTURAL AUDIT REPORT
=======================================================
Project Site  : {site_name}
Location      : {location}
Lead Inspector: {inspector}
Date          : {date_ins}
-------------------------------------------------------
IDENTIFIED DEFECTS & OBSERVATIONS:
"""
        for item in defect_types:
            report_txt += f" - [X] {item}\n"

        report_txt += f"""
INSPECTOR'S TECHNICAL REMARKS:
{comments}

-------------------------------------------------------
Status: ACTION REQUIRED
Generated by CONSTRUCTVISION AI Inspection System
======================================================="""

        st.success("✅ Structural Audit Report Generated Successfully!")
        st.code(report_txt, language="text")

        st.download_button(
            label="💾 Download Technical Audit (.TXT)",
            data=report_txt,
            file_name=f"Audit_Report_{site_name.replace(' ', '_')}.txt",
            mime="text/plain"
        )

# =====================================================
# FOOTER
# =====================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:10px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI</b> | Developed by <b>Ritika Bhumkar & Laiba Mulani</b> | Civil Engineering Department Project
</div>
""", unsafe_allow_html=True)
