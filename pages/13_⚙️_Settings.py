from datetime import datetime
import json
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Global Settings & AI Calibration Console | CONSTRUCTVISION AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initializing global session state defaults
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Glowing Dark Glass"
if "accent_color" not in st.session_state:
    st.session_state.accent_color = "#38BDF8"
if "currency_symbol" not in st.session_state:
    st.session_state.currency_symbol = "₹"
if "global_scale_ratio" not in st.session_state:
    st.session_state.global_scale_ratio = 0.15
if "governing_code" not in st.session_state:
    st.session_state.governing_code = "IS 456:2000 (Indian Standard)"
if "strain_threshold_limit" not in st.session_state:
    st.session_state.strain_threshold_limit = 250.0
if "gst_tax_rate" not in st.session_state:
    st.session_state.gst_tax_rate = 18.0

theme_mode = st.session_state.app_theme

if theme_mode == "Clean Light Engineering":
    bg_style = "background: #F8FAFC !important; color: #0F172A !important;"
    card_bg = "background: #FFFFFF !important; border: 1px solid #CBD5E1 !important; color: #0F172A !important;"
    text_color = "#0F172A"
elif theme_mode == "High-Contrast Blueprint":
    bg_style = "background: #02182B !important; color: #E0F2FE !important;"
    card_bg = "background: #032845 !important; border: 1px solid #0284C7 !important; color: #E0F2FE !important;"
    text_color = "#E0F2FE"
else:  # Glowing Dark Glass (Default)
    bg_style = "background: radial-gradient(circle at 50% -20%, #172437 0%, #080D14 60%, #03060A 100%) !important; color: #E2E8F0 !important;"
    card_bg = "background: rgba(13, 20, 32, 0.82) !important; backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.09) !important; color: #E2E8F0 !important;"
    text_color = "#FFFFFF"

st.markdown(f"""
<style>
    .stApp {{
        {bg_style}
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    .dark-card, .settings-card {{
        {card_bg}
        border-radius: 16px !important;
        padding: 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }}
    .dark-card:hover, .settings-card:hover {{
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }}

    h1, h2, h3, h4 {{
        color: {text_color} !important;
        font-weight: 700 !important;
    }}
    .accent-cyan {{ color: #38BDF8 !important; text-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }}
    .accent-orange {{ color: #F97316 !important; text-shadow: 0 0 12px rgba(249, 115, 22, 0.4); }}
    .accent-green {{ color: #10B981 !important; text-shadow: 0 0 12px rgba(16, 185, 129, 0.4); }}
    .accent-red {{ color: #EF4444 !important; text-shadow: 0 0 12px rgba(239, 68, 68, 0.4); }}

    .stButton>button {{
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.4) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.5) !important;
        transform: translateY(-1px);
    }}

    .badge-blue {{ background: rgba(37, 99, 235, 0.25); color: #60A5FA; border: 1px solid #2563EB; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }}
    .badge-success {{ background: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }}
</style>
""", unsafe_allow_html=True)

gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road"
})

with st.sidebar:
    st.markdown("### ⚙️ **Settings Console**")
    st.caption("Global Architecture Preferences & Calibration")
    st.divider()

    st.markdown("#### 🔗 Linked Active Target")
    st.caption(f"• **Active Site:** `{gps_info.get('site_code','CV-SITE')}` ({gps_info.get('label','Solapur')})")
    st.caption(f"• **UI Theme:** `{st.session_state.app_theme}`")
    st.caption(f"• **Governing Code:** `{st.session_state.governing_code[:16]}...`")
    st.caption(f"• **Scale Ratio:** `{st.session_state.global_scale_ratio:.2f} mm/px`")
    st.caption(f"• **Currency:** `{st.session_state.currency_symbol}`")

    st.divider()
    st.caption("Department of Civil Engineering © 2026")

st.title("⚙️ Global System Settings & AI Calibration Console")
st.caption("Central control hub for application theme customization, computer vision parameters, civil code standards, IoT telemetry limits, and financial rates.")

