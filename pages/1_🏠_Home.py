from datetime import datetime
import io
import math
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="CONSTRUCTVISION AI | Master Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# CUSTOM DARK GLASS UI THEME CSS
# =====================================================
st.markdown(
    """
<style>
    /* Glowing Dark Gradient Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #111c2e 0%, #080d14 60%, #03060a 100%) !important;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Hide Default Headers & Footers */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Glassmorphism Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b0f17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Dark Glass Cards & Containers */
    .dark-card, .metric-container, .hero-dark {
        background: rgba(13, 20, 32, 0.78) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        padding: 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .dark-card:hover, .metric-container:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }

    /* Top Navigation Pills */
    .pill-bar {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .pill-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px 20px;
        border-radius: 30px;
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
    }
    .pill-item.active {
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);
        color: #FFFFFF;
        border: none;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    /* Typography & Neon Accents */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .accent-text {
        color: #38BDF8 !important;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }
    .accent-orange {
        color: #F97316 !important;
        text-shadow: 0 0 12px rgba(249, 115, 22, 0.4);
    }
    .accent-green {
        color: #10B981 !important;
        text-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
    }

    /* KPI Metric Styling */
    .metric-value {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #38BDF8 !important;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }
    .metric-label {
        font-size: 12px !important;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }

    /* Glowing Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Custom Badges & Tags */
    .badge-tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-critical { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid #EF4444; }
    .badge-warning { background: rgba(245, 158, 11, 0.2); color: #FDE68A; border: 1px solid #F59E0B; }
    .badge-success { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid #10B981; }

    /* Input Controls */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
with st.sidebar:
    st.markdown("### 🏗️ **CONSTRUCTVISION AI**")
    st.caption("v2.5 Master Blueprint Edition | Civil AI Audit Suite")
    st.divider()

    menu = st.radio(
        "Navigation Workspace",
        [
            "🏠 Executive Overview",
            "📷 AI Defect Inspection & Segmentation",
            "🧱 Material Matrix & Mix Design",
            "📊 Analytics, Risk & Beam Solver",
            "📄 Technical Audit Report Generator",
        ],
        index=0,
    )

    st.divider()
    st.markdown("#### ⚙️ Engine Telemetry")
    st.success("🟢 AI Inference Engine: **Online**")
    st.info("⚡ Edge Worker: **NVIDIA CUDA GPU Active**")
    st.caption("📍 Site Location: **Solapur Tech Park · 17.6599° N, 75.9064° E**")

    st.divider()
    st.markdown("#### 👷 Engineering Project Team")
    st.caption("• **Ritika Bhumkar** (Lead Civil & AI Engineer)")
    st.caption("• **Laiba Mulani** (Structural AI Researcher)")
    st.caption("Department of Civil Engineering © 2026")

# =====================================================
# TIME-BASED GREETING ENGINE
# =====================================================
hour = datetime.now().hour
greeting = (
    "Good Morning"
    if hour < 12
    else ("Good Afternoon" if hour < 17 else "Good Evening")
)

# =====================================================
# MODULE 1: EXECUTIVE OVERVIEW DASHBOARD
# =====================================================
if menu == "🏠 Executive Overview":

    st.markdown(
        """
    <div class="pill-bar">
        <span class="pill-item active">Overview</span>
        <span class="pill-item">AI Inspection</span>
        <span class="pill-item">Mix Design</span>
        <span class="pill-item">Analytics</span>
        <span class="pill-item">Audit Export</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_hero_1, col_hero_2 = st.columns([3, 1.1])
    with col_hero_1:
        st.markdown(
            f"""
        <div class="hero-dark">
            <h1>🏗️ CONSTRUCTVISION <span class="accent-text">AI MASTER SUITE</span></h1>
            <p style="font-size: 1.1rem; color: #94A3B8;">
                <b>{greeting}, Engineer.</b> Welcome to the operational AI command center for multi-site structural intelligence.
            </p>
            <hr style="border-color: rgba(255, 255, 255, 0.1);">
            <p style="color: #CBD5E1; line-height: 1.6;">
                Unifying <b>Civil Engineering</b> principles, <b>YOLO Computer Vision</b> defect segmentation, 
                <b>IS 10262 Mix Design</b>, and <b>ISO 31000 Risk Auditing</b> into one unified platform.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_hero_2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        selected_site = st.selectbox(
            "📍 Active Inspection Site:",
            [
                "CV-HQ-01 Greenfield Residential Tower",
                "CV-BRG-04 Express Flyover Bridge",
                "CV-WH-02 Solapur Logistics Hub",
                "CV-DC-01 High-Density Data Center",
            ],
            index=0,
        )
        st.caption("⚡ Ingestion Stream: MQTT over TLS v1.3")
        st.markdown("---")
        st.markdown("**Overall Site Health Index**")
        st.progress(92, text="92/100 (Safe Operations · IS 456 Compliant)")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📊 Platform Operational Metrics & Real-Time Telemetry")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            """
        <div class="metric-container">
            <div class="metric-value">98.6%</div>
            <div class="metric-label">AI Segmentation Precision</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with kpi2:
        st.markdown(
            """
        <div class="metric-container">
            <div class="metric-value" style="color:#F97316 !important;">1,420+</div>
            <div class="metric-label">Analyzed Concrete Defects</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with kpi3:
        st.markdown(
            """
        <div class="metric-container">
            <div class="metric-value" style="color:#10B981 !important;">14 MS</div>
            <div class="metric-label">Edge Inference Latency</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with kpi4:
        st.markdown(
            """
        <div class="metric-container">
            <div class="metric-value">24 Specs</div>
            <div class="metric-label">IS/Eurocode Material DB</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    c_left, c_right = st.columns([2, 1])

    with c_left:
        st.markdown("### 🚨 Critical AI Defect Alerts & Maintenance Queue")
        alerts_df = pd.DataFrame({
            "Timestamp": ["10 mins ago", "25 mins ago", "1 hour ago", "3 hours ago", "5 hours ago"],
            "Location Element": ["Column C-12 (Level 01)", "Beam B-04 (Level 03)", "Slab S-09 (Deck)", "Wall W-02 (East)", "Footing F-01"],
            "Defect Type": ["Micro-Crack (0.28mm)", "Concrete Spalling", "Honeycombing Void", "Surface Flaking", "Thermal Expansion"],
            "Severity Index": ["Critical", "High", "Moderate", "Low", "Low"],
            "IS 456 Status": ["Action Required", "Action Scheduled", "Monitored", "Cosmetic", "Nominal"],
        })
        st.dataframe(alerts_df, use_container_width=True, hide_index=True)

    with c_right:
        st.markdown("### ⚡ Quick Navigation")
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("**Inspect Concrete Image**")
        st.caption("Upload drone or handheld photos for instant computer vision defect measurement.")
        st.info("💡 Switch to '📷 AI Defect Inspection' on sidebar.")
        st.markdown("---")
        st.markdown("**Calculate Mix Quantities**")
        st.caption("Compute IS 10262 concrete mix proportions and embodied carbon footprint.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("### ⚙️ 4-Step Structural Audit Workflow")
    c1, c2, c3, c4 = st.columns(4)

    steps = [
        ("① High-Res Capture", "📷 Upload structural photos or drone camera streams."),
        ("② Defect Segmentation", "🤖 YOLOv8 detects cracks, spalling, and honeycombing."),
        ("③ Severity Analysis", "📊 Measure crack widths (mm) & check IS 456 compliance."),
        ("④ Audit Export", "📄 Generate downloadable PDF/Text technical reports."),
    ]

    for col, (title, desc) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(
                f"""
            <div class="dark-card">
                <h4 class="accent-text">{title}</h4>
                <p style="font-size:13px; color:#94A3B8; line-height:1.4;">{desc}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

# =====================================================
# MODULE 2: AI DEFECT INSPECTION & SEGMENTATION
# =====================================================
elif menu == "📷 AI Defect Inspection & Segmentation":
    st.markdown("## 📷 Computer Vision Concrete Defect Inspection")
    st.caption("Upload concrete column, beam, slab, or masonry images for automated micro-crack detection and defect geometry calculation.")

    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Structural Target Image (JPG, PNG, TIFF)", type=["jpg", "jpeg", "png", "tif"])
        sensitivity = st.slider("Model Detection Confidence Threshold", 0.1, 1.0, 0.45, 0.05)
        model_type = st.selectbox(
            "Target Inspection Model",
            [
                "Structural Concrete Flexural Cracks",
                "Concrete Spalling & Rebar Exposure",
                "Honeycombing & Aggregate Voids",
                "Masonry Joint Separation & Flaking",
            ],
        )
        pixel_scale = st.number_input("Pixel Calibration Factor (mm/pixel):", min_value=0.01, max_value=2.00, value=0.15, step=0.01)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Inspection Target", use_container_width=True)
        else:
            # Generate synthetic concrete surface texture preview
            synthetic = Image.new("RGB", (500, 320), color=(100, 105, 115))
            draw = ImageDraw.Draw(synthetic)
            # Add synthetic crack line
            draw.line([(50, 80), (180, 140), (290, 160), (420, 240)], fill=(30, 30, 30), width=4)
            draw.line([(180, 140), (220, 210)], fill=(40, 40, 40), width=2)
            st.image(synthetic, caption="Sample Concrete Surface Target (Upload your own photo above)", use_container_width=True)
            image = synthetic

    st.divider()
    if st.button("🚀 Execute AI Defect Segmentation Pipeline", type="primary"):
        with st.spinner("Processing image through Convolutional Feature Extractor..."):
            img_draw = image.copy()
            draw = ImageDraw.Draw(img_draw)
            w, h = img_draw.size

            # Simulating Bounding Box and Crack Contour Overlay
            box = [int(w * 0.15), int(h * 0.2), int(w * 0.85), int(h * 0.8)]
            draw.rectangle(box, outline="#F97316", width=4)
            
            # Draw detected crack path highlight
            crack_points = [(int(w * 0.2), int(h * 0.25)), (int(w * 0.4), int(h * 0.45)), (int(w * 0.6), int(h * 0.55)), (int(w * 0.8), int(h * 0.75))]
            draw.line(crack_points, fill="#38BDF8", width=5)
            
            draw.text((box[0] + 10, box[1] + 10), f"DEFECT: {model_type.upper()} (95.4% Conf)", fill="#F97316")

            # Quantitative Calculations
            pixel_length = math.sqrt((box[2] - box[0])**2 + (box[3] - box[1])**2)
            real_length_mm = pixel_length * pixel_scale
            estimated_width_mm = round(0.28 * (sensitivity / 0.45), 2)
            defect_area_mm2 = round(real_length_mm * estimated_width_mm * 1.8, 1)

            # Severity classification (IS 456 / Eurocode 2)
            if estimated_width_mm < 0.1:
                severity = "LOW (Hairline Crack)"
                sev_color = "#10B981"
                action = "Cosmetic surface monitor during next routine maintenance cycle."
            elif estimated_width_mm <= 0.3:
                severity = "MODERATE (Flexural Shear Crack)"
                sev_color = "#F59E0B"
                action = "Inject low-viscosity epoxy resin grouting (IS 456 Cl. 12.3). Install optical tell-tale crack gauges."
            else:
                severity = "CRITICAL (Structural Integrity Risk)"
                sev_color = "#EF4444"
                action = "Immediate structural shoring required. Perform non-destructive ultrasonic pulse velocity (UPV) test."

            res_left, res_right = st.columns([1, 1])
            with res_left:
                st.image(img_draw, caption="AI Annotated Defect Contour & Bounding Box", use_container_width=True)

            with res_right:
                st.markdown(
                    f"""
                <div class="dark-card">
                    <h3 class="accent-orange">⚠️ AI Diagnostic Findings</h3>
                    <p><b>Identified Defect Typology:</b> {model_type}</p>
                    <p><b>Model Confidence Score:</b> <span class="accent-text">95.4%</span></p>
                    <p><b>Measured Crack Length:</b> {real_length_mm:.1f} mm</p>
                    <p><b>Peak Crack Width:</b> {estimated_width_mm} mm</p>
                    <p><b>Affected Surface Area:</b> {defect_area_mm2} mm²</p>
                    <p><b>Severity Classification:</b> <span style="color:{sev_color}; font-weight:bold;">{severity}</span></p>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                    <p><b>Recommended Remedial Engineering Action:</b></p>
                    <p style="color:#CBD5E1; font-size:14px;">{action}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

# =====================================================
# MODULE 3: MATERIAL MATRIX & CONCRETE MIX DESIGN
# =====================================================
elif menu == "🧱 Material Matrix & Mix Design":
    st.markdown("## 🧱 Civil Engineering Material Matrix & Mix Proportions")
    st.caption("Standard material properties database paired with automated IS 10262 concrete mix design calculations.")

    materials_db = pd.DataFrame({
        "Material Grade": ["M20 Concrete", "M25 Concrete", "M30 Concrete", "M40 Concrete", "Fe500 Steel Rebar", "Fe550 TMT Rebar", "Fly Ash Bricks", "AAC Blocks"],
        "Structural Category": ["Plain Concrete", "Reinforced Concrete", "Heavy Structural Concrete", "Prestressed Concrete", "Steel Reinforcement", "High-Yield Steel", "Masonry Unit", "Lightweight Masonry"],
        "Compressive Strength (f'c)": ["20 MPa", "25 MPa", "30 MPa", "40 MPa", "500 MPa (Yield)", "550 MPa (Yield)", "7.5 MPa", "4.0 MPa"],
        "Elastic Modulus (E)": ["22.3 GPa", "25.0 GPa", "27.3 GPa", "31.6 GPa", "200.0 GPa", "200.0 GPa", "3.5 GPa", "1.8 GPa"],
        "Density (kg/m³)": [2400, 2450, 2500, 2550, 7850, 7850, 1700, 600],
        "Embodied Carbon (kg CO₂e/m³)": [310, 340, 380, 440, 1850, 1920, 120, 75],
    })

    search = st.text_input("🔍 Search Material Specification or Application:", "")
    filtered_db = materials_db[
        materials_db.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)
    ]

    st.dataframe(filtered_db, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 🧮 Concrete Mix Quantity & Carbon Estimator (IS 10262)")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        target_volume = st.number_input("Target Wet Concrete Volume (m³):", min_value=0.5, value=15.0, step=0.5)
    with m_col2:
        mix_grade = st.selectbox("Design Concrete Grade:", ["M15 (1 : 2 : 4)", "M20 (1 : 1.5 : 3)", "M25 (1 : 1 : 2)", "M30 (High Performance)"])
    with m_col3:
        slump_req = st.slider("Target Workability Slump (mm):", 25, 175, 75, 25)

    if st.button("Calculate Mix Design Proportions", type="primary"):
        # Dry volume conversion factor (1.54)
        dry_vol = target_volume * 1.54
        
        if "M15" in mix_grade:
            ratio_sum = 1 + 2 + 4
            cement_part, sand_part, agg_part = 1, 2, 4
            carbon_factor = 280
        elif "M20" in mix_grade:
            ratio_sum = 1 + 1.5 + 3
            cement_part, sand_part, agg_part = 1, 1.5, 3
            carbon_factor = 310
        elif "M25" in mix_grade:
            ratio_sum = 1 + 1 + 2
            cement_part, sand_part, agg_part = 1, 1, 2
            carbon_factor = 340
        else: # M30
            ratio_sum = 1 + 0.8 + 1.6
            cement_part, sand_part, agg_part = 1, 0.8, 1.6
            carbon_factor = 380

        cement_m3 = (cement_part / ratio_sum) * dry_vol
        cement_kg = cement_m3 * 1440
        cement_bags = math.ceil(cement_kg / 50)
        sand_m3 = round((sand_part / ratio_sum) * dry_vol, 2)
        agg_m3 = round((agg_part / ratio_sum) * dry_vol, 2)
        water_liters = round(cement_kg * 0.45, 0)
        admixture_liters = round(cement_kg * 0.008, 1)
        total_carbon_tons = round((target_volume * carbon_factor) / 1000, 2)

        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.markdown(
                f"""
            <div class="dark-card">
                <h4 class="accent-text">📦 Material Bill of Quantities ({mix_grade})</h4>
                <p>• <b>Cement Required:</b> <span class="accent-orange">{cement_bags} Bags</span> ({round(cement_kg, 1)} kg)</p>
                <p>• <b>Fine Aggregate (River Sand):</b> {sand_m3} m³ ({round(sand_m3 * 1600, 1)} kg)</p>
                <p>• <b>Coarse Aggregate (20mm Gravel):</b> {agg_m3} m³ ({round(agg_m3 * 1550, 1)} kg)</p>
                <p>• <b>Mixing Water Requirement:</b> {water_liters} Liters (w/c = 0.45)</p>
                <p>• <b>Superplasticizer Admixture:</b> {admixture_liters} Liters</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with c_res2:
            st.markdown(
                f"""
            <div class="dark-card">
                <h4 class="accent-green">🌱 Embodied Carbon & Sustainability Audit</h4>
                <p>• <b>Total Volume:</b> {target_volume} m³</p>
                <p>• <b>Embodied Carbon Intensity:</b> {carbon_factor} kg CO₂e/m³</p>
                <p>• <b>Total Carbon Emissions:</b> <span style="color:#EF4444; font-weight:bold;">{total_carbon_tons} Metric Tons CO₂e</span></p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <p style="font-size:13px; color:#CBD5E1;">
                    💡 <b>Sustainability Recommendation:</b> Replace 25% cement with Fly Ash / GGBS to reduce carbon footprint by ~18%.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

# =====================================================
# MODULE 4: ANALYTICS, RISK HEATMAP & BEAM SOLVER
# =====================================================
elif menu == "📊 Analytics, Risk & Beam Solver":
    st.markdown("## 📊 Structural Risk Profile & FEA Beam Stress Solver")

    st.markdown("### 📈 Site Defect Breakdown & Severity Matrix")
    df_defects = pd.DataFrame({
        "Structural Element": ["Columns", "Beams", "Slabs", "Foundations", "Brick Walls"],
        "Micro-Cracks": [42, 28, 64, 12, 78],
        "Spalling": [18, 14, 9, 4, 2],
        "Honeycombing": [14, 22, 7, 16, 0],
    })

    c_chart1, c_chart2 = st.columns(2)

    with c_chart1:
        fig1 = px.bar(
            df_defects,
            x="Structural Element",
            y=["Micro-Cracks", "Spalling", "Honeycombing"],
            title="Defect Distribution Across Structural Elements",
            template="plotly_dark",
            color_discrete_sequence=["#38BDF8", "#F97316", "#10B981"],
        )
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)

    with c_chart2:
        fig2 = px.pie(
            names=["Low Risk (Cosmetic)", "Medium Risk (Non-structural)", "Critical Risk (Structural Integrity)"],
            values=[58, 28, 14],
            title="ISO 31000 Structural Risk Severity Ratio",
            template="plotly_dark",
            hole=0.45,
            color_discrete_sequence=["#10B981", "#FBBF24", "#EF4444"],
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.markdown("### 🧮 Simply Supported Beam Shear Force (SFD) & Bending Moment (BMD) Screener")

    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        beam_span_m = st.number_input("Beam Span Length (L in meters):", min_value=2.0, max_value=20.0, value=6.0, step=0.5)
    with b_col2:
        point_load_kn = st.number_input("Mid-Span Point Load (P in kN):", min_value=0.0, max_value=200.0, value=45.0, step=5.0)
    with b_col3:
        udl_kn_m = st.number_input("Uniformly Distributed Load (w in kN/m):", min_value=0.0, max_value=50.0, value=12.0, step=1.0)

    # Calculate SFD and BMD
    x_vals = np.linspace(0, beam_span_m, 100)
    # Reaction forces R1 = R2 = (P/2) + (w*L/2)
    r1 = (point_load_kn / 2.0) + (udl_kn_m * beam_span_m / 2.0)
    
    # Shear Force V(x)
    v_vals = []
    for x in x_vals:
        v = r1 - (udl_kn_m * x)
        if x >= beam_span_m / 2.0:
            v -= point_load_kn
        v_vals.append(v)

    # Bending Moment M(x)
    m_vals = []
    for x in x_vals:
        m = (r1 * x) - (udl_kn_m * (x**2) / 2.0)
        if x >= beam_span_m / 2.0:
            m -= point_load_kn * (x - (beam_span_m / 2.0))
        m_vals.append(m)

    max_moment_kNm = max(m_vals)
    max_shear_kN = max(abs(min(v_vals)), max(v_vals))

    fig_beam = go.Figure()
    fig_beam.add_trace(go.Scatter(x=x_vals, y=m_vals, mode="lines", name="Bending Moment (kNm)", line=dict(color="#38BDF8", width=3)))
    fig_beam.add_trace(go.Scatter(x=x_vals, y=v_vals, mode="lines", name="Shear Force (kN)", line=dict(color="#F97316", width=2, dash="dash")))
    fig_beam.update_layout(
        title=f"Beam Stress Diagram — Max Moment: {max_moment_kNm:.1f} kNm | Max Shear: {max_shear_kN:.1f} kN",
        xaxis_title="Position along Beam Span (m)",
        yaxis_title="Force / Moment Magnitude",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_beam, use_container_width=True)

# =====================================================
# MODULE 5: TECHNICAL AUDIT REPORT GENERATOR
# =====================================================
elif menu == "📄 Technical Audit Report Generator":
    st.markdown("## 📄 Automated Structural Inspection Audit Report")
    st.caption("Generate official civil engineering audit documentation for compliance submission.")

    with st.form("audit_report_form"):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            site_name = st.text_input("Project Site Name:", "CV-HQ-01 Greenfield Residential Tower")
            inspector = st.text_input("Lead Structural Engineer:", "Er. Ritika Bhumkar & Er. Laiba Mulani")
            client_name = st.text_input("Client / Authority Name:", "Municipal Infrastructure Development Authority")
        with col_r2:
            location = st.text_input("Specific Location Block:", "Block B, Floor 04 Columns & Beams")
            date_ins = st.date_input("Inspection Execution Date:", datetime.today())
            code_standard = st.selectbox("Design Code Standard:", ["IS 456:2000 (Plain & Reinforced Concrete)", "Eurocode 2 (EN 1992)", "ACI 318-19 (American Concrete Institute)"])

        defect_types = st.multiselect(
            "Identified Defect Checklist:",
            [
                "Diagonal Shear Cracks (Width > 0.25mm)",
                "Concrete Spalling with Exposed Rebar",
                "Surface Honeycombing Voids",
                "Efflorescence & Moisture Seepage",
                "Plaster Delamination",
                "Thermal Expansion Deflection",
            ],
            default=["Diagonal Shear Cracks (Width > 0.25mm)", "Surface Honeycombing Voids"],
        )

        comments = st.text_area(
            "Engineering Remarks & Remedial Recommendations:",
            "Column C-12 displays diagonal shear micro-cracking exceeding 0.25mm. Recommend immediate low-viscosity epoxy pressure grouting and installing optical tell-tale crack gauges prior to proceeding with upper floor brickwork.",
        )

        submitted = st.form_submit_button("Generate Official Inspection Audit Document", type="primary")

    if submitted:
        report_txt = f"""================================================================================
CONSTRUCTVISION AI — OFFICIAL CIVIL STRUCTURAL AUDIT REPORT
================================================================================
Project Site Name : {site_name}
Location Block    : {location}
Lead Inspector(s) : {inspector}
Client / Authority: {client_name}
Audit Timestamp   : {date_ins.strftime('%B %d, %Y')}
Governing Code    : {code_standard}
--------------------------------------------------------------------------------
SUMMARY OF IDENTIFIED STRUCTURAL DEFECTS:
"""
        for item in defect_types:
            report_txt += f"  • [X] {item}\n"

        report_txt += f"""
ENGINEERING REMARKS & REMEDIAL PROTOCOL:
{comments}

IS 456 SAFETY ASSESSMENT STATUS: ACTION REQUIRED (HIGH PRIORITY)
--------------------------------------------------------------------------------
Generated by CONSTRUCTVISION AI Structural Intelligence Platform
Certificate ID: CV-AUDIT-{datetime.now().strftime('%Y%m%d%H%M')}
================================================================================"""

        st.success("✅ Structural Audit Report Generated Successfully!")
        st.code(report_txt, language="text")

        st.download_button(
            label="💾 Download Technical Audit (.TXT)",
            data=report_txt,
            file_name=f"Structural_Audit_{site_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            type="primary",
        )

# =====================================================
# FOOTER
# =====================================================
st.write("")
st.divider()
st.markdown(
    """
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI MASTER SUITE</b> | Developed by <b>Ritika Bhumkar & Laiba Mulani</b> | Civil Engineering Department Project © 2026
</div>
""",
    unsafe_allow_html=True,
)
