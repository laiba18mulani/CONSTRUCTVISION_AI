from datetime import datetime
import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================================
# 1. PAGE CONFIGURATION & DARK GLASS THEME
# ==========================================================
st.set_page_config(
    page_title="Civil Engineering Virtual Practical Lab | CONSTRUCTVISION AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Glowing Dark Gradient Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #172437 0%, #080D14 60%, #03060A 100%) !important;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    section[data-testid="stSidebar"] {
        background-color: #0B0F17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .dark-card, .lab-card, .hero-dark {
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
    .dark-card:hover, .lab-card:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }

    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .accent-cyan { color: #38BDF8 !important; text-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }
    .accent-orange { color: #F97316 !important; text-shadow: 0 0 12px rgba(249, 115, 22, 0.4); }
    .accent-green { color: #10B981 !important; text-shadow: 0 0 12px rgba(16, 185, 129, 0.4); }
    .accent-red { color: #EF4444 !important; text-shadow: 0 0 12px rgba(239, 68, 68, 0.4); }

    .badge-blue { background: rgba(37, 99, 235, 0.25); color: #60A5FA; border: 1px solid #2563EB; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-success { background: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-warning { background: rgba(249, 115, 22, 0.25); color: #FDBA74; border: 1px solid #F97316; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-critical { background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-block; }

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

gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road"
})

if "lab_completed_experiments" not in st.session_state:
    st.session_state.lab_completed_experiments = {}

with st.sidebar:
    st.markdown("### 🎮 **Virtual Civil Lab**")
    st.caption("Interactive Engineering Practical Simulators")
    st.divider()

    active_lab = st.radio(
        "Select Practical Simulator:",
        [
            "🧪 Lab 1: Concrete Slump Cone Test (IS 7320)",
            "🔬 Lab 2: UTM Rebar Tensile Test (IS 1608)",
            "📡 Lab 3: Ultrasonic Pulse Velocity (IS 516)",
            "🔨 Lab 4: Schmidt Rebound Hammer Test",
            "⏳ Lab 5: Fine Aggregate Sieve Analysis",
            "🎓 Lab 6: Practical Exam & Certification"
        ],
        index=0
    )

    st.divider()
    st.markdown("#### 🔗 Linked Active Target")
    st.caption(f"• **Active Site:** `{gps_info.get('site_code','CV-SITE')}` ({gps_info.get('label','Solapur')})")
    st.caption(f"• **Completed Practicals:** `{len(st.session_state.lab_completed_experiments)} / 5`")
    st.divider()
    st.caption("Department of Civil Engineering © 2026")

st.title("🎮 Civil Engineering Virtual Practical & Interactive Lab Suite")
st.caption("Virtual laboratory experiments simulating standard Indian Standard (IS), ASTM, and Eurocode civil engineering testing procedures.")

st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-blue">📍 VIRTUAL LAB WORKSPACE</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">IS Code Compliant Experimental Simulator</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>Lead Developers:</b> <span class="accent-cyan">Er. Ritika Bhumkar</span> & <span class="accent-orange">Er. Laiba Mulani</span> | 
            <b>Status:</b> <span style="color:#10B981; font-weight:bold;">LAB READY</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if "Lab 1" in active_lab:
    st.markdown("## 🧪 Lab 1: Concrete Slump Cone Workability Test (IS 7320 / ASTM C143)")
    st.caption("Determine the consistency and workability of fresh concrete mix through cone mold subsidence analysis.")

    col_l1_in, col_l1_res = st.columns([1, 1.2])

    with col_l1_in:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Fresh Concrete Batch Parameters**")
        
        concrete_grade = st.selectbox("Design Concrete Grade:", ["M15 (Lean Mix)", "M20 (PCC/RCC)", "M25 (RCC Structural)", "M35 (High Strength)", "M40 (Prestressed)"], index=2)
        wc_ratio = st.slider(r"Water-Cement Ratio ($w/c$):", min_value=0.30, max_value=0.75, value=0.48, step=0.01)
        sand_ratio = st.slider("Fine-to-Total Aggregate Ratio (%):", min_value=30, max_value=55, value=40, step=1)
        admixture_dosage = st.slider("Superplasticizer Admixture Dosage (% by wt. cement):", min_value=0.0, max_value=2.0, value=0.6, step=0.1)
        tamping_strokes = st.number_input("Tamping Rod Strokes per Layer (25 Mandated by IS 7320):", min_value=5, max_value=50, value=25, step=1)
        
        st.markdown("</div>", unsafe_allow_html=True)

    base_slump = 20.0 + (wc_ratio - 0.35) * 350.0 + (admixture_dosage * 35.0) - ((40 - sand_ratio) * 1.5)
    if tamping_strokes < 25:
        base_slump += (25 - tamping_strokes) * 1.2
    slump_mm = max(5.0, min(240.0, round(base_slump, 1)))

    if slump_mm < 50:
        slump_type = "Very Low (Dry Mix / True Slump)"
        workability_desc = "Suitable for road paving & heavy mass concrete compaction by power vibrators."
        badge_cls = "badge-blue"
    elif slump_mm <= 100:
        slump_type = "Medium (True Slump)"
        workability_desc = "Ideal for standard RCC beams, columns, slabs, and manually compacted structural concrete."
        badge_cls = "badge-success"
    elif slump_mm <= 175:
        slump_type = "High (True / Flowing Slump)"
        workability_desc = "Suitable for pumpable concrete in congested rebar cages."
        badge_cls = "badge-warning"
    else:
        slump_type = "Collapse Slump (Excessive Segregation)"
        workability_desc = "⚠️ Warning: Excess water causes mix bleeding, aggregate separation, and loss of 28-day strength."
        badge_cls = "badge-critical"

    with col_l1_res:
        st.markdown(f"""
        <div class="dark-card">
            <h4 class="accent-cyan" style="margin-top:0;">📊 Experimental Slump Reading</h4>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:12px; color:#94A3B8;">MEASURED SLUMP SUBSIDENCE</span>
                    <h1 class="accent-orange" style="margin:4px 0 0 0; font-size:42px;">{slump_mm:.1f} <span style="font-size:20px; color:#CBD5E1;">mm</span></h1>
                </div>
                <div>
                    <span class="{badge_cls}">● {slump_type.split('(')[0].strip().upper()}</span>
                </div>
            </div>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="margin:4px 0;"><b>IS 1199 Classification:</b> {slump_type}</p>
            <p style="margin:4px 0;"><b>Field Suitability:</b> {workability_desc}</p>
            <p style="margin:4px 0;"><b>Compaction Factor Equivalent:</b> ~{min(0.98, max(0.75, 0.72 + (slump_mm/700.0))):.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    cone_height = 300.0  # standard 300mm slump cone
    top_dia = 100.0
    bot_dia = 200.0

    orig_y = [0, cone_height, cone_height, 0]
    orig_x = [-bot_dia/2, -top_dia/2, top_dia/2, bot_dia/2]

    deformed_height = cone_height - slump_mm
    deformed_top_width = top_dia + (slump_mm * 0.4)
    deformed_bot_width = bot_dia + (slump_mm * 0.2)

    def_y = [0, deformed_height, deformed_height, 0]
    def_x = [-deformed_bot_width/2, -deformed_top_width/2, deformed_top_width/2, deformed_bot_width/2]

    fig_slump = go.Figure()
    fig_slump.add_trace(go.Scatter(x=orig_x + [orig_x[0]], y=orig_y + [orig_y[0]], mode='lines', name='Standard Metal Mold (300mm)', line=dict(color='#38BDF8', width=2, dash='dash')))
    fig_slump.add_trace(go.Scatter(x=def_x + [def_x[0]], y=def_y + [def_y[0]], fill='toself', fillcolor='rgba(249, 115, 22, 0.3)', name=f'Slumped Concrete ({slump_mm:.1f}mm)', line=dict(color='#F97316', width=3)))

    fig_slump.update_layout(
        title="Cross-Sectional Mold Subsidence Diagram (IS 7320)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        xaxis=dict(title=dict(text="Cone Base Width (mm)"), range=[-220, 220]),
        yaxis=dict(title=dict(text="Height Above Base Plate (mm)"), range=[0, 340])
    )
    st.plotly_chart(fig_slump, use_container_width=True)

    if st.button("💾 Record Lab 1 Data to Session Log", type="primary"):
        st.session_state.lab_completed_experiments["Lab 1"] = {
            "name": "Concrete Slump Cone Test (IS 7320)",
            "result": f"{slump_mm:.1f} mm ({slump_type})",
            "status": "Verified Complete",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success("✅ Lab 1 experimental trial recorded to official audit log!")

elif "Lab 2" in active_lab:
    st.markdown("## 🔬 Lab 2: Universal Testing Machine (UTM) Tensile Test (IS 1608 / ASTM E8)")
    st.caption(r"Apply monotonic axial tension to structural steel rebar to generate the complete Stress-Strain ($\sigma - \varepsilon$) constitutive curve.")

    col_l2_in, col_l2_res = st.columns([1, 1.2])

    with col_l2_in:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Rebar Specimen Geometry & Grade**")
        
        steel_grade = st.selectbox("TMT Steel Rebar Grade:", ["Fe 415 (Mild Deformed)", "Fe 500 (Standard TMT)", "Fe 550D (High Ductility Earthquake Grade)", "Fe 600 (High Strength)"], index=1)
        bar_diameter_mm = st.selectbox(r"Nominal Bar Diameter ($d_b$):", [8, 10, 12, 16, 20, 25, 32], index=3)  # 16mm default
        gauge_calc = float(round(5.65 * math.sqrt(math.pi * (bar_diameter_mm**2) / 4.0), 1))
        gauge_length_mm = st.number_input(r"Gauge Length ($L_0 = 5.65\sqrt{A_0}$):", min_value=50.0, max_value=300.0, value=gauge_calc, step=1.0)
        cross_area_mm2 = math.pi * (bar_diameter_mm ** 2) / 4.0
        st.markdown(f"• **Initial Cross-Sectional Area ($A_0$):** `{cross_area_mm2:.1f} mm²`")
        
        st.markdown("</div>", unsafe_allow_html=True)

    if "415" in steel_grade:
        fy = 415.0
        fu = 485.0
        rupture_strain = 0.18
    elif "500" in steel_grade:
        fy = 500.0
        fu = 545.0
        rupture_strain = 0.145
    elif "550" in steel_grade:
        fy = 550.0
        fu = 600.0
        rupture_strain = 0.160
    else:  # Fe 600
        fy = 600.0
        fu = 660.0
        rupture_strain = 0.120

    E_modulus = 200000.0  # MPa (200 GPa)
    yield_strain = fy / E_modulus

    # Generate multi-stage Stress-Strain curve
    strain_elastic = np.linspace(0, yield_strain, 30)
    stress_elastic = strain_elastic * E_modulus

    strain_plateau = np.linspace(yield_strain, yield_strain + 0.005, 10)
    stress_plateau = np.full_like(strain_plateau, fy)

    strain_hardening = np.linspace(yield_strain + 0.005, rupture_strain * 0.7, 40)
    stress_hardening = fy + (fu - fy) * np.sin(((strain_hardening - (yield_strain + 0.005)) / (rupture_strain * 0.7 - (yield_strain + 0.005))) * (math.pi / 2))

    strain_necking = np.linspace(rupture_strain * 0.7, rupture_strain, 20)
    stress_necking = fu - (fu * 0.12) * ((strain_necking - (rupture_strain * 0.7)) / (rupture_strain - rupture_strain * 0.7)) ** 2

    total_strain = np.concatenate([strain_elastic, strain_plateau, strain_hardening, strain_necking])
    total_stress = np.concatenate([stress_elastic, stress_plateau, stress_hardening, stress_necking])
    total_load_kN = (total_stress * cross_area_mm2) / 1000.0

    peak_load_kN = (fu * cross_area_mm2) / 1000.0
    yield_load_kN = (fy * cross_area_mm2) / 1000.0

    with col_l2_res:
        st.markdown(f"""
        <div class="dark-card">
            <h4 class="accent-cyan" style="margin-top:0;">📊 UTM Tensile Test Output</h4>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:12px; color:#94A3B8;">0.2% PROOF YIELD STRENGTH ($f_y$)</span>
                    <h2 class="accent-cyan" style="margin:2px 0 0 0;">{fy:.1f} MPa</h2>
                </div>
                <div>
                    <span style="font-size:12px; color:#94A3B8;">ULTIMATE TENSILE STRENGTH ($f_u$)</span>
                    <h2 class="accent-orange" style="margin:2px 0 0 0;">{fu:.1f} MPa</h2>
                </div>
            </div>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="margin:4px 0;">• <b>Peak Tensile Breaking Load:</b> <span class="accent-green" style="font-weight:bold;">{peak_load_kN:.1f} kN</span> ({round(peak_load_kN * 101.97, 0):,.0f} kgf)</p>
            <p style="margin:4px 0;">• <b>Yield Load Capacity:</b> {yield_load_kN:.1f} kN</p>
            <p style="margin:4px 0;">• <b>Total Percentage Elongation at Fracture:</b> {rupture_strain * 100:.1f}% (IS 1786 Min: 12%)</p>
            <p style="margin:4px 0;">• <b>Ductility Ratio ($f_u / f_y$):</b> {(fu/fy):.2f} (Compliant with Seismic Zone IV/V)</p>
        </div>
        """, unsafe_allow_html=True)

    fig_utm = go.Figure()
    fig_utm.add_trace(go.Scatter(x=total_strain * 100, y=total_stress, mode='lines', name=f'{steel_grade} Stress-Strain Curve', line=dict(color='#38BDF8', width=3)))
    fig_utm.add_trace(go.Scatter(x=[yield_strain * 100], y=[fy], mode='markers+text', name='Yield Point', text=[f"Yield: {fy} MPa"], textposition="top left", marker=dict(color='#10B981', size=10)))
    fig_utm.add_trace(go.Scatter(x=[rupture_strain * 0.7 * 100], y=[fu], mode='markers+text', name='Ultimate Point', text=[f"Peak: {fu} MPa"], textposition="top right", marker=dict(color='#F97316', size=10)))
    fig_utm.add_trace(go.Scatter(x=[rupture_strain * 100], y=[total_stress[-1]], mode='markers+text', name='Fracture Necking', text=["Fracture"], textposition="bottom right", marker=dict(color='#EF4444', size=10)))

    fig_utm.update_layout(
        title=f"Stress vs. Strain Constitutive Curve — {steel_grade} (Ø {bar_diameter_mm}mm)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        xaxis=dict(title=dict(text="Engineering Strain (%)")),
        yaxis=dict(title=dict(text="Engineering Stress (MPa)"))
    )
    st.plotly_chart(fig_utm, use_container_width=True)

    if st.button("💾 Record Lab 2 Data to Session Log", type="primary"):
        st.session_state.lab_completed_experiments["Lab 2"] = {
            "name": f"UTM Tensile Test on {steel_grade} (Ø{bar_diameter_mm}mm)",
            "result": f"Yield {fy} MPa | Ultimate {fu} MPa | Elongation {rupture_strain*100:.1f}%",
            "status": "Verified Complete",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success("✅ Lab 2 UTM Tensile trial recorded to official audit log!")

elif "Lab 3" in active_lab:
    st.markdown("## 📡 Lab 3: Ultrasonic Pulse Velocity (UPV) Non-Destructive Test (IS 516 Part 5 / ASTM C597)")
    st.caption("Measure longitudinal ultrasonic pulse transit speed through concrete members to assess internal density, micro-cracks, and honeycombing voids.")

    col_l3_in, col_l3_res = st.columns([1, 1.2])

    with col_l3_in:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Transducer Setup & Member Geometry**")

        transmission_mode = st.selectbox("Transducer Transmission Mode:", ["Direct Transmission (Opposite Faces)", "Semi-Direct Transmission (Adjacent Faces)", "Indirect / Surface Transmission (Same Face)"], index=0)
        path_length_mm = st.slider(r"Concrete Path Length ($L$ in mm):", min_value=100, max_value=1500, value=400, step=50)
        void_presence = st.selectbox("Internal Defect / Honeycombing Condition:", ["Solid Dense Concrete (No Voids)", "Minor Micro-Fissures (<0.2mm)", "Moderate Void Honeycombing", "Severe Internal Delamination / Rebar Voids"], index=1)
        transducer_freq = st.selectbox("Transducer Operating Frequency:", ["54 kHz (Standard Concrete)", "24 kHz (Heavy Mass / Aggregate Concrete)", "150 kHz (Mortar / Paste)"], index=0)

        st.markdown("</div>", unsafe_allow_html=True)

    path_m = path_length_mm / 1000.0

    if "Solid" in void_presence:
        base_velocity = 4.65  # km/s
    elif "Minor" in void_presence:
        base_velocity = 3.95  # km/s
    elif "Moderate" in void_presence:
        base_velocity = 3.25  # km/s
    else:
        base_velocity = 2.45  # km/s

    if "Semi-Direct" in transmission_mode:
        base_velocity *= 0.90
    elif "Indirect" in transmission_mode:
        base_velocity *= 0.82

    transit_time_microsec = round((path_m / base_velocity) * 1000.0, 1)
    measured_velocity_km_s = round(path_m / (transit_time_microsec / 1000.0), 2)

    if measured_velocity_km_s > 4.5:
        upv_quality = "EXCELLENT"
        upv_desc = "Dense, defect-free concrete. Compressive strength > 35 MPa."
        badge_cls = "badge-success"
    elif measured_velocity_km_s >= 3.5:
        upv_quality = "GOOD"
        upv_desc = "Sound structural concrete with minor natural micro-pores. Normal serviceability."
        badge_cls = "badge-blue"
    elif measured_velocity_km_s >= 3.0:
        upv_quality = "MEDIUM (Doubtful)"
        upv_desc = "Micro-fissures or minor compaction voids present. Monitor load concentration."
        badge_cls = "badge-warning"
    else:
        upv_quality = "POOR (Severe Honeycombing)"
        upv_desc = "Internal delamination, honeycombing voids, or cracked rebar interface. Grouting required."
        badge_cls = "badge-critical"

    with col_l3_res:
        st.markdown(f"""
        <div class="dark-card">
            <h4 class="accent-cyan" style="margin-top:0;">📊 UPV Diagnostic Readout</h4>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:12px; color:#94A3B8;">ULTRASONIC VELOCITY ($V$)</span>
                    <h1 class="accent-cyan" style="margin:2px 0 0 0; font-size:40px;">{measured_velocity_km_s} <span style="font-size:18px; color:#CBD5E1;">km/s</span></h1>
                </div>
                <div>
                    <span class="{badge_cls}">● {upv_quality}</span>
                </div>
            </div>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="margin:4px 0;">• <b>Measured Pulse Transit Time ($T$):</b> <span class="accent-orange" style="font-weight:bold;">{transit_time_microsec} µs</span></p>
            <p style="margin:4px 0;">• <b>Acoustic Path Distance ($L$):</b> {path_length_mm} mm ({path_m} m)</p>
            <p style="margin:4px 0;">• <b>IS 516 Rating:</b> {upv_desc}</p>
            <p style="margin:4px 0;">• <b>Estimated Dynamic Elastic Modulus ($E_d$):</b> ~{round(2400 * (measured_velocity_km_s * 1000)**2 / 1e9, 1)} GPa</p>
        </div>
        """, unsafe_allow_html=True)

    fig_upv = go.Figure(go.Indicator(
        mode="gauge+number",
        value=measured_velocity_km_s,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "IS 516 UPV Concrete Rating (km/s)", 'font': {'color': '#CBD5E1'}},
        gauge={
            'axis': {'range': [1.5, 5.0], 'tickwidth': 1, 'tickcolor': '#94A3B8'},
            'bar': {'color': '#38BDF8'},
            'steps': [
                {'range': [1.5, 3.0], 'color': 'rgba(239, 68, 68, 0.4)'},
                {'range': [3.0, 3.5], 'color': 'rgba(249, 115, 22, 0.4)'},
                {'range': [3.5, 4.5], 'color': 'rgba(2, 132, 199, 0.4)'},
                {'range': [4.5, 5.0], 'color': 'rgba(16, 185, 129, 0.4)'}
            ],
            'threshold': {
                'line': {'color': "#10B981", 'width': 4},
                'thickness': 0.75,
                'value': 4.5
            }
        }
    ))
    fig_upv.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(l=20, r=20, t=30, b=10))
    st.plotly_chart(fig_upv, use_container_width=True)

    if st.button("💾 Record Lab 3 Data to Session Log", type="primary"):
        st.session_state.lab_completed_experiments["Lab 3"] = {
            "name": "Ultrasonic Pulse Velocity Test (IS 516)",
            "result": f"{measured_velocity_km_s} km/s ({upv_quality})",
            "status": "Verified Complete",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success("✅ Lab 3 UPV trial recorded to official audit log!")

elif "Lab 4" in active_lab:
    st.markdown("## 🔨 Lab 4: Schmidt Rebound Hammer Surface Hardness Test (IS 516 Part 5)")
    st.caption(r"Assess surface hardness and estimate in-situ compressive strength of concrete members through non-destructive rebound number ($R$) calibration.")

    col_l4_in, col_l4_res = st.columns([1, 1.2])

    with col_l4_in:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Hammer Test Parameters**")

        hammer_orientation = st.selectbox("Impact Orientation Angle:", ["Horizontal (0° - Beam/Column Sides)", "Vertically Downward (-90° - Floor Slab)", "Vertically Upward (+90° - Slab Soffit Ceiling)"], index=0)
        target_concrete_age = st.selectbox("Concrete Curing Age:", ["7 Days", "14 Days", "28 Days (Standard Design Age)", "90+ Days (Mature Concrete)"], index=2)
        carbonation_layer = st.slider("Surface Carbonation Layer Depth (mm):", min_value=0.0, max_value=8.0, value=1.0, step=0.5)

        st.markdown(r"##### **10 Single-Point Impact Readings ($R_i$):**")
        r_cols = st.columns(5)
        rebound_readings = []
        default_r = [36, 38, 35, 37, 39, 36, 38, 34, 37, 36]
        for idx in range(10):
            with r_cols[idx % 5]:
                val = st.number_input(f"R#{idx+1}", min_value=10, max_value=60, value=default_r[idx], key=f"r_inp_{idx}")
                rebound_readings.append(val)

        st.markdown("</div>", unsafe_allow_html=True)

    mean_r = np.mean(rebound_readings)
    # Exclude outliers differing by more than +/- 6 units
    filtered_r = [r for r in rebound_readings if abs(r - mean_r) <= 6.0]
    final_rebound_r = round(np.mean(filtered_r), 1)

    # Orientation correction factor
    if "Downward" in hammer_orientation:
        corr_r = final_rebound_r - 2.5
    elif "Upward" in hammer_orientation:
        corr_r = final_rebound_r + 2.5
    else:
        corr_r = final_rebound_r

    # Compressive strength empirical formula: f_ck = 0.018 * R^2 + 0.42 * R - carbonation
    est_comp_strength_mpa = round(0.018 * (corr_r ** 2) + 0.42 * corr_r - (carbonation_layer * 0.8), 1)

    with col_l4_res:
        st.markdown(f"""
        <div class="dark-card">
            <h4 class="accent-cyan" style="margin-top:0;">📊 Rebound Hammer Strength Takeoff</h4>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:12px; color:#94A3B8;">MEAN REBOUND NUMBER ($R$)</span>
                    <h2 class="accent-orange" style="margin:2px 0 0 0;">{final_rebound_r}</h2>
                </div>
                <div>
                    <span style="font-size:12px; color:#94A3B8;">ESTIMATED COMPRESSIVE STRENGTH</span>
                    <h1 class="accent-green" style="margin:2px 0 0 0; font-size:36px;">{est_comp_strength_mpa} <span style="font-size:18px; color:#CBD5E1;">MPa</span></h1>
                </div>
            </div>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="margin:4px 0;">• <b>Impact Angle Correction:</b> {hammer_orientation.split('(')[0]}</p>
            <p style="margin:4px 0;">• <b>Validated Readings Count:</b> {len(filtered_r)} of 10 points (Outliers suppressed)</p>
            <p style="margin:4px 0;">• <b>Concrete Grade Match:</b> ~<b>M{int(round(est_comp_strength_mpa/5.0)*5)}</b> Equivalent</p>
        </div>
        """, unsafe_allow_html=True)

    r_curve_x = np.linspace(15, 55, 100)
    r_curve_y = 0.018 * (r_curve_x ** 2) + 0.42 * r_curve_x

    fig_rh = go.Figure()
    fig_rh.add_trace(go.Scatter(x=r_curve_x, y=r_curve_y, mode='lines', name='IS 516 Calibration Curve', line=dict(color='#38BDF8', width=2)))
    fig_rh.add_trace(go.Scatter(x=[corr_r], y=[est_comp_strength_mpa], mode='markers+text', name='In-Situ Test Point', text=[f"R={corr_r:.1f} → {est_comp_strength_mpa} MPa"], textposition="top left", marker=dict(color='#10B981', size=12)))

    fig_rh.update_layout(
        title="Schmidt Hammer Calibration Chart: Rebound No. vs. In-Situ Strength",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        xaxis=dict(title=dict(text="Corrected Rebound Number (R)")),
        yaxis=dict(title=dict(text="Estimated Compressive Strength (MPa)"))
    )
    st.plotly_chart(fig_rh, use_container_width=True)

    if st.button("💾 Record Lab 4 Data to Session Log", type="primary"):
        st.session_state.lab_completed_experiments["Lab 4"] = {
            "name": "Schmidt Rebound Hammer Test (IS 516)",
            "result": f"R={final_rebound_r} → {est_comp_strength_mpa} MPa (~M{int(round(est_comp_strength_mpa/5.0)*5)})",
            "status": "Verified Complete",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success("✅ Lab 4 Rebound Hammer trial recorded to official audit log!")

elif "Lab 5" in active_lab:
    st.markdown("## ⏳ Lab 5: Fine Aggregate Sieve Analysis & Fineness Modulus (IS 2386 / ASTM C136)")
    st.caption("Determine particle size distribution of sand, compute Fineness Modulus (FM), and classify against IS 383 Grading Zones (I to IV).")

    col_l5_in, col_l5_res = st.columns([1.1, 1])

    with col_l5_in:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Sieve Stack Retained Masses (Total Sample: 1000g)**")
        
        sieves = ["4.75 mm", "2.36 mm", "1.18 mm", "600 µm", "300 µm", "150 µm", "Pan (<150µm)"]
        default_retained = [25.0, 95.0, 240.0, 310.0, 210.0, 95.0, 25.0]

        retained_masses = []
        for s_label, def_mass in zip(sieves, default_retained):
            val = st.number_input(f"Retained on {s_label} (g):", min_value=0.0, max_value=1000.0, value=def_mass, step=5.0)
            retained_masses.append(val)

        st.markdown("</div>", unsafe_allow_html=True)

    total_mass = sum(retained_masses)
    pct_retained = [(m / total_mass) * 100.0 for m in retained_masses]
    cum_retained = np.cumsum(pct_retained).tolist()
    pct_passing = [100.0 - c for c in cum_retained]

    # Fineness Modulus = Sum of cumulative % retained on standard sieves (excluding Pan) / 100
    fineness_modulus = round(sum(cum_retained[:-1]) / 100.0, 2)

    if fineness_modulus > 3.2:
        sand_zone = "Zone I (Coarse Sand)"
        sand_suitability = "Suitable for heavy mass concrete & thick RCC columns."
    elif fineness_modulus >= 2.6:
        sand_zone = "Zone II (Medium Sand - Standard)"
        sand_suitability = "Ideal for general structural RCC beams, columns, and slabs."
    elif fineness_modulus >= 2.2:
        sand_zone = "Zone III (Fine Sand)"
        sand_suitability = "Recommended for masonry mortars and internal plaster rendering."
    else:
        sand_zone = "Zone IV (Very Fine Sand)"
        sand_suitability = "Suitable for finishing plasters only; not recommended for structural RCC."

    sieve_df = pd.DataFrame({
        "IS Sieve Size": sieves,
        "Retained Mass (g)": retained_masses,
        "Individual % Retained": [f"{p:.1f}%" for p in pct_retained],
        "Cumulative % Retained": [f"{c:.1f}%" for c in cum_retained],
        "% Passing": [f"{p:.1f}%" for p in pct_passing]
    })

    with col_l5_res:
        st.markdown(f"""
        <div class="dark-card">
            <h4 class="accent-cyan" style="margin-top:0;">📊 Particle Grading Takeoff</h4>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:12px; color:#94A3B8;">FINENESS MODULUS (FM)</span>
                    <h1 class="accent-cyan" style="margin:2px 0 0 0; font-size:38px;">{fineness_modulus}</h1>
                </div>
                <div>
                    <span class="badge-success">● {sand_zone.split('(')[0].strip()}</span>
                </div>
            </div>
            <hr style="border-color:rgba(255,255,255,0.08);">
            <p style="margin:4px 0;">• <b>IS 383 Grading:</b> {sand_zone}</p>
            <p style="margin:4px 0;">• <b>Engineering Application:</b> {sand_suitability}</p>
            <p style="margin:4px 0;">• <b>Total Sieve Mass Checked:</b> {total_mass:.1f} g</p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(sieve_df, use_container_width=True, hide_index=True)

    sieve_microns = [4750, 2360, 1180, 600, 300, 150, 75]
    fig_sieve = go.Figure()
    fig_sieve.add_trace(go.Scatter(x=sieve_microns, y=pct_passing, mode='lines+markers', name='Experimental Sample Curve', line=dict(color='#38BDF8', width=3), marker=dict(size=8, color='#F97316')))

    fig_sieve.update_layout(
        title="Particle Size Distribution Semi-Log Curve (IS 2386)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=330,
        xaxis=dict(title=dict(text="Sieve Aperture Size (µm) - Log Scale"), type="log", autorange="reversed"),
        yaxis=dict(title=dict(text="Percentage Passing (%)"), range=[0, 105])
    )
    st.plotly_chart(fig_sieve, use_container_width=True)

    if st.button("💾 Record Lab 5 Data to Session Log", type="primary"):
        st.session_state.lab_completed_experiments["Lab 5"] = {
            "name": "Fine Aggregate Sieve Analysis (IS 2386)",
            "result": f"FM = {fineness_modulus} ({sand_zone})",
            "status": "Verified Complete",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success("✅ Lab 5 Sieve Analysis trial recorded to official audit log!")

else:
    st.markdown("## 🎓 Lab 6: Virtual Practical Assessment & Completion Certificate")
    st.caption("Verify practical lab accomplishments, review experiment trails, and generate your certified completion transcript.")

    st.markdown("### 📋 Completed Virtual Practical Ledger")
    
    if st.session_state.lab_completed_experiments:
        completed_df = pd.DataFrame([
            {"Experiment Code": code, "Experiment Title": data["name"], "Recorded Diagnostic Value": data["result"], "Status": data["status"], "Timestamp": data["timestamp"]}
            for code, data in st.session_state.lab_completed_experiments.items()
        ])
        st.dataframe(completed_df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ No practical trials recorded yet in this session. Run experiments in Labs 1 to 5 to populate your ledger.")

    st.divider()
    st.markdown("### 📜 Virtual Practical Certificate Generator")

    c_cert1, c_cert2 = st.columns(2)
    with c_cert1:
        student_name = st.text_input("Student / Engineer Full Name:", "Er. Ritika Bhumkar")
        roll_no = st.text_input("Enrollment / Candidate ID:", "CV-CIVIL-2026-042")
    with c_cert2:
        inst_name = st.text_input("Institution / Organization:", "Department of Civil Engineering & Solapur Smart Infrastructure")
        evaluator = st.selectbox("Faculty Evaluator / Authority:", ["Er. Ritika Bhumkar & Er. Laiba Mulani (Lead Devs)", "Head of Department (Civil Engineering)"])

    cert_txt = f"""================================================================================
CONSTRUCTVISION AI — CIVIL ENGINEERING VIRTUAL PRACTICAL CERTIFICATE
================================================================================
Candidate Name    : {student_name}
Enrollment ID     : {roll_no}
Institution       : {inst_name}
Issued Date       : {datetime.now().strftime('%d %B %Y')}
Evaluated By      : {evaluator}
================================================================================
COMPLETED PRACTICAL EXPERIMENTS & AUDIT TRAIL:
"""
    for code, data in st.session_state.lab_completed_experiments.items():
        cert_txt += f"  • [{code}] {data['name']}\n    Result: {data['result']} | Verified: {data['timestamp']}\n\n"

    cert_txt += f"""--------------------------------------------------------------------------------
STATUS: OFFICIALLY CERTIFIED (IS 456 / IS 516 / IS 1608 / IS 2386 COMPLIANT)
System Certificate ID: CV-CERT-{datetime.now().strftime('%Y%m%d%H%M')}
Developed by Er. Ritika Bhumkar & Er. Laiba Mulani | Department of Civil Engineering
================================================================================"""

    st.download_button(
        label="📥 Download Certified Virtual Practical Transcript (.TXT)",
        data=cert_txt,
        file_name=f"Practical_Certificate_{roll_no}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )

st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI VIRTUAL LAB ENGINE</b> | IS & ASTM Civil Engineering Testing Simulators<br>
    Developed by <b>Er. Ritika Bhumkar</b> & <b>Er. Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
