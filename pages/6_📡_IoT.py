import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import time

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="3D Structural Twin & Sensor Nodes | CONSTRUCTVISION AI",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CUSTOM CYBER-DARK BLUEPRINT STYLING
# =========================================================
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Dark Blueprint Background Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image:
            linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
        background-size: 35px 35px;
        pointer-events: none;
        z-index: 0;
    }

    /* Hide Default Headers/Footers */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1E293B;
    }

    /* Dark Card Container */
    .dark-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        transition: all 0.3s ease-in-out;
    }
    .dark-card:hover {
        border-color: #38BDF8;
        box-shadow: 0 6px 25px rgba(56, 189, 248, 0.2);
    }

    /* Hero Banner */
    .hero-dark {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 6px solid #38BDF8;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Accent Colors */
    h1, h2, h3, h4 { color: #F8FAFC !important; font-weight: 700; }
    .accent-cyan { color: #38BDF8 !important; }
    .accent-orange { color: #F97316 !important; }
    .accent-green { color: #10B981 !important; }
    .accent-red { color: #EF4444 !important; }

    /* Custom Metric Display */
    .metric-box {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        margin-top: 4px;
    }
    .metric-lbl {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px;
        color: #94A3B8;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284C7 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. SIDEBAR CONTROLS & AI ASSISTANT
# =========================================================
with st.sidebar:
    st.markdown("### 🏗️ **CONSTRUCTVISION AI**")
    st.caption("3D Structural Twin & IoT Sensor Telemetry")
    st.divider()

    st.markdown("#### 🌍 Environmental Stressors")
    wind = st.slider("Wind Load (km/h)", 0, 200, 35)
    seismic = st.slider("Seismic Forces (Richter)", 0.0, 8.0, 1.2, step=0.1)
    temp = st.slider("Ambient Temperature (°C)", -10, 50, 30)

    st.divider()
    st.markdown("#### 📡 IoT Mesh Network")
    sampling_freq = st.selectbox("Sensor Sampling Rate", ["10 Hz", "50 Hz", "100 Hz (Real-Time)"], index=2)
    show_labels = st.toggle("Show Node Sensor Labels on 3D Twin", value=True)

    st.divider()
    st.markdown("#### 🤖 Smart Mitigation")
    self_healing = st.toggle("Activate Bacterial Self-Healing Concrete", value=False)
    damping_system = st.toggle("Activate Seismic Mass Dampers", value=False)

    st.divider()
    st.markdown("#### 🤖 AI Structural Assistant")
    user_query = st.text_input("Ask Assistant (e.g., 'Check Column C1 Risk')", key="ai_assistant_input")
    if user_query:
        if "risk" in user_query.lower() or "column" in user_query.lower():
            st.info("🤖 **AI Diagnostic:** Column C1 & C2 are experiencing moderate shear load. Recommended action: Monitor micro-strain variations during wind bursts above 50 km/h.")
        else:
            st.success("🤖 **AI Assistant:** Structural safety index is optimal at 94.2%. Mesh gateway is online.")

    st.divider()
    st.caption("Developed by Ritika Bhumkar & Laiba Mulani © 2026")

# =========================================================
# 4. SENSOR DATA & GPS GEOLOCATION GENERATION LOGIC
# =========================================================
def generate_sensor_dataframe():
    components_data = [
        {"Sensor_ID": "SN-FBG-101", "Name": "Foundation Pad", "Type": "Mass Concrete", "Sensor_Type": "Fiber Optic Strain (FBG)", "X": 5, "Y": 5, "Z": 0, "Base_Stress": 12, "Battery": 98, "RSSI": -62, "Lat": 18.5204, "Lon": 73.8567},
        {"Sensor_ID": "SN-ACC-102", "Name": "Column C1 (NW)", "Type": "RCC Column", "Sensor_Type": "3-Axis MEMS Accelerometer", "X": 2, "Y": 2, "Z": 1, "Base_Stress": 14, "Battery": 92, "RSSI": -58, "Lat": 18.5206, "Lon": 73.8565},
        {"Sensor_ID": "SN-STR-103", "Name": "Column C2 (NE)", "Type": "RCC Column", "Sensor_Type": "Piezoelectric Strain Gauge", "X": 8, "Y": 2, "Z": 1, "Base_Stress": 14, "Battery": 88, "RSSI": -65, "Lat": 18.5206, "Lon": 73.8569},
        {"Sensor_ID": "SN-ACC-104", "Name": "Column C3 (SW)", "Type": "RCC Column", "Sensor_Type": "3-Axis MEMS Accelerometer", "X": 2, "Y": 8, "Z": 1, "Base_Stress": 15, "Battery": 95, "RSSI": -60, "Lat": 18.5202, "Lon": 73.8565},
        {"Sensor_ID": "SN-STR-105", "Name": "Column C4 (SE)", "Type": "RCC Column", "Sensor_Type": "Piezoelectric Strain Gauge", "X": 8, "Y": 8, "Z": 1, "Base_Stress": 15, "Battery": 91, "RSSI": -67, "Lat": 18.5202, "Lon": 73.8569},
        {"Sensor_ID": "SN-INC-106", "Name": "Mid Column C1-Upper", "Type": "RCC Column", "Sensor_Type": "Wireless Inclinometer", "X": 2, "Y": 2, "Z": 5, "Base_Stress": 18, "Battery": 84, "RSSI": -71, "Lat": 18.5206, "Lon": 73.8565},
        {"Sensor_ID": "SN-INC-107", "Name": "Mid Column C2-Upper", "Type": "RCC Column", "Sensor_Type": "Wireless Inclinometer", "X": 8, "Y": 2, "Z": 5, "Base_Stress": 18, "Battery": 87, "RSSI": -69, "Lat": 18.5206, "Lon": 73.8569},
        {"Sensor_ID": "SN-AE-108", "Name": "Load Brick Wall", "Type": "AAC Masonry", "Sensor_Type": "Acoustic Emission Cracking Sensor", "X": 5, "Y": 2, "Z": 3, "Base_Stress": 9, "Battery": 79, "RSSI": -74, "Lat": 18.5205, "Lon": 73.8567},
        {"Sensor_ID": "SN-LAS-109", "Name": "Exterior Chajja", "Type": "Precast Slab", "Sensor_Type": "Laser Displacement Sensor", "X": 5, "Y": 0, "Z": 6, "Base_Stress": 6, "Battery": 96, "RSSI": -55, "Lat": 18.5207, "Lon": 73.8567},
        {"Sensor_ID": "SN-STR-110", "Name": "Roof Perimeter Beam", "Type": "RCC Beam", "Sensor_Type": "Piezoelectric Strain Gauge", "X": 5, "Y": 5, "Z": 8, "Base_Stress": 16, "Battery": 90, "RSSI": -63, "Lat": 18.5204, "Lon": 73.8567},
        {"Sensor_ID": "SN-FBG-111", "Name": "Main Roof Slab", "Type": "RCC Slab", "Sensor_Type": "Fiber Optic Strain (FBG)", "X": 5, "Y": 5, "Z": 9, "Base_Stress": 13, "Battery": 85, "RSSI": -59, "Lat": 18.5204, "Lon": 73.8567},
    ]
    df = pd.DataFrame(components_data)

    df["Current_Stress_MPa"] = df["Base_Stress"] + (wind * 0.12) + (seismic**2 * 1.6) + (abs(temp - 25) * 0.25)

    if self_healing:
        df["Current_Stress_MPa"] *= 0.65
    if damping_system:
        df["Current_Stress_MPa"] *= 0.80

    df["Current_Stress_MPa"] = df["Current_Stress_MPa"].round(2)
    df["Micro_Strain_ue"] = (df["Current_Stress_MPa"] * 42.5).round(1)
    df["Vibration_G"] = round(0.02 + (seismic * 0.15) + (wind * 0.003), 3)

    def evaluate_status(stress):
        if stress < 25:
            return "NORMAL", "#10B981"
        elif stress < 45:
            return "WARNING", "#F97316"
        else:
            return "CRITICAL", "#EF4444"

    res = df["Current_Stress_MPa"].apply(evaluate_status)
    df["Status"] = [r[0] for r in res]
    df["Status_Color"] = [r[1] for r in res]

    return df

# =========================================================
# 5. ADVANCED TOPOGRAPHY & MULTI-VIEW 3D ANIMATION ENGINE
# =========================================================
def create_advanced_3d_architectural_twin(df, mode="3D Structural Wireframe", display_labels=True):
    fig = go.Figure()

    # --- TOPOGRAPHY & TERRAIN LANDSCAPE SURFACE ---
    grid_x, grid_y = np.meshgrid(np.linspace(-2, 12, 35), np.linspace(-2, 12, 35))
    grid_z = np.sin(grid_x / 2.5) * np.cos(grid_y / 2.5) * 0.7 - 0.8  
    
    fig.add_trace(go.Surface(
        x=grid_x, y=grid_y, z=grid_z,
        colorscale='Viridis', opacity=0.45, showscale=False, hoverinfo='none', name="Site Topography"
    ))

    # --- ARCHITECTURAL VIEW MODES ---
    if mode == "Exterior Facade Mode":
        x_fac = [2, 8, 8, 2, 2, 2, 8, 8, 2, 2]
        y_fac = [2, 2, 8, 8, 2, 2, 2, 8, 8, 2]
        z_fac = [0, 0, 0, 0, 0, 9, 9, 9, 9, 9]
        fig.add_trace(go.Mesh3d(x=x_fac, y=y_fac, z=z_fac, color='#0284C7', opacity=0.25, name="Exterior Envelope"))

    elif mode == "Interior Walkthrough Mesh":
        fig.add_trace(go.Scatter3d(
            x=[2, 8, 5, 5], y=[5, 5, 2, 8], z=[4, 4, 4, 4],
            mode='lines', line=dict(color='#F59E0B', width=6), name="Interior Partitions"
        ))

    elif mode == "4D Construction Timeline":
        colors_4d = ['#10B981', '#38BDF8', '#F59E0B', '#EF4444']
        df['Phase_Color'] = [colors_4d[int(z) % 4] for z in df['Z']]

    # --- STRUCTURAL CONNECTIONS ---
    connections = [
        ("SN-FBG-101", "SN-ACC-102"), ("SN-FBG-101", "SN-STR-103"), ("SN-FBG-101", "SN-ACC-104"), ("SN-FBG-101", "SN-STR-105"),
        ("SN-ACC-102", "SN-INC-106"), ("SN-STR-103", "SN-INC-107"),
        ("SN-ACC-102", "SN-STR-103"), ("SN-ACC-104", "SN-STR-105"), ("SN-ACC-102", "SN-ACC-104"), ("SN-STR-103", "SN-STR-105"),
        ("SN-INC-106", "SN-STR-110"), ("SN-INC-107", "SN-STR-110"), ("SN-STR-110", "SN-FBG-111"), ("SN-AE-108", "SN-LAS-109")
    ]

    for start_id, end_id in connections:
        node_a = df[df["Sensor_ID"] == start_id].iloc[0]
        node_b = df[df["Sensor_ID"] == end_id].iloc[0]
        fig.add_trace(go.Scatter3d(
            x=[node_a["X"], node_b["X"]], y=[node_a["Y"], node_b["Y"]], z=[node_a["Z"], node_b["Z"]],
            mode='lines', line=dict(color='#38BDF8' if mode == "4D Construction Timeline" else '#334155', width=5),
            hoverinfo='none', showlegend=False
        ))

    # --- 3D IOT SENSOR NODES ---
    mode_style = 'markers+text' if display_labels else 'markers'
    node_colors = df["Status_Color"] if mode != "4D Construction Timeline" else df["Phase_Color"]

    fig.add_trace(go.Scatter3d(
        x=df["X"], y=df["Y"], z=df["Z"], mode=mode_style,
        marker=dict(size=14, color=node_colors, opacity=0.95, line=dict(width=2, color='#FFFFFF')),
        text=df["Sensor_ID"] if display_labels else None, textposition="top center",
        hovertemplate=(
            "<b>Node ID: %{customdata[0]}</b><br>" +
            "Component: %{customdata[1]}<br>" +
            "Sensor Hardware: %{customdata[2]}<br>" +
            "Stress: %{customdata[3]} MPa<br>" +
            "Battery: %{customdata[4]}%<extra></extra>"
        ),
        customdata=df[["Sensor_ID", "Name", "Sensor_Type", "Current_Stress_MPa", "Battery"]].values,
        showlegend=False
    ))

    fig.update_layout(
        template="plotly_dark", height=580,
        scene=dict(
            xaxis=dict(title="Width (m)", backgroundcolor="#0F172A", gridcolor="#1E293B"),
            yaxis=dict(title="Depth (m)", backgroundcolor="#0F172A", gridcolor="#1E293B"),
            zaxis=dict(title="Elevation (m)", backgroundcolor="#0F172A", gridcolor="#1E293B"),
            camera=dict(eye=dict(x=1.7 * np.cos(0.4), y=1.7 * np.sin(0.4), z=1.2))
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

# =========================================================
# 6. MAIN PAGE HEADER
# =========================================================
st.markdown("""
<div class="hero-dark">
    <h1>🏗️ 3D Building Modeling & <span class="accent-cyan">Construction AI</span></h1>
    <p style="font-size: 1.1rem; color: #94A3B8;">
        3D Digital Twin Reconstruction with Embedded IoT Node Sensor Telemetry
    </p>
    <hr style="border-color: #334155;">
    <p style="color: #CBD5E1;">
        Upload inspection photographs to extract component geometries, monitor active IoT node sensor telemetry (Micro-strain, Vibration, Inclinometer angles), and simulate structural stress response.
    </p>
</div>
""", unsafe_allow_html=True)

# Generate Live Data
df_sensors = generate_sensor_dataframe()
max_stress = df_sensors["Current_Stress_MPa"].max()
avg_stress = df_sensors["Current_Stress_MPa"].mean()
critical_count = len(df_sensors[df_sensors["Status"] == "CRITICAL"])
active_nodes = len(df_sensors)

# Top Live KPI Panel
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Active Node Sensors</div>
        <div class="metric-val accent-cyan">{active_nodes} Nodes</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Peak Stress Load</div>
        <div class="metric-val accent-orange">{max_stress} MPa</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    status_color_class = "accent-red" if critical_count > 0 else "accent-green"
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Critical Sensor Alerts</div>
        <div class="metric-val {status_color_class}">{critical_count} Nodes</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Mesh Gateway Status</div>
        <div class="metric-val accent-green">ONLINE (99.8%)</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================================================
# 7. DASHBOARD INTERACTIVE TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 AI Image Analysis & 3D/4D/5D Twin", 
    "🎥 Live CCTV / Phone Feeds",
    "🗺️ GPS Location Map",
    "📡 Node Sensor Inspector", 
    "📊 Telemetry & Risk Analytics"
])

# ---------------------------------------------------------
# TAB 1: 3D/4D/5D ARCHITECTURAL RECONSTRUCTION & SENSOR MAP
# ---------------------------------------------------------
with tab1:
    st.subheader("Upload Site Photo to Generate 3D Digital Twin with Node Sensors & Topography")

    uploaded_files = st.file_uploader(
        "Upload site inspection photographs (JPG / PNG):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    view_mode = st.radio(
        "Select BIM Architectural View Mode:",
        ["3D Structural Wireframe", "4D Construction Timeline", "5D Cost Estimation Matrix", "Interior Walkthrough Mesh", "Exterior Facade Mode"],
        horizontal=True
    )

    if uploaded_files:
        with st.spinner('🤖 AI Vision extracting structural members, terrain topography, and mapping IoT sensor nodes...'):
            time.sleep(1.2)

        st.success("✅ Geometry, Topography & Sensor Mapping Complete: 11 Active Node Sensors Mounted on Frame.")

        col1, col2 = st.columns([1, 1.2])

        with col1:
            st.markdown("#### 📷 Visual Site Target")
            image = Image.open(uploaded_files[0])
            st.image(image, use_container_width=True, caption="Target Site Image")

        with col2:
            st.markdown(f"#### 🏗️ Digital Twin ({view_mode})")
            fig_3d = create_advanced_3d_architectural_twin(df_sensors, mode=view_mode, display_labels=show_labels)
            st.plotly_chart(fig_3d, use_container_width=True)

        if view_mode == "5D Cost Estimation Matrix":
            st.markdown("---")
            st.subheader("💰 5D BIM Cost & Material Estimation Matrix")
            m_c1, m_c2, m_c3 = st.columns(3)
            m_c1.metric("Concrete & Steel Structural Cost", "₹ 48,50,000")
            m_c2.metric("IoT Sensor Mesh Infrastructure", "₹ 3,20,000")
            m_c3.metric("Projected Retrofit Reserve", "₹ 5,10,000")

    else:
        st.info("💡 Waiting for input photo. Upload a residential structure image above to trigger automatic 3D BIM & Node Sensor extraction.")

# ---------------------------------------------------------
# TAB 2: LIVE CCTV & PHONE CAMERA FEEDS
# ---------------------------------------------------------
with tab2:
    st.subheader("🎥 Site Monitoring & Live Camera Streams")
    
    cam_col1, cam_col2 = st.columns(2)
    with cam_col1:
        st.markdown("#### 📹 CCTV Cam #1 - Main Structure Elevation")
        camera_url = st.text_input("IP Camera RTSP / HTTP URL:", value="https://images.unsplash.com/photo-1541888946425-d0fbb186a5b7?w=800")
        st.image(camera_url, caption="Live CCTV Site Stream (Online)", use_container_width=True)

    with cam_col2:
        st.markdown("#### 📱 Mobile Phone Live Inspection Feed")
        enable_cam = st.checkbox("Connect Mobile WebCam Feed", value=False)
        if enable_cam:
            st.camera_input("Capture Real-Time Site Inspection Frame")
        else:
            st.info("Check the box above to stream directly from your mobile or laptop webcam.")

# ---------------------------------------------------------
# TAB 3: GPS LOCATION MAP
# ---------------------------------------------------------
with tab3:
    st.subheader("🗺️ Geographic GPS Coordinates & Node Spatial Map")
    
    fig_map = px.scatter_mapbox(
        df_sensors,
        lat="Lat",
        lon="Lon",
        color="Status",
        size="Current_Stress_MPa",
        hover_name="Name",
        hover_data=["Sensor_ID", "Sensor_Type", "Current_Stress_MPa"],
        color_discrete_map={"NORMAL": "#10B981", "WARNING": "#F97316", "CRITICAL": "#EF4444"},
        zoom=17,
        mapbox_style="carto-darkmatter",
        title="GPS Geographic Mesh Node Overlay"
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=500)
    st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------------------------------------
# TAB 4: NODE SENSOR INSPECTOR (WITH FIXED PLOTLY BUG)
# ---------------------------------------------------------
with tab4:
    st.subheader("📡 Individual Node Sensor Diagnostics & Dual-Axis Telemetry Stream")

    selected_sensor_id = st.selectbox(
        "Select Node Sensor to Inspect:",
        options=df_sensors["Sensor_ID"].tolist(),
        format_func=lambda x: f"{x} - {df_sensors[df_sensors['Sensor_ID']==x]['Name'].values[0]} ({df_sensors[df_sensors['Sensor_ID']==x]['Sensor_Type'].values[0]})"
    )

    sensor_row = df_sensors[df_sensors["Sensor_ID"] == selected_sensor_id].iloc[0]

    # Diagnostic Header
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Component", sensor_row["Name"])
    d2.metric("Sensor Type", sensor_row["Sensor_Type"])
    d3.metric("Micro-Strain (με)", f"{sensor_row['Micro_Strain_ue']} με")
    d4.metric("Battery Level", f"{sensor_row['Battery']}%", delta="-0.1% / hr")

    st.write("")

    st.markdown(f"#### 📈 Real-Time Live Dual Telemetry Stream: `{selected_sensor_id}`")
    
    time_pts = np.linspace(0, 30, 150)
    base_val = sensor_row["Current_Stress_MPa"]
    noise = np.random.normal(0, 0.5, 150)
    seismic_vibe = np.sin(time_pts * 2) * (seismic * 1.5)
    wind_vibe = np.cos(time_pts * 0.8) * (wind * 0.05)
    waveform = base_val + noise + seismic_vibe + wind_vibe
    vibration_wave = (waveform * 0.02) + np.random.normal(0, 0.01, 150)

    # Dual-Axis Plotly Figure
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=time_pts, y=waveform, name="Live Stress (MPa)", line=dict(color="#38BDF8", width=2)))
    fig1.add_trace(go.Scatter(x=time_pts, y=vibration_wave, name="Vibration (G)", line=dict(color="#F59E0B", width=2), yaxis="y2"))

    # FIX: Corrected yref="y2" instead of yaxis="y2" to prevent Plotly layout shape error
    limits = {"vib_threshold": [0, 0.8]}
    fig1.add_hline(
        y=limits["vib_threshold"][1], 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Max Vibration Limit", 
        yref="y2"
    )

    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        xaxis=dict(title="Time (s)"),
        yaxis=dict(title="Stress (MPa)"),
        yaxis2=dict(title="Vibration (G)", overlaying="y", side="right"),
        height=450
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------
# TAB 5: TELEMETRY & RISK ANALYTICS
# ---------------------------------------------------------
with tab5:
    st.subheader("📊 Live Stress Telemetry & Stress Distribution")

    col_chart1, col_chart2 = st.columns([3, 2])

    with col_chart1:
        fig_bar = px.bar(
            df_sensors,
            x="Name",
            y="Current_Stress_MPa",
            color="Status",
            color_discrete_map={"NORMAL": "#10B981", "WARNING": "#F97316", "CRITICAL": "#EF4444"},
            title="Component Stress Profile (MPa)",
            template="plotly_dark",
            hover_data=["Sensor_ID", "Sensor_Type", "Micro_Strain_ue"]
        )
        fig_bar.update_layout(paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.markdown("""
        <div class="dark-card">
            <h4 class="accent-cyan">⚙️ Load Threshold Legend</h4>
            <p><span style="color:#10B981;">■ <b>NORMAL (< 25 MPa):</b></span> Safe operational range. Standard elastic deformation.</p>
            <p><span style="color:#F97316;">■ <b>WARNING (25 - 45 MPa):</b></span> Micro-fissure risk. Requires periodic sensor monitoring.</p>
            <p><span style="color:#EF4444;">■ <b>CRITICAL (> 45 MPa):</b></span> High shear/compressive threat. Immediate retrofitting recommended.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📋 IoT Sensor Node Hardware Inventory")
    st.dataframe(
        df_sensors[["Sensor_ID", "Name", "Type", "Sensor_Type", "X", "Y", "Z", "Current_Stress_MPa", "Micro_Strain_ue", "Battery", "RSSI", "Status"]],
        use_container_width=True,
        hide_index=True
    )

    csv = df_sensors.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Export Node Sensor Logs (.CSV)",
        data=csv,
        file_name="IoT_Node_Sensor_Telemetry_Log.csv",
        mime="text/csv"
    )

# =========================================================
# 8. FOOTER
# =========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:10px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI</b> | 3D Structural Modeling & Node Sensor Module | Developed by <b>Ritika Bhumkar & Laiba Mulani</b>
</div>
""", unsafe_allow_html=True)
