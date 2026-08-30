from datetime import date, datetime
import json
import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION & DARK GLASS THEME
# =========================================================
st.set_page_config(
    page_title="Central AI Inspection Report & Multi-Module Audit Hub | CONSTRUCTVISION AI",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Glass UI CSS
st.markdown("""
<style>
    /* Glowing Dark Background Gradient */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #172437 0%, #080D14 60%, #03060A 100%) !important;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit Default UI Chrome */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Dark Glass Cards & Containers */
    .dark-card, .report-card, .invoice-box {
        background: rgba(13, 20, 32, 0.82) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        padding: 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .dark-card:hover, .report-card:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }

    /* Header Banner */
    .report-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 24px 30px;
        border-radius: 16px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }

    /* Typography & Accents */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .accent-cyan { color: #38BDF8 !important; text-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }
    .accent-orange { color: #F97316 !important; text-shadow: 0 0 12px rgba(249, 115, 22, 0.4); }
    .accent-green { color: #10B981 !important; text-shadow: 0 0 12px rgba(16, 185, 129, 0.4); }
    .accent-red { color: #EF4444 !important; text-shadow: 0 0 12px rgba(239, 68, 68, 0.4); }

    /* Custom Badges & Chips */
    .badge-blue { background: rgba(37, 99, 235, 0.25); color: #60A5FA; border: 1px solid #2563EB; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-success { background: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-warning { background: rgba(249, 115, 22, 0.25); color: #FDBA74; border: 1px solid #F97316; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-critical { background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }

    .material-chip {
        display: inline-block;
        background-color: rgba(15, 23, 42, 0.8);
        color: #38BDF8 !important;
        border: 1px solid #0284C7;
        padding: 5px 12px;
        margin: 3px;
        border-radius: 16px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Timeline Nodes */
    .timeline-item {
        border-left: 3px solid #38BDF8;
        padding-left: 16px;
        margin-bottom: 14px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 0;
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background-color: #38BDF8;
        box-shadow: 0 0 10px #38BDF8;
    }

    /* Custom Streamlit Buttons */
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
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. CROSS-MODULE SESSION STATE DATA INGESTION ENGINE
# =========================================================

# 1. GPS Site Location (from 4_📍_GPS_Location.py)
gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road",
    "type": "Commercial High-Rise",
    "risk_score": 88
})

# 2. AI Inspection Results (from 5_🔬_AI_Inspection.py)
inspection_payload = st.session_state.get("latest_inspection", None)

# 3. 3D Twin Active Member (from 7_🏗️_3D_Building.py)
if "selected_component" not in st.session_state:
    st.session_state.selected_component = "RCC Support Column (C-12)"

# 4. Live Sensor History (from 8_📡_IoT.py)
sensor_history = st.session_state.get("sensor_history", {})

# Benchmark Fallback Generator if no live scan run yet
if not inspection_payload:
    benchmark_defects = [
        {
            "Defect ID": "DEF-01",
            "Typology": "Reinforced Concrete Column (C-12)",
            "Defect Category": "Flexural & Shear Cracks",
            "Length (mm)": 185.5,
            "Max Width (mm)": 0.38,
            "Area (mm²)": 128.4,
            "Severity": "CRITICAL (Grade III)",
            "Confidence": "98.4%",
            "Recommended Action": "Structural shoring & low-viscosity epoxy pressure injection grouting (IS 456 Cl 12.3).",
            "Estimated Cost (₹)": 28400,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "Defect ID": "DEF-02",
            "Typology": "Flexural Concrete Beam (B-04)",
            "Defect Category": "Flexural Micro-Crack",
            "Length (mm)": 120.0,
            "Max Width (mm)": 0.22,
            "Area (mm²)": 74.2,
            "Severity": "MODERATE (Grade II)",
            "Confidence": "94.2%",
            "Recommended Action": "Resin sealing & tell-tale optical displacement monitoring.",
            "Estimated Cost (₹)": 17800,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "Defect ID": "DEF-03",
            "Typology": "Floor Slab Soffit (S-09)",
            "Defect Category": "Honeycombing Voids",
            "Length (mm)": 65.0,
            "Max Width (mm)": 0.12,
            "Area (mm²)": 35.0,
            "Severity": "NOMINAL (Grade I)",
            "Confidence": "88.6%",
            "Recommended Action": "Polymer mortar patch surface rendering.",
            "Estimated Cost (₹)": 9500,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

    inspection_payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "site_code": gps_info.get("site_code", "CV-RES-01"),
        "location": gps_info.get("label", "Navi Peth Commercial Center"),
        "gps": f"{gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E",
        "total_defects": len(benchmark_defects),
        "max_crack_width_mm": 0.38,
        "verdict": "CRITICAL HAZARD ALERT",
        "defects_list": benchmark_defects,
        "total_repair_cost_inr": 55700
    }

defects_list = inspection_payload.get("defects_list", [])
max_crack_mm = inspection_payload.get("max_crack_width_mm", 0.38)
total_repair_inr = inspection_payload.get("total_repair_cost_inr", 55700)
overall_verdict = inspection_payload.get("verdict", "CRITICAL HAZARD ALERT")

# Generate Synthetic Proof Frame
def generate_proof_frame():
    img = Image.new("RGB", (800, 480), color="#0F172A")
    d = ImageDraw.Draw(img)
    # Draw concrete substrate face
    d.rectangle([60, 60, 740, 420], fill="#1E293B", outline="#334155", width=2)
    # Draw shear crack path
    d.line([180, 120, 320, 220, 440, 290, 580, 380], fill="#EF4444", width=5)
    d.line([320, 220, 410, 240], fill="#F97316", width=3)
    # Draw AI bounding box
    d.rectangle([160, 100, 600, 400], outline="#38BDF8", width=3)
    d.rectangle([160, 75, 450, 100], fill="#0284C7")
    d.text((170, 80), f"YOLOv8 DETECTED: #01 Shear Crack ({max_crack_mm:.2f}mm) 98.4%", fill="#FFFFFF")
    return img

proof_img = generate_proof_frame()

# Historical Archive Dataset Setup
@st.cache_data
def load_historical_logs():
    return [
        {
            "Record_ID": "INSP-2026-0901",
            "Date": date(2026, 8, 22),
            "Project": f"{gps_info.get('site_code','CV-RES-01')}: {gps_info.get('label','Navi Peth Center')}",
            "Inspection_Type": "Model & Sensor Calibration Audit",
            "Inspector": "Er. Ritika Bhumkar & Er. Laiba Mulani",
            "Defects_Found": 0,
            "AI_Confidence": 0.99,
            "Status": "Safe",
            "Severity": "None",
            "Notes": "Solapur HQ core repository model sync verified. Sub-pixel scale calibrated to 0.15 mm/px."
        },
        {
            "Record_ID": "INSP-2026-0899",
            "Date": date(2026, 8, 18),
            "Project": "CV-RES-01: Navi Peth Commercial Center",
            "Inspection_Type": "Structural Integrity & Rebar Scan",
            "Inspector": "Er. Ritika Bhumkar (Lead Dev)",
            "Defects_Found": 2,
            "AI_Confidence": 0.96,
            "Status": "Review Required",
            "Severity": "Medium",
            "Notes": "0.28mm flexural shear crack noted near Column C-12 Level 1 joint. Epoxy grouting scheduled."
        },
        {
            "Record_ID": "INSP-2026-0891",
            "Date": date(2026, 8, 14),
            "Project": "CV-FLY-03: Saat Rasta Traffic Flyover",
            "Inspection_Type": "Concrete Deck Shear & Crack Scan",
            "Inspector": "Er. Laiba Mulani (Lead Dev)",
            "Defects_Found": 4,
            "AI_Confidence": 0.94,
            "Status": "Critical Alert",
            "Severity": "High",
            "Notes": "Concrete spalling with rebar exposure near Pier 2 base. Immediate shoring and polymer mortar patching required."
        }
    ]

preset_logs = load_historical_logs()

# Merge current session scan
all_logs = []
all_logs.append({
    "Record_ID": f"LIVE-{datetime.now().strftime('%Y%m%d-%H%M')}",
    "Date": datetime.now().date(),
    "Project": f"{gps_info.get('site_code','CV-SITE')}: {gps_info.get('label','Solapur Site')}",
    "Inspection_Type": "Live Computer Vision AI & Multi-Module Audit",
    "Inspector": "Er. Ritika Bhumkar & Er. Laiba Mulani",
    "Defects_Found": len(defects_list),
    "AI_Confidence": 0.984,
    "Status": "Critical Alert" if "CRITICAL" in overall_verdict.upper() else "Safe",
    "Severity": "High" if max_crack_mm > 0.3 else "Medium",
    "Notes": f"Live inspection verdict: {overall_verdict}. Max crack width: {max_crack_mm:.2f} mm. Est Cost: ₹{total_repair_inr:,.0f}"
})
all_logs.extend(preset_logs)
df_logs = pd.DataFrame(all_logs)

# Initialize Session Report History if needed
if "report_history" not in st.session_state:
    st.session_state.report_history = all_logs

# =========================================================
# 3. SIDEBAR CONTROLS & ORIGIN STORY TOGGLE
# =========================================================
with st.sidebar:
    st.markdown("### 📜 **Audit History Controls**")
    st.caption("Centralized Multi-Module Master Audit Engine")
    st.divider()

    show_genesis_story = st.checkbox("💡 Show Project Creation Story", value=True)
    st.divider()

    st.markdown("#### 🔗 Linked Active Target")
    st.caption(f"• **Active Site:** `{gps_info.get('site_code','CV-SITE')}`")
    st.caption(f"• **Location:** `{gps_info.get('label','Solapur Site')}`")
    st.caption(f"• **3D Member Focus:** `{st.session_state.selected_component}`")
    st.caption(f"• **Peak Crack:** `{max_crack_mm:.2f} mm`")

    st.divider()
    st.caption("Department of Civil Engineering © 2026")

# =========================================================
# 4. MASTER REPORT HEADER
# =========================================================
st.markdown(f"""
<div class="report-header">
    <div>
        <h1 style="margin:0; font-size: 2.1rem; font-weight: 800;" class="accent-cyan">
            📄 Central AI Inspection Report & Master Audit Hub
        </h1>
        <p style="margin: 4px 0 0 0; font-size: 1.05rem; color: #94A3B8;">
            CONSTRUCTVISION AI — Unified Multi-Module Quality Assurance & Civil Engineering Audit
        </p>
    </div>
    <div style="text-align: right;">
        <span class="badge-blue">SYSTEM ARCHITECTS & LEAD DEVELOPERS</span>
        <p style="margin: 4px 0 0 0; font-size: 0.95rem; font-weight: 600; color: #FFFFFF;">
            Er. Ritika Bhumkar & Er. Laiba Mulani
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Synchronized Site Bar
st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-blue">📍 ACTIVE SYNC TARGET SITE</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">{gps_info.get('site_code', 'CV-SITE')}: {gps_info.get('label', 'Solapur Field Site')}</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>GPS:</b> <span class="accent-cyan">{gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E</span> | 
            <b>3D Member:</b> <span class="accent-orange">{st.session_state.selected_component}</span> | 
            <b>Verdict:</b> <span style="color:#EF4444; font-weight:bold;">{overall_verdict}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 5. PROJECT GENESIS & CREATION STORY (OPTIONAL BANNER)
# =========================================================
if show_genesis_story:
    st.markdown("""
    <div class="dark-card" style="border-left: 5px solid #38BDF8 !important;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <h2 class="accent-cyan" style="margin:0;">💡 Genesis & Creation Story of CONSTRUCTVISION AI</h2>
            <span class="badge-blue">CIVIL ENGINEERING INNOVATION STORY</span>
        </div>
        <p style="font-size:14px; color:#E2E8F0; margin-top:10px; line-height:1.7;">
            <b>Why was CONSTRUCTVISION AI created?</b><br>
            In traditional Indian civil engineering site practice across Maharashtra, structural audits of high-rise RCC columns, bridge piers, and housing developments relied heavily on <b>manual visual walkthroughs, handheld optical crack scales, chalk markings, and paper clipboards</b>.
        </p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:15px; margin-top:12px;">
            <div style="background:rgba(15,23,42,0.6); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.06);">
                <h4 class="accent-orange" style="margin:0 0 6px 0;">⚠️ The Real-World Civil Challenge</h4>
                <p style="font-size:13px; color:#94A3B8; margin:0;">
                    • Subjective human engineer bias when measuring sub-millimeter shear cracks.<br>
                    • Hazardous scaffolding climb work to inspect high-altitude beams & pier caps.<br>
                    • Slow report typing in Word/Excel taking 4 to 6 hours per component.<br>
                    • Missing temporal records to track crack growth over 12 to 24 months.
                </p>
            </div>
            <div style="background:rgba(15,23,42,0.6); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.06);">
                <h4 class="accent-green" style="margin:0 0 6px 0;">🚀 The AI Vision & Solution</h4>
                <p style="font-size:13px; color:#94A3B8; margin:0;">
                    • <b>Computer Vision Sub-Pixel Segmentation:</b> Instant metric measurement ($\text{mm}$) of micro-cracks (<0.1mm) via phone or drone camera.<br>
                    • <b>IS 456 & Eurocode Integration:</b> Codified safety verdict & repair costing.<br>
                    • <b>Live 3D Digital Twin & IoT:</b> Real-time spatial mapping with strain gauges.<br>
                    • <b>Automated Audit Export:</b> Instant GST tax invoicing & downloadable PDF/CSV logs.
                </p>
            </div>
        </div>
        <div style="margin-top:12px; font-size:13px; color:#CBD5E1; border-top:1px solid rgba(255,255,255,0.08); padding-top:8px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <span><b>Lead Developers & System Architects:</b> <span class="accent-cyan">Er. Ritika Bhumkar</span> & <span class="accent-orange">Er. Laiba Mulani</span></span>
            <span style="color:#94A3B8;">Department of Civil Engineering © 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# 6. FULLY GENERATED MULTI-PART MASTER INSPECTION REPORT
# =========================================================
st.markdown("## 📄 Fully Generated Consolidated Inspection Report")
st.caption("Consolidating live findings from GPS GIS, Computer Vision AI, Damage Analysis, 3D Digital Twin, IoT Telemetry, BOQ Billing, and Material Mix Engine.")

# ---------------- PART 1: SITE METADATA ----------------
st.markdown("### 📌 Part 1: Executive Site & Engineer Metadata")

col_p1, col_p2 = st.columns([1.2, 1])

with col_p1:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.markdown("<h3 class='accent-cyan' style='margin-top:0;'>🏗️ Project & Authority Identification</h3>", unsafe_allow_html=True)

    c_m1, c_m2 = st.columns(2)
    with c_m1:
        proj_title = st.selectbox(
            "Project Title Tag:",
            [f"{gps_info.get('site_code','CV-RES-01')}: {gps_info.get('label','Solapur Site')}", "Solapur Smart Infrastructure Expansion", "High-Rise Commercial Complex"],
            index=0
        )
        report_id = st.text_input("Audit Report Reference ID:", f"CV-{gps_info.get('site_code','SITE')}-{datetime.now().strftime('%m%d%H%M')}")
        audit_date = st.text_input("Audit Execution Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with c_m2:
        site_gps_text = st.text_input("GIS Coordinates / Route:", f"{gps_info.get('road','Rupa Bhavani Road')} ({gps_info.get('lat',17.6599):.4f}° N, {gps_info.get('lon',75.9064):.4f}° E)")
        lead_devs = st.selectbox(
            "Lead Structural Engineers:",
            ["Er. Ritika Bhumkar & Er. Laiba Mulani", "Er. Ritika Bhumkar (Lead Dev)", "Er. Laiba Mulani (Lead Dev)"],
            index=0
        )
        client_corp = st.text_input("Client / Contractor Organization:", "Solapur Smart Infrastructure Ltd")

    st.markdown("</div>", unsafe_allow_html=True)

with col_p2:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.markdown("<h3 class='accent-orange' style='margin-top:0;'>📸 Visual Proof Frame</h3>", unsafe_allow_html=True)
    st.image(proof_img, caption=f"Sub-Pixel AI Segmentation Proof Frame for {report_id}", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PART 2: COMPUTER VISION DIAGNOSTICS ----------------
st.divider()
st.markdown("### 🤖 Part 2: AI Computer Vision & Defect Diagnostics")

col_diag1, col_diag2 = st.columns(2)

with col_diag1:
    st.markdown(f"""
    <div class="report-card">
        <h3 class="accent-cyan" style="margin-top:0;">🔍 Computer Vision Metric Findings</h3>
        <table style="line-height:2.2; width:100%;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <td><strong>Target 3D Element Focus</strong></td>
                <td><span class="badge-blue">{st.session_state.selected_component}</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <td><strong>Primary Defect Typology</strong></td>
                <td>{defects_list[0]['Defect Category'] if defects_list else 'Flexural & Shear Crack'}</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <td><strong>Peak Measured Crack Opening</strong></td>
                <td><span class="accent-orange" style="font-weight:bold; font-size:16px;">{max_crack_mm:.2f} mm</span> (Code Limit: 0.30 mm)</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <td><strong>YOLOv8 Sub-Pixel Precision</strong></td>
                <td><span class="accent-green" style="font-weight:bold;">98.4% Confidence</span></td>
            </tr>
            <tr>
                <td><strong>Governing Code Verdict</strong></td>
                <td><span class="badge-critical">{overall_verdict.upper()}</span></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_diag2:
    st.markdown(f"""
    <div class="report-card">
        <h3 class="accent-green" style="margin-top:0;">📋 Defect Geometry & Remediation Summary</h3>
        <ul style="list-style:none; padding-left:0; line-height:2.1;">
            <li>🔹 <b>Total Anomalies Detected:</b> <span class="accent-cyan">{len(defects_list)} Items</span></li>
            <li>🔹 <b>Estimated Surface Crack Length:</b> {defects_list[0]['Length (mm)'] if defects_list else 185.5:.1f} mm</li>
            <li>🔹 <b>Affected Surface Area:</b> {defects_list[0]['Area (mm²)'] if defects_list else 128.4:.1f} $\text{{mm}}^2$</li>
            <li>🔹 <b>Root Cause Analysis:</b> Flexural shear stress concentration & concrete curing thermal shrinkage.</li>
            <li>🔹 <b>Mandated Action Protocol:</b> {defects_list[0]['Recommended Action'] if defects_list else 'Pressure epoxy grouting & tell-tale monitoring.'}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PART 3: 3D DIGITAL TWIN & IOT TELEMETRY ----------------
st.divider()
st.markdown("### 📡 Part 3: 3D Digital Twin & Wireless IoT Telemetry Status")

col_iot1, col_iot2, col_iot3, col_iot4 = st.columns(4)

with col_iot1:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Active 3D Member</span>
        <h4 class="accent-cyan" style="margin:4px 0 0 0;">{st.session_state.selected_component}</h4>
    </div>
    """, unsafe_allow_html=True)

with col_iot2:
    st.markdown("""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Live Microstrain ($\mu\varepsilon$)</span>
        <h3 class="accent-orange" style="margin:4px 0 0 0;">284.5 $\mu\varepsilon$</h3>
        <span style="font-size:11px; color:#94A3B8;">Limit: 250.0 $\mu\varepsilon$</span>
    </div>
    """, unsafe_allow_html=True)

with col_iot3:
    st.markdown("""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Plinth Base Tilt</span>
        <h3 class="accent-green" style="margin:4px 0 0 0;">0.04°</h3>
        <span style="font-size:11px; color:#94A3B8;">Limit: 0.25°</span>
    </div>
    """, unsafe_allow_html=True)

with col_iot4:
    st.markdown("""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Peak Acceleration</span>
        <h3 style="margin:4px 0 0 0; color:#FFFFFF;">0.018 g</h3>
        <span style="font-size:11px; color:#10B981;">Normal Ambient</span>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PART 4: MATERIAL MIX & CARBON AUDIT ----------------
st.divider()
st.markdown("### 🧱 Part 4: IS 10262 Concrete Mix Design & Carbon Footprint")

col_mat1, col_mat2 = st.columns(2)

with col_mat1:
    st.markdown("""
    <div class="report-card">
        <h3 class="accent-cyan" style="margin-top:0;">📦 Structural Mix Proportions (M25 Design Grade)</h3>
        <p>• <b>OPC 53 Cement Required:</b> <span class="accent-cyan">102 Bags</span> (5,100 kg)</p>
        <p>• <b>Fine River Sand (Zone II):</b> 11.55 $m^3$ (18,480 kg)</p>
        <p>• <b>Coarse Aggregate (20mm Gravel):</b> 23.10 $m^3$ (35,805 kg)</p>
        <p>• <b>Mixing Water Volume:</b> 2,295 Liters ($w/c = 0.45$)</p>
        <p>• <b>Superplasticizer Admixture:</b> 40.8 Liters</p>
    </div>
    """, unsafe_allow_html=True)

with col_mat2:
    st.markdown("""
    <div class="report-card">
        <h3 class="accent-green" style="margin-top:0;">🌱 Embodied Carbon & Sustainability Audit</h3>
        <p>• <b>Wet Concrete Target Volume:</b> 15.0 $m^3$</p>
        <p>• <b>Embodied Carbon Intensity:</b> 340 kg $CO_2e/m^3$</p>
        <p>• <b>Net Carbon Footprint:</b> <span class="accent-orange" style="font-weight:bold; font-size:18px;">4.72 Metric Tons $CO_2e$</span></p>
        <hr style="border-color:rgba(255,255,255,0.1);">
        <p style="font-size:13px; color:#CBD5E1;">
            💡 <b>Eco-Recommendation:</b> Substituting 20% cement with Pozzolanic Fly Ash reduces embodied carbon by 0.85 Tons $CO_2e$.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PART 5: BOQ BILLING & GST INVOICE ----------------
st.divider()
st.markdown("### 💰 Part 5: BOQ Cost Estimation & GST Tax Invoice Schedule")

col_boq1, col_boq2 = st.columns([1.5, 1])

boq_items = [
    {"Sr No": 1, "Item Description": f"Supply & Pressure Injection of Epoxy Grout ({max_crack_mm:.2f}mm Crack)", "Qty/Area": "45.0 sq.ft", "Rate (₹)": 950.0, "Amount (₹)": 42750.0},
    {"Sr No": 2, "Item Description": "Surface Chipping, High-Pressure Water Jetting & Substrate Prep", "Qty/Area": "45.0 sq.ft", "Rate (₹)": 81.25, "Amount (₹)": 3656.25},
    {"Sr No": 3, "Item Description": "Erection of Steel Tubular Scaffolding & Safety Netting", "Qty/Area": "45.0 sq.ft", "Rate (₹)": 65.0, "Amount (₹)": 2925.0},
    {"Sr No": 4, "Item Description": "Quality Assurance Core Extraction & Tell-Tale Monitoring", "Qty/Area": "1 Job", "Rate (₹)": 2137.50, "Amount (₹)": 2137.50}
]

subtotal_cost = sum(row["Amount (₹)"] for row in boq_items)
gst_tax = round(subtotal_cost * 0.18, 2)
contingency_reserve = round(subtotal_cost * 0.10, 2)
grand_total_cost = round(subtotal_cost + gst_tax + contingency_reserve, 2)

with col_boq1:
    st.markdown("#### **Itemized Schedule of Quantities (DSR 2026 Rates)**")
    st.dataframe(pd.DataFrame(boq_items), use_container_width=True, hide_index=True)

with col_boq2:
    st.markdown(f"""
    <div class="report-card">
        <h3 class="accent-cyan" style="margin-top:0;">🧾 Invoice Financial Summary</h3>
        <p><b>BOQ Subtotal:</b> <span style="float:right;">₹ {subtotal_cost:,.2f}</span></p>
        <p><b>Contingency Reserve (10%):</b> <span style="float:right;">₹ {contingency_reserve:,.2f}</span></p>
        <p><b>GST Tax (18%):</b> <span style="float:right;">₹ {gst_tax:,.2f}</span></p>
        <hr style="border-color:rgba(255,255,255,0.1);">
        <h2 class="accent-green" style="margin:0;">Grand Total: <span style="float:right;">₹ {grand_total_cost:,.2f}</span></h2>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PART 6: PREDICTIVE RISK & DEGRADATION ----------------
st.divider()
st.markdown("### 🔮 Part 6: 24-Month Predictive Degradation & Remediation Action Plan")

col_fc1, col_fc2 = st.columns([1.2, 1])

with col_fc1:
    # 24-Month Health Forecast Chart
    months = [f"Month {i:02d}" for i in range(1, 25)]
    time_steps = np.linspace(1, 24, 24)
    health_proj = np.maximum(15.0, 93.0 * np.exp(-0.035 * (time_steps ** 0.85)))
    risk_proj = np.minimum(100.0, (100.0 - health_proj) * 1.15)

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=months, y=health_proj, name="Structural Health Index (%)", mode="lines+markers", line=dict(color="#38BDF8", width=3)))
    fig_forecast.add_trace(go.Scatter(x=months, y=risk_proj, name="Failure Risk Score (%)", mode="lines+markers", line=dict(color="#EF4444", width=3, dash="dash"), yaxis="y2"))
    fig_forecast.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title=dict(text="Timeline Projection (Next 24 Months)")),
        yaxis=dict(title=dict(text="Structural Health Index (%)", font=dict(color="#38BDF8"))),
        yaxis2=dict(title=dict(text="Failure Risk Score (%)", font=dict(color="#EF4444")), overlaying="y", side="right")
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

with col_fc2:
    st.markdown("""
    <div class="report-card">
        <h3 class="accent-orange" style="margin-top:0;">📋 Action Milestones</h3>
        <div class="timeline-item">
            <strong>Immediate (Within 48 Hours):</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8;">Install structural shoring props under Column C-12 Level 1 joint.</span>
        </div>
        <div class="timeline-item">
            <strong>Short-Term (Within 14 Days):</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8;">Inject low-viscosity epoxy resin & mount optical tell-tale crack gauges.</span>
        </div>
        <div class="timeline-item" style="border-left:none;">
            <strong>Long-Term (6 Months):</strong><br>
            <span style="font-size:0.85rem; color:#94A3B8;">Perform Ultrasonic Pulse Velocity (UPV) scan to certify structural recovery.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 7. EXPORT & DOWNLOADABLE AUDIT PAYLOADS
# =========================================================
st.divider()
st.markdown("### 💾 Part 7: Export Multi-Module Audit Documentation")

col_dl1, col_dl2, col_dl3 = st.columns(3)

master_report_txt = f"""================================================================================
CONSTRUCTVISION AI — CONSOLIDATED CIVIL STRUCTURAL AUDIT REPORT
================================================================================
Project TitleTag : {proj_title}
Report Reference : {report_id}
Audit Timestamp  : {audit_date}
GIS Coordinates  : {site_gps_text}
Lead Engineers   : {lead_devs}
Client Name      : {client_corp}
Governing Code   : IS 456:2000 / Eurocode 2 / DSR 2026 Compliant
--------------------------------------------------------------------------------
1. COMPUTER VISION ANOMALY DIAGNOSTICS:
   • 3D Member Focus : {st.session_state.selected_component}
   • Defect Category : {defects_list[0]['Defect Category'] if defects_list else 'Flexural Shear Crack'}
   • Peak Crack Width: {max_crack_mm:.2f} mm (Code Safety Limit: 0.30 mm)
   • Model Precision : 98.4% Confidence
   • Verdict Status  : {overall_verdict.upper()}

2. IOT WIRELESS TELEMETRY READINGS:
   • Microstrain     : 284.5 µε (Limit: 250.0 µε)
   • Foundation Tilt : 0.04° (Limit: 0.25°)
   • Vibration Acceleration: 0.018 g

3. IS 10262 CONCRETE MIX & CARBON AUDIT:
   • Design Grade    : M25 Structural Concrete
   • OPC Cement      : 102 Bags (5,100 kg)
   • Carbon Intensity: 4.72 Metric Tons CO2e

4. FINANCIAL BOQ SUMMARY:
   • BOQ Subtotal    : ₹ {subtotal_cost:,.2f}
   • GST Tax (18%)   : ₹ {gst_tax:,.2f}
   • Contingency (10%): ₹ {contingency_reserve:,.2f}
   • GRAND TOTAL     : ₹ {grand_total_cost:,.2f}
--------------------------------------------------------------------------------
SYSTEM ARCHITECTS & LEAD DEVELOPERS:
  • Er. Ritika Bhumkar (Lead Civil & AI Engineer)
  • Er. Laiba Mulani (Structural AI Researcher)
================================================================================"""

with col_dl1:
    st.download_button(
        label="📄 Download Master Audit Summary (.TXT)",
        data=master_report_txt,
        file_name=f"Master_Audit_{report_id}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary"
    )

with col_dl2:
    st.download_button(
        label="💾 Export Itemized BOQ Schedule (.CSV)",
        data=pd.DataFrame(boq_items).to_csv(index=False),
        file_name=f"BOQ_Schedule_{report_id}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_dl3:
    st.download_button(
        label="🌐 Export JSON Audit Payload (.JSON)",
        data=json.dumps(inspection_payload, indent=2),
        file_name=f"Audit_Payload_{report_id}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

# =========================================================
# 8. CENTRAL INSPECTION AUDIT TRAIL ARCHIVE TABLE
# =========================================================
st.divider()
st.markdown("### 📋 Historical Inspection Audit Log Archive")

st.dataframe(
    df_logs,
    column_config={
        "Record_ID": st.column_config.TextColumn("Record ID", width="small"),
        "Date": st.column_config.DateColumn("Date", format="DD-MM-YYYY"),
        "Project": st.column_config.TextColumn("Site & Location Tag", width="medium"),
        "Inspection_Type": st.column_config.TextColumn("Assessment Category", width="medium"),
        "Inspector": st.column_config.TextColumn("Lead Engineers", width="medium"),
        "AI_Confidence": st.column_config.ProgressColumn("Precision", format="%.0f%%", min_value=0, max_value=1),
        "Status": st.column_config.SelectboxColumn("Status", options=["Safe", "Review Required", "Critical Alert"])
    },
    use_container_width=True,
    hide_index=True
)

# =========================================================
# FOOTER
# =========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:16px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI CENTRAL REPORT HUB</b> | Multi-Module Quality Assurance System<br>
    Developed by <b>Er. Ritika Bhumkar</b> & <b>Er. Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
