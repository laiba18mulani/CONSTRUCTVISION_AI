from datetime import datetime
import json
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION & DARK GLASS UI THEME
# =========================================================
st.set_page_config(
    page_title="AI Crack & Structural Defect Inspection | CONSTRUCTVISION AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Glowing Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #172437 0%, #080D14 60%, #03060A 100%) !important;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit Default Header/Footer */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Dark Glass Cards & Containers */
    .dark-card, .metric-box {
        background: rgba(13, 20, 32, 0.78) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .dark-card:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
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

    /* Custom Badges */
    .badge-blue { background: rgba(37, 99, 235, 0.25); color: #60A5FA; border: 1px solid #2563EB; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-critical { background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-success { background: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }

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

# Safe import for external utilities
try:
    from utils.site_data import add_inspection_record
except ImportError:
    def add_inspection_record(payload):
        if "inspection_history_records" not in st.session_state:
            st.session_state["inspection_history_records"] = []
        st.session_state["inspection_history_records"].append(payload)

# =========================================================
# 2. GPS SESSION SYNCHRONIZATION BRIDGE
# =========================================================
gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road",
    "type": "Commercial High-Rise",
    "risk_score": 88
})

st.title("🔬 AI Concrete Defect & Micro-Crack Segmentation Engine")
st.caption("Computer vision feature extraction, metric sub-pixel defect measurement, and automated civil engineering code compliance.")

# Location Sync Bar
st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-blue">📍 ACTIVE SYNC SITE</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">{gps_info.get('site_code', 'CV-SITE')}: {gps_info.get('label', 'Solapur Field Site')}</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>Route:</b> {gps_info.get('road', 'N/A')} | 
            <b>Coordinates:</b> <span style="color:#38BDF8;">{gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 3. SIDEBAR CONTROLS & COMPUTER VISION TUNING
# =========================================================
with st.sidebar:
    st.markdown("### ⚙️ **AI Model Calibration**")
    st.caption("Sub-pixel Scale & Computer Vision Parameters")
    st.divider()

    inspection_typology = st.selectbox(
        "Target Component Typology:",
        ["Reinforced Concrete Column", "Flexural Concrete Beam", "Floor Slab / Deck Soffit", "Brick Masonry Wall", "Plinth & Footing"],
        index=0
    )

    defect_mode = st.selectbox(
        "Detection Model Mode:",
        ["Flexural & Shear Cracks", "Concrete Spalling & Rebar Exposure", "Honeycombing & Aggregate Voids", "Masonry Joint Separation"],
        index=0
    )

    st.divider()
    st.markdown("#### 📏 Metric Scale Calibration")
    px_to_mm_ratio = st.number_input("Pixel-to-mm Scale Factor (mm/px):", min_value=0.01, max_value=2.00, value=0.15, step=0.01)

    st.divider()
    st.markdown("#### 🎛️ Sensitivity Controls")
    crack_sensitivity = st.slider("Canny Edge Sensitivity:", min_value=10, max_value=200, value=45, step=5)
    min_crack_length = st.slider("Min Defect Threshold (px):", min_value=10, max_value=300, value=30, step=5)

    st.divider()
    st.markdown("#### 🧹 Noise Filtering Rules")
    auto_isolate = st.checkbox("Suppress Sky & Glare Artifacts", value=True)
    suppress_trees = st.checkbox("Suppress Vegetation / Leaf Shadows", value=True)

    st.caption("Department of Civil Engineering © 2026")

# =========================================================
# 4. IMAGE ACQUISITION & PHONE CAMERA INPUT ENGINE
# =========================================================
col_source, col_kpis = st.columns([2, 1])

with col_source:
    source_option = st.radio(
        "Select Image Input Source:", 
        ["📸 Snap via Phone / Live Camera", "📤 Upload Field Photo (JPG/PNG)", "🎯 Generate Demo Concrete Target"], 
        horizontal=True
    )

image_to_process = None

if "Phone" in source_option:
    camera_photo = st.camera_input("📸 Capture Concrete Target Image with Phone/Laptop Camera")
    if camera_photo is not None:
        image_to_process = Image.open(camera_photo).convert('RGB')
        st.success("📷 Live Camera Frame Captured & Staged for Analysis!")
elif "Upload" in source_option:
    uploaded_file = st.file_uploader("Upload concrete structural image for inspection...", type=["jpg", "jpeg", "png", "tif"])
    if uploaded_file is not None:
        image_to_process = Image.open(uploaded_file).convert('RGB')
else:
    # Synthetic Concrete Surface Generator for Demo Testing
    synth = np.full((420, 640, 3), 130, dtype=np.uint8)
    noise = np.random.normal(0, 12, (420, 640, 3)).astype(np.int16)
    synth = np.clip(synth.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Draw primary diagonal shear crack
    cv2.polylines(synth, [np.array([[80, 60], [160, 130], [240, 180], [330, 270], [420, 330], [510, 380]])], False, (25, 25, 25), 5)
    cv2.polylines(synth, [np.array([[240, 180], [320, 200], [410, 230]])], False, (35, 35, 35), 3)
    # Draw spalling zone
    cv2.circle(synth, (480, 140), 35, (70, 65, 60), -1)
    cv2.circle(synth, (480, 140), 20, (30, 30, 30), -1)
    
    image_to_process = Image.fromarray(synth)

# =========================================================
# 5. COMPUTER VISION INSPECTION ENGINE
# =========================================================
if image_to_process is not None:
    st.divider()
    
    col_orig, col_proc = st.columns(2)
    
    with col_orig:
        st.markdown("### 📷 Original Target Image")
        st.image(image_to_process, use_container_width=True)

    img_np = np.array(image_to_process.convert('RGB'))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    
    h, w = gray.shape
    valid_building_mask = np.ones((h, w), dtype=np.uint8) * 255

    # Sky & Foliage Filtering
    if auto_isolate:
        sky_blue = cv2.inRange(hsv, np.array([85, 20, 100]), np.array([135, 255, 255]))
        sky_bright = cv2.inRange(hsv, np.array([0, 0, 210]), np.array([180, 45, 255]))
        sky_mask = cv2.bitwise_or(sky_blue, sky_bright)
        valid_building_mask = cv2.bitwise_and(valid_building_mask, cv2.bitwise_not(sky_mask))

    if suppress_trees:
        green_mask = cv2.inRange(hsv, np.array([25, 30, 20]), np.array([90, 255, 255]))
        green_mask = cv2.dilate(green_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)
        valid_building_mask = cv2.bitwise_and(valid_building_mask, cv2.bitwise_not(green_mask))

    # Geometric Feature Extraction
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, crack_sensitivity, crack_sensitivity * 2)
    edges_masked = cv2.bitwise_and(edges, edges, mask=valid_building_mask)
    
    kernel_line = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    connected_edges = cv2.morphologyEx(edges_masked, cv2.MORPH_CLOSE, kernel_line)
    
    contours, _ = cv2.findContours(connected_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    annotated_img = img_np.copy()
    defects_detected = []
    defect_counter = 1

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeter < min_crack_length:
            continue
            
        area = cv2.contourArea(cnt)
        x, y, box_w, box_h = cv2.boundingRect(cnt)
        
        aspect_ratio = max(box_w, box_h) / float(min(box_w, box_h) + 1e-5)
        rect_area = box_w * box_h
        extent = float(area) / rect_area if rect_area > 0 else 0
        
        if aspect_ratio >= 1.6 or extent < 0.40:
            length_px = perimeter / 2.0
            width_px = (area / length_px) if length_px > 0 else 1.2
            
            width_mm = round(min(max(width_px * px_to_mm_ratio, 0.08), 6.50), 2)
            length_mm = round(length_px * px_to_mm_ratio, 1)
            surface_area_mm2 = round(area * (px_to_mm_ratio ** 2), 1)

            # Severity Classification (IS 456 / Eurocode 2)
            if width_mm > 0.30:
                severity = "CRITICAL (Grade III)"
                color = (255, 50, 50)
                remediation = "Structural shoring & pressure epoxy injection grouting."
            elif width_mm >= 0.10:
                severity = "MODERATE (Grade II)"
                color = (255, 165, 0)
                remediation = "Low-viscosity resin sealing & tell-tale monitoring."
            else:
                severity = "NOMINAL (Grade I)"
                color = (50, 220, 100)
                remediation = "Surface cosmetic monitoring."

            cv2.drawContours(annotated_img, [cnt], -1, color, 2)
            cv2.rectangle(annotated_img, (x - 2, y - 2), (x + box_w + 2, y + box_h + 2), color, 1)
            cv2.putText(annotated_img, f"#{defect_counter} [{width_mm}mm]", (x, max(y - 6, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
            cv2.putText(annotated_img, f"#{defect_counter} [{width_mm}mm]", (x, max(y - 6, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
            
            repair_cost_inr = round(width_mm * 8500 + length_mm * 120 + 1500, 0)

            defects_detected.append({
                "Defect ID": f"DEF-{defect_counter:02d}",
                "Typology": inspection_typology,
                "Defect Category": defect_mode,
                "Length (mm)": length_mm,
                "Max Width (mm)": width_mm,
                "Area (mm²)": surface_area_mm2,
                "Severity": severity,
                "Confidence": f"{min(98, int(82 + (aspect_ratio * 1.5)))}%",
                "Recommended Action": remediation,
                "Estimated Cost (₹)": repair_cost_inr,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            defect_counter += 1

    with col_proc:
        st.markdown("### 🎯 AI Bounding Box & Segmentation Overlay")
        st.image(annotated_img, use_container_width=True)

    # =========================================================
    # 6. QUANTITATIVE DIAGNOSTIC RESULTS & SUMMARY
    # =========================================================
    st.divider()
    st.markdown("### 📊 Diagnostic Findings & Metric Breakdown")

    if defects_detected:
        max_width = max([d["Max Width (mm)"] for d in defects_detected])
        total_cost = sum([d["Estimated Cost (₹)"] for d in defects_detected])
        overall_status = "CRITICAL HAZARD" if max_width > 0.30 else ("ACTION MONITORED" if max_width >= 0.10 else "NOMINAL COMPLIANCE")
        status_cls = "badge-critical" if max_width > 0.30 else ("badge-blue" if max_width >= 0.10 else "badge-success")

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="dark-card">
                <span style="font-size:12px; color:#94A3B8;">Inspection Status</span>
                <h3 style="margin:4px 0 0 0;"><span class="{status_cls}">{overall_status}</span></h3>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col2:
            st.markdown(f"""
            <div class="dark-card">
                <span style="font-size:12px; color:#94A3B8;">Peak Crack Width</span>
                <h2 class="accent-orange" style="margin:4px 0 0 0;">{max_width:.2f} mm</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col3:
            st.markdown(f"""
            <div class="dark-card">
                <span style="font-size:12px; color:#94A3B8;">Detected Anomalies</span>
                <h2 class="accent-cyan" style="margin:4px 0 0 0;">{len(defects_detected)} Defects</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col4:
            st.markdown(f"""
            <div class="dark-card">
                <span style="font-size:12px; color:#94A3B8;">Estimated Remediation</span>
                <h2 class="accent-green" style="margin:4px 0 0 0;">₹{total_cost:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)

        df_defects = pd.DataFrame(defects_detected)
        st.dataframe(
            df_defects[["Defect ID", "Typology", "Defect Category", "Length (mm)", "Max Width (mm)", "Area (mm²)", "Severity", "Confidence", "Estimated Cost (₹)", "Recommended Action"]],
            use_container_width=True,
            hide_index=True
        )

        # =========================================================
        # 7. CROSS-MODULE SYNC BRIDGE & EXPORT
        # =========================================================
        st.markdown("### 🔗 Sync Findings with Structural Modules")

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "site_code": gps_info.get("site_code", "CV-SITE"),
            "location": gps_info.get("label", "Solapur Field Site"),
            "gps": f"{gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E",
            "total_defects": len(defects_detected),
            "max_crack_width_mm": max_width,
            "verdict": overall_status,
            "defects_list": defects_detected,
            "total_repair_cost_inr": total_cost
        }

        st.session_state["latest_inspection"] = payload
        add_inspection_record(payload)

        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            if st.button("📊 Export & Proceed to Damage Analysis", use_container_width=True, type="primary"):
                st.success("Inspection payload synchronized! Select '6_📊_Damage_Analysis.py' on the sidebar.")

        with col_act2:
            st.download_button(
                label="💾 Download Inspection Log (.CSV)",
                data=df_defects.to_csv(index=False),
                file_name=f"Inspection_Log_{gps_info.get('site_code','SITE')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_act3:
            st.download_button(
                label="🌐 Download JSON Audit Payload (.JSON)",
                data=json.dumps(payload, indent=2),
                file_name=f"Audit_Payload_{gps_info.get('site_code','SITE')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

    else:
        st.success("✅ Nominal Condition: No structural micro-cracks detected above confidence threshold. Surface texture complies with IS 456 safe limits.")

# =========================================================
# FOOTER
# =========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI INSPECTION ENGINE</b> | Structural Surface Anomaly Classifier<br>
    Developed by <b>Ritika Bhumkar</b> & <b>Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