st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-blue">📍 GLOBAL SYSTEM SYNC</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">{gps_info.get('site_code','CV-SITE')}: {gps_info.get('label','Solapur Field Site')}</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>Active Theme:</b> <span class="accent-cyan">{st.session_state.app_theme}</span> | 
            <b>Scale:</b> <span class="accent-orange">{st.session_state.global_scale_ratio:.2f} mm/px</span> | 
            <b>System Status:</b> <span style="color:#10B981; font-weight:bold;">100% OPERATIONAL</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_theme, tab_vision, tab_codes, tab_iot, tab_finance, tab_profile, tab_backup = st.tabs([
    "🎨 Appearance & Theme",
    "🔬 AI Vision Calibration",
    "📐 Civil Code Standards",
    "📡 IoT Gateway & Alarms",
    "💰 Financials & BOQ Rates",
    "👷 Lead Profile & Signature",
    "💾 Backup & Reset"
])

with tab_theme:
    st.markdown("### 🎨 Application UI Theme & Aesthetic Controls")
    st.caption("Customize the global appearance, color palette, font sizing, and visual density across all pages.")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **UI Theme Palette**")

        theme_options = ["Glowing Dark Glass", "Clean Light Engineering", "High-Contrast Blueprint"]
        current_theme_idx = theme_options.index(st.session_state.app_theme) if st.session_state.app_theme in theme_options else 0
        selected_theme = st.selectbox(
            "Select Global Theme Preset:",
            theme_options,
            index=current_theme_idx
        )

        accent_color_choice = st.color_picker(
            "Primary Accent Color:",
            value=st.session_state.get("accent_color", "#38BDF8")
        )

        sidebar_behavior = st.selectbox(
            "Sidebar State on Launch:",
            ["Expanded (Default)", "Collapsed Mode"],
            index=0
        )

        if st.button("💾 Apply Theme Settings", type="primary"):
            st.session_state.app_theme = selected_theme
            st.session_state.accent_color = accent_color_choice
            st.success("✅ Theme settings applied globally across all modules!")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Theme Live Preview**")
        st.markdown(f"• **Current Palette:** `{selected_theme}`")
        st.markdown(f"• **Accent Highlight:** <span style='color:{accent_color_choice}; font-weight:bold;'>{accent_color_choice}</span>", unsafe_allow_html=True)
        st.markdown("• **Card Backdrop:** Glassmorphism Blur (`16px`)")
        st.markdown("• **Font Family:** `Inter, -apple-system, sans-serif`")
        st.divider()
        st.markdown("<p style='font-size:12px; color:#94A3B8;'>Note: Switching themes updates CSS properties instantly on page reload.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_vision:
    st.markdown("### 🔬 Computer Vision & Sub-Pixel Scale Calibration")
    st.caption("Calibrate pixel-to-millimeter transformation ratios, edge detection sensitivity, and background noise filters.")

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Sub-Pixel Scale Calibration**")

        scale_ratio = st.number_input(
            "Default Pixel-to-mm Transformation Scale Factor (mm/px):",
            min_value=0.01, max_value=2.00,
            value=float(st.session_state.global_scale_ratio),
            step=0.01,
            help="Defines how many millimeters correspond to 1 pixel in high-resolution field imagery."
        )

        canny_threshold = st.slider(
            "Canny Edge Sensitivity Threshold:",
            min_value=10, max_value=200, value=45, step=5
        )

        confidence_cutoff = st.slider(
            "YOLOv8 Confidence Cutoff Score (%):",
            min_value=50, max_value=99, value=85, step=1
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col_v2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Noise Filtering & Suppression Rules**")

        isolate_sky = st.checkbox("Automatically Suppress Sky Blue & Bright Glare Artifacts", value=True)
        suppress_vegetation = st.checkbox("Automatically Suppress Green Vegetation & Leaf Shadows", value=True)
        min_defect_px = st.number_input("Minimum Defect Bounding Area (pixels):", min_value=5, max_value=500, value=30, step=5)

        if st.button("💾 Save Vision Calibration Rules", type="primary"):
            st.session_state.global_scale_ratio = scale_ratio
            st.success("✅ Vision model calibration saved! Scale ratio updated globally.")

        st.markdown("</div>", unsafe_allow_html=True)

with tab_codes:
    st.markdown("### 📐 Civil Engineering Code Standards & Safety Limits")
    st.caption("Map structural defect severity thresholds and safety compliance checks against international civil codes.")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Governing Design Standard**")

        code_options = [
            "IS 456:2000 (Indian Standard Plain & Reinforced Concrete)",
            "Eurocode 2 (EN 1992 Design of Concrete Structures)",
            "ACI 318-19 (American Concrete Institute Building Code)",
            "BS 8110 (British Standard Structural Use of Concrete)"
        ]
        curr_code_idx = code_options.index(st.session_state.governing_code) if st.session_state.governing_code in code_options else 0
        code_choice = st.selectbox(
            "Active Civil Engineering Code Standard:",
            code_options,
            index=curr_code_idx
        )

        max_hairline = st.number_input("Permissible Hairline Crack Opening Limit (mm):", min_value=0.05, max_value=0.50, value=0.10, step=0.01)
        max_shear_limit = st.number_input("Critical Shear Crack Action Limit (mm):", min_value=0.10, max_value=1.00, value=0.30, step=0.01)

        if st.button("💾 Update Governing Code Limits", type="primary"):
            st.session_state.governing_code = code_choice
            st.success(f"✅ Code compliance engine set to '{code_choice}'!")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Non-Destructive Testing (NDT) UPV Rating Scale**")
        st.markdown("• **> 4.5 km/s:** Excellent Structural Concrete")
        st.markdown("• **3.5 - 4.5 km/s:** Good Concrete Quality")
        st.markdown("• **3.0 - 3.5 km/s:** Medium Quality (Micro-voids present)")
        st.markdown("• **< 3.0 km/s:** Poor Concrete (Honeycombing / Severe Delamination)")
        st.divider()
        st.markdown("• **IS 456 Clause 35.3.2:** Surface crack widths shall not exceed 0.30 mm in direct tension/shear members.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab_iot:
    st.markdown("### 📡 Wireless IoT Gateway & Emergency Alarm Thresholds")
    st.caption("Configure MQTT broker connection parameters, wireless sensor polling frequencies, and acoustic emergency alarms.")

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **MQTT Broker Endpoint**")

        st.text_input("MQTT Broker URL:", "mqtts://gateway.constructvision.ai")
        st.number_input("Port Number:", min_value=1000, max_value=65535, value=8883)
        st.selectbox("Security Transport Protocol:", ["TLS v1.3 with X.509 Client Certs", "TLS v1.2 Standard", "WebSockets Secure (WSS)"])
        polling_rate = st.slider("Telemetry Stream Update Interval (seconds):", min_value=1, max_value=10, value=2, step=1)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_i2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Safety Threshold Limits & Siren Alarms**")

        microstrain_limit = st.number_input(
            r"Microstrain Safety Limit ($\mu\varepsilon$):",
            min_value=50.0, max_value=1000.0,
            value=float(st.session_state.strain_threshold_limit),
            step=10.0
        )

        tilt_limit_deg = st.number_input("Maximum Base Tilt Angle (°):", min_value=0.01, max_value=2.00, value=0.25, step=0.01)
        enable_audio_alarm = st.checkbox("Play Synthesized Warning Siren Tone on Threshold Breach", value=True)

        if st.button("💾 Save IoT Gateway Settings", type="primary"):
            st.session_state.strain_threshold_limit = microstrain_limit
            st.success("✅ Wireless IoT thresholds and gateway parameters saved!")

        st.markdown("</div>", unsafe_allow_html=True)

with tab_finance:
    st.markdown("### 💰 BOQ Estimation Rates, Taxes & Currency Settings")
    st.caption("Manage currency symbols, GST tax percentages, inflation buffers, and DSR schedule rate cards.")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Currency & Tax Configuration**")

        curr_choice = st.selectbox(
            "Primary Currency Symbol:",
            ["₹ (Indian Rupee - INR)", "$ (US Dollar - USD)", "€ (Euro - EUR)", "£ (British Pound - GBP)"],
            index=0
        )

        gst_rate = st.number_input(
            "Applicable GST Tax Rate (%):",
            min_value=0.0, max_value=30.0,
            value=float(st.session_state.gst_tax_rate),
            step=1.0
        )

        inflation_buf = st.slider("Material Inflation Buffer (%):", min_value=0, max_value=25, value=8, step=1)
        contingency_buf = st.slider("Unforeseen Risk Contingency Buffer (%):", min_value=0, max_value=30, value=10, step=1)

        if st.button("💾 Apply Financial Settings", type="primary"):
            st.session_state.currency_symbol = curr_choice[0]
            st.session_state.gst_tax_rate = gst_rate
            st.success("✅ Currency and GST tax settings updated globally!")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_f2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Default DSR 2026 Rate Schedule Overrides**")
        st.markdown("• **Low Viscosity Epoxy Grout:** ₹ 950.00 / sq.ft")
        st.markdown("• **Polymer Modified Mortar:** ₹ 1,650.00 / sq.ft")
        st.markdown("• **High-Pressure Water Jetting:** ₹ 81.25 / sq.ft")
        st.markdown("• **Steel Tubular Scaffolding:** ₹ 65.00 / sq.ft")
        st.markdown("• **Skilled Repair Labor:** ₹ 185.00 / sq.ft")
        st.markdown("</div>", unsafe_allow_html=True)

with tab_profile:
    st.markdown("### 👷 Lead Structural Architects & System Developers")
    st.caption("System architect profiles and digital signatures affixed to master audit reports.")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("""
        <div class="dark-card">
            <span class="badge-blue">SYSTEM ARCHITECT & LEAD DEVELOPER</span>
            <h3 class="accent-cyan" style="margin:6px 0 2px 0;">Er. Ritika Bhumkar</h3>
            <p style="margin:0; font-size:13px; color:#94A3B8;">Lead Civil & Structural AI Engineer</p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <p style="font-size:13px; color:#CBD5E1;">
                • Department of Civil Engineering<br>
                • Focus: Computer Vision Defect Segmentation & FEA Stress Modeling<br>
                • Authorized Audit Signatory ID: <code>CV-DEV-01-RB</code>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="dark-card">
            <span class="badge-blue">SYSTEM ARCHITECT & LEAD DEVELOPER</span>
            <h3 class="accent-orange" style="margin:6px 0 2px 0;">Er. Laiba Mulani</h3>
            <p style="margin:0; font-size:13px; color:#94A3B8;">Structural AI Researcher & Systems Architect</p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <p style="font-size:13px; color:#CBD5E1;">
                • Department of Civil Engineering<br>
                • Focus: Wireless IoT Telemetry & 3D Digital Twin Integration<br>
                • Authorized Audit Signatory ID: <code>CV-DEV-02-LM</code>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.text_input("Organization / Client Corporation Name:", "Solapur Smart Infrastructure Ltd & Solapur HQ")
    st.text_input("Digital Audit Certificate Reference:", "ISO 9001:2015 & IS 456 Certified Platform")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_backup:
    st.markdown("### 💾 Configuration Export, Import & Factory Reset")
    st.caption("Export system settings to JSON payloads or restore settings to factory defaults.")

    col_b1, col_b2 = st.columns(2)

    export_payload = {
        "timestamp": datetime.now().isoformat(),
        "app_theme": st.session_state.app_theme,
        "accent_color": st.session_state.accent_color,
        "currency_symbol": st.session_state.currency_symbol,
        "global_scale_ratio": st.session_state.global_scale_ratio,
        "governing_code": st.session_state.governing_code,
        "strain_threshold_limit": st.session_state.strain_threshold_limit,
        "gst_tax_rate": st.session_state.gst_tax_rate,
        "lead_engineers": ["Er. Ritika Bhumkar", "Er. Laiba Mulani"]
    }

    with col_b1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Export Settings Payload**")
        st.json(export_payload)

        st.download_button(
            label="📥 Download Settings Backup (.JSON)",
            data=json.dumps(export_payload, indent=4),
            file_name=f"ConstructVision_Settings_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True,
            type="primary"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Factory Reset System Session**")
        st.warning("⚠️ Warning: Resetting clears all active temporary session states and restores baseline defaults.")

        if st.button("🔄 Perform Factory Reset of Session State", use_container_width=True):
            st.session_state.clear()
            st.success("✅ Factory reset completed! Reloading system defaults...")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:16px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI GLOBAL SETTINGS & CALIBRATION CONSOLE</b><br>
    Developed by <b>Er. Ritika Bhumkar</b> & <b>Er. Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
