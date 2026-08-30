import altair as alt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# SAFE MODULE IMPORTS & ROBUST FALLBACK ENGINE
# =========================================================
try:
    from modules.digital_twin.engine import TwinInputs, frame_members, frame_nodes, screening_results, telemetry
    from modules.portfolio import render as portfolio
except ImportError:
    from dataclasses import dataclass

    @dataclass
    class TwinInputs:
        floors: int = 10
        bays_x: int = 4
        bays_y: int = 3
        bay_m: float = 6.0
        storey_m: float = 3.5
        concrete_mpa: float = 35.0
        column_mm: float = 600.0
        beam_mm: float = 450.0
        wind_mps: float = 15.0
        rainfall_mm_h: float = 25.0
        flood_m: float = 0.5
        live_load_kpa: float = 3.0

    def frame_members(inputs: TwinInputs):
        members = []
        # Structural Columns
        for fx in range(inputs.bays_x + 1):
            for fy in range(inputs.bays_y + 1):
                for fz in range(inputs.floors):
                    x = fx * inputs.bay_m
                    y = fy * inputs.bay_m
                    z1 = fz * inputs.storey_m
                    z2 = (fz + 1) * inputs.storey_m
                    members.append(((x, y, z1), (x, y, z2), "column"))
        # Beams along X-Axis
        for fz in range(1, inputs.floors + 1):
            for fy in range(inputs.bays_y + 1):
                for fx in range(inputs.bays_x):
                    x1 = fx * inputs.bay_m
                    x2 = (fx + 1) * inputs.bay_m
                    y = fy * inputs.bay_m
                    z = fz * inputs.storey_m
                    members.append(((x1, y, z), (x2, y, z), "beam"))
        # Beams along Y-Axis
        for fz in range(1, inputs.floors + 1):
            for fx in range(inputs.bays_x + 1):
                for fy in range(inputs.bays_y):
                    x = fx * inputs.bay_m
                    y1 = fy * inputs.bay_m
                    y2 = (fy + 1) * inputs.bay_m
                    z = fz * inputs.storey_m
                    members.append(((x1, y1, z), (x, y2, z), "beam"))
        return members

    def frame_nodes(inputs: TwinInputs):
        nodes_list = []
        for fz in range(inputs.floors + 1):
            for fx in range(inputs.bays_x + 1):
                for fy in range(inputs.bays_y + 1):
                    nodes_list.append({
                        "x": fx * inputs.bay_m,
                        "y": fy * inputs.bay_m,
                        "z": fz * inputs.storey_m
                    })
        return pd.DataFrame(nodes_list)

    def screening_results(inputs: TwinInputs):
        wind_kpa = 0.613 * (inputs.wind_mps ** 2) / 1000.0
        flood_kpa = 9.81 * inputs.flood_m
        total_height = inputs.floors * inputs.storey_m
        dead_load_kpa = (inputs.concrete_mpa / 30.0) * 4.5
        
        moment_kNm = (inputs.live_load_kpa + dead_load_kpa) * (inputs.bay_m ** 2) / 8.0
        capacity_kNm = 0.138 * inputs.concrete_mpa * (inputs.beam_mm ** 2) * 300 / 1e6
        
        utilization = min(1.2, (moment_kNm / max(1.0, capacity_kNm)) + (wind_kpa * total_height / 120.0))
        status = "Safe (IS 456 Nominal)" if utilization < 0.75 else ("Warning (Elevated Stress)" if utilization <= 0.95 else "Critical (Exceeds Capacity)")
        drift_ratio = (wind_kpa * total_height) / 450.0
        
        return {
            "utilization": utilization,
            "status": status,
            "wind_kpa": wind_kpa,
            "flood_kpa": flood_kpa,
            "moment_kNm": moment_kNm,
            "capacity_kNm": capacity_kNm,
            "drift_ratio": drift_ratio
        }

    def telemetry(periods: int = 720):
        dates = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq='h')
        np.random.seed(42)
        strain = 180 + np.sin(np.linspace(0, 10, periods)) * 50 + np.random.normal(0, 10, periods)
        tilt = 0.5 + np.cos(np.linspace(0, 5, periods)) * 0.2 + np.random.normal(0, 0.05, periods)
        wind = 12 + np.random.uniform(-5, 10, periods)
        temp = 24 + np.sin(np.linspace(0, 24, periods)) * 6 + np.random.normal(0, 1, periods)
        return pd.DataFrame({
            "time": dates,
            "strain_µε": strain,
            "tilt_mrad": tilt,
            "wind_mps": np.maximum(0, wind),
            "temperature_°C": temp
        })

    def portfolio():
        st.title("Enterprise Portfolio Overview")
        st.caption("Multi-site infrastructure health, GIS risk index, and operational monitoring.")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Monitored Assets", "14 Buildings", "+2 active sites")
        c2.metric("Portfolio Health", "94.2%", "+0.5% this week")
        c3.metric("Telemetry Nodes", "640 Sensors", "98.5% online")
        c4.metric("Active Maintenance", "03 Alerts", "-1 resolved today", delta_color="inverse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Regional Infrastructure Map")
        map_df = pd.DataFrame({
            "lat": [12.9716, 19.0760, 13.0827, 17.6599, 17.3850],
            "lon": [77.5946, 72.8777, 80.2707, 75.9064, 78.4867],
            "asset": ["CV-HQ-01 Bengaluru", "CV-BRG-04 Mumbai", "CV-WH-02 Chennai", "CV-RES-08 Solapur", "CV-DC-01 Hyderabad"],
            "score": [92, 88, 97, 99, 95]
        })
        st.map(map_df, latitude="lat", longitude="lon", size=25, color="#0284c7")

        st.subheader("Asset Health Registry")
        assets = pd.DataFrame([
            ["CV-HQ-01", "Bengaluru HQ Tower", "Commercial Skyscraper", "Karnataka", 92, "Nominal"],
            ["CV-BRG-04", "Mumbai Express Flyover", "Truss Bridge", "Maharashtra", 88, "Inspection Due"],
            ["CV-WH-02", "Chennai Logistics Hub", "Industrial Warehouse", "Tamil Nadu", 97, "Nominal"],
            ["CV-RES-08", "Solapur Residential Complex", "2 BHK Housing", "Maharashtra", 99, "Nominal"],
            ["CV-DC-01", "Hyderabad Data Center", "Critical Infrastructure", "Telangana", 95, "Nominal"]
        ], columns=["Asset Code", "Asset Name", "Typology", "Location", "Health Score", "Status"])
        
        st.dataframe(assets, hide_index=True, use_container_width=True, column_config={
            "Health Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d%%")
        })

st.set_page_config(page_title="ConstructVision | Digital Twin Engine", page_icon="🏗️", layout="wide")

st.session_state.setdefault("twin", TwinInputs())

with st.sidebar:
    st.title("ConstructVision")
    st.caption("Built environment intelligence & structural twin platform")
    
    view = st.radio(
        "Workspace Navigation", 
        ["Portfolio", "Command center", "Twin studio", "Capture & reconstruction", "Asset health", "IoT Telemetry & CCTV", "Integration"], 
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("🟢 **LIVE TELEMETRY** — CV-HQ-01 · Bengaluru")
    st.caption("Digital Twin Platform · v2.5 Ultimate")

def make_frame(inputs: TwinInputs, show_wind: bool = False, color_by_stress: bool = False):
    figure = go.Figure()
    res = screening_results(inputs)
    util = res["utilization"]
    
    # Stress-based color coding
    if color_by_stress:
        beam_color = "#34d399" if util < 0.75 else ("#f59e0b" if util <= 0.95 else "#ef4444")
        col_color = "#38bdf8" if util < 0.75 else ("#fbbf24" if util <= 0.95 else "#f87171")
    else:
        beam_color = "#42C9D9"
        col_color = "#91E6DF"

    for start, end, kind in frame_members(inputs):
        figure.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]], 
                y=[start[1], end[1]], 
                z=[start[2], end[2]], 
                mode="lines", 
                line=dict(color=col_color if kind == "column" else beam_color, width=6 if kind == "column" else 4), 
                hoverinfo="skip", 
                showlegend=False
            )
        )
    
    nodes = frame_nodes(inputs)
    figure.add_trace(
        go.Scatter3d(
            x=nodes.x, 
            y=nodes.y, 
            z=nodes.z, 
            mode="markers", 
            marker=dict(size=3, color="#F7B955"), 
            name="Sensor-ready nodes", 
            hovertemplate="Node X: %{x:.1f} m<br>Node Y: %{y:.1f} m<br>Node Z: %{z:.1f} m<extra></extra>"
        )
    )
    
    if show_wind and inputs.wind_mps > 0:
        z_coords = list(range(2, int(inputs.floors * inputs.storey_m), max(1, int(inputs.storey_m))))
        figure.add_trace(
            go.Cone(
                x=[-3] * len(z_coords), 
                y=[inputs.bays_y * inputs.bay_m / 2] * len(z_coords), 
                z=z_coords, 
                u=[inputs.wind_mps / 4] * len(z_coords), 
                v=[0] * len(z_coords), 
                w=[0] * len(z_coords), 
                colorscale=[[0, "#38bdf8"], [1, "#0284c7"]], 
                showscale=False, 
                sizemode="absolute", 
                sizeref=0.8, 
                name="Lateral Wind Load Vectors"
            )
        )
        
    figure.update_layout(
        height=580, 
        margin=dict(l=0, r=0, t=0, b=0), 
        paper_bgcolor="#07131F", 
        plot_bgcolor="#07131F", 
        scene=dict(
            bgcolor="#07131F", 
            xaxis=dict(visible=False), 
            yaxis=dict(visible=False), 
            zaxis=dict(visible=False), 
            aspectmode="data", 
            camera=dict(eye=dict(x=1.6, y=1.7, z=1.05))
        ), 
        legend=dict(font=dict(color="#EDF7FA"))
    )
    return figure

def hero():
    st.title("A Living Operational Model of Your Built Asset")
    st.caption("3D parametric BIM frame, real-time IoT strain monitoring, and operational hazard scenario testing—unified in one operational twin.")
    
    data = telemetry()
    current = data.iloc[-1]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Structural Health Index", "92.4 / 100", "+0.7 this week")
    c2.metric("Telemetry Channels", "48 / 52", "4 commissioning")
    c3.metric("Active Anomaly Alerts", "02", "1 needs review", delta_color="inverse")
    c4.metric("Gateway Ingest Rate", "18 ms", "MQTT over TLS")
        
    left, right = st.columns([1.5, 1])
    with left:
        with st.container(border=True):
            st.subheader("Instrumented Asset Digital Twin", help="Editable parametric 3D structural frame with real-time sensor node overlays.")
            st.plotly_chart(make_frame(st.session_state.twin, show_wind=True, color_by_stress=True), use_container_width=True, config={"displaylogo": False})
            
    with right:
        with st.container(border=True):
            st.subheader("Priority Field Signals")
            st.warning("Column C-2 / Level 01 — Microstrain trend above baseline (+12%)", icon="📈")
            st.info("Rainfall threshold approaching foundation sump drain (25 mm/h)", icon="💧")
            st.success("North Elevation CCTV Visual Inspection camera feed synchronized", icon="✅")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Today's Environmental Context")
            mc1, mc2 = st.columns(2)
            mc1.metric("Wind Speed", f"{current['wind_mps']:.1f} m/s")
            mc2.metric("Ambient Temp", f"{current['temperature_°C']:.1f} °C")
            
            st.caption("Site Location: Bengaluru Tech Park · Coordinates: 12.9716° N, 77.5946° E")

def studio():
    st.title("Twin Studio & FEA Load Screener")
    st.caption("Parametrically modify structural frame dimensions, materials, and extreme environmental hazard loads. Runs preliminary IS 456 / Eurocode structural safety screening.")
    
    with st.form("geometry"):
        st.markdown("##### **1. Architectural Geometry & Material Properties**")
        a, b, c = st.columns(3)
        floors = a.number_input("Storeys (Floors)", 1, 60, st.session_state.twin.floors)
        bays_x = b.number_input("X-Axis Bays", 1, 20, st.session_state.twin.bays_x)
        bays_y = c.number_input("Y-Axis Bays", 1, 20, st.session_state.twin.bays_y)
        
        bay_m = a.number_input("Bay Span Length (m)", 3.0, 15.0, st.session_state.twin.bay_m, 0.5)
        storey_m = b.number_input("Storey Height (m)", 2.4, 8.0, st.session_state.twin.storey_m, 0.1)
        concrete = c.number_input("Concrete Strength f'c (MPa)", 15.0, 100.0, st.session_state.twin.concrete_mpa, 5.0)
        
        col_mm = a.number_input("Column Section Width (mm)", 300.0, 1200.0, st.session_state.twin.column_mm, 50.0)
        beam_mm = b.number_input("Beam Section Depth (mm)", 250.0, 1000.0, st.session_state.twin.beam_mm, 50.0)
        
        updated = st.form_submit_button("Rebuild 3D BIM Frame", type="primary", icon="🏗️")
        
    if updated:
        old = st.session_state.twin
        st.session_state.twin = TwinInputs(
            int(floors), int(bays_x), int(bays_y), bay_m, storey_m, concrete, col_mm, beam_mm, 
            old.wind_mps, old.rainfall_mm_h, old.flood_m, old.live_load_kpa
        )
        st.toast("Structural frame geometry updated successfully!")
        
    twin = st.session_state.twin
    control, model = st.columns([0.85, 1.55])
    
    with control:
        with st.container(border=True):
            st.markdown("##### **2. Hazard & Load Scenario Inputs**")
            wind = st.slider("Lateral Wind Velocity (m/s)", 0, 80, int(twin.wind_mps))
            rain = st.slider("Rainfall Intensity (mm/h)", 0, 250, int(twin.rainfall_mm_h))
            flood = st.slider("Submergence Flood Depth (m)", 0.0, 5.0, twin.flood_m, 0.1)
            live = st.slider("Occupancy Live Load (kPa)", 1.0, 12.0, twin.live_load_kpa, 0.25)
            
            scenario = TwinInputs(
                twin.floors, twin.bays_x, twin.bays_y, twin.bay_m, twin.storey_m, 
                twin.concrete_mpa, twin.column_mm, twin.beam_mm, wind, rain, flood, live
            )
            result = screening_results(scenario)
            
            st.divider()
            st.markdown("##### **3. Preliminary Screening Results**")
            st.metric("Peak Structural Utilization", f"{result['utilization']:.1%}", result["status"])
            st.metric("Wind Drag Pressure", f"{result['wind_kpa']:.2f} kPa")
            st.metric("Hydrostatic Base Uplift Pressure", f"{result['flood_kpa']:.1f} kPa")
            st.metric("Design Bending Moment Demand", f"{result['moment_kNm']:.1f} kNm")
            
            # Export CSV Report
            report_df = pd.DataFrame([{
                "Floors": twin.floors, "Total_Height_m": twin.floors * twin.storey_m,
                "Concrete_MPa": twin.concrete_mpa, "Wind_Speed_m_s": wind,
                "Peak_Utilization": f"{result['utilization']:.1%}", "Status": result["status"]
            }])
            st.download_button(
                "📥 Export Screening Audit Report (CSV)", 
                data=report_df.to_csv(index=False), 
                file_name=f"BIM_Screening_Report_{twin.floors}F.csv", 
                mime="text/csv"
            )
            
    with model:
        st.plotly_chart(make_frame(scenario, show_wind=True, color_by_stress=True), use_container_width=True, config={"displaylogo": False})
        
    st.warning(
        "Screening analysis only: Evaluates gravity loads, simple beam bending, dynamic wind drag, and hydrostatic pressure. "
        "Project-grade decisions require full 3D Finite Element Analysis (FEA) execution via the Integration Layer.", 
        icon="⚠️"
    )

def capture():
    st.title("Capture & Photogrammetry Mesh Reconstruction")
    st.caption("Transform drone imagery and multi-view site photo sets into a scaled point cloud / 3D mesh registered against the structural model.")
    
    uploads = st.file_uploader("Upload Overlapping Site Images (JPG, PNG, TIFF)", type=["jpg", "jpeg", "png", "tif"], accept_multiple_files=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Uploaded Imagery Files", len(uploads or []))
    c2.metric("Minimum Target Images", "60 Images")
    c3.metric("Required Overlap Ratio", "≥ 70% Overlap")
    
    with st.expander("Photogrammetry Reconstruction Pipeline Workflow", expanded=True):
        st.markdown(
            "1. **EXIF Inspection & Camera Calibration**: Validates focal length, aperture, sensor size, and GPS coordinates.\n"
            "2. **Feature Extraction & Sparse Cloud Generation**: Extracts SIFT features and computes camera projection matrices.\n"
            "3. **Dense Point Cloud / Mesh Surface Generation**: Executes multi-view stereo (MVS) depth estimation.\n"
            "4. **Georeferencing & Scale Control**: Aligns GCP ground control points to real-world coordinates.\n"
            "5. **BIM Structural Alignment**: Registers reconstructed mesh against the parametric 3D frame."
        )
        
    if uploads and st.button("Start Mesh Reconstruction Job", type="primary", icon="▶️"):
        st.progress(85, text="Processing sparse feature matching & depth maps via GPU worker...")
        st.toast("Reconstruction package staged. Connected to High-Performance GPU compute worker.")
        
    st.info(
        "For decision-grade 3D twins, ensure full 360° orbital camera coverage with constant lighting. "
        "A minimum of 60 calibrated photos is recommended for sub-centimeter geometric accuracy.", 
        icon="📷"
    )

def health():
    st.title("Asset Structural Health Monitoring (SHM)")
    st.caption("Long-term time-series analysis for strain gauges, tiltmeters, accelerometers, and environmental sensors.")
    
    data = telemetry(24 * 30)
    
    window_choice = st.radio("Time-Series Window", ["24 hours", "7 days", "30 days"], horizontal=True)
    size = {"24 hours": 24, "7 days": 168, "30 days": 720}[window_choice]
    frame = data.tail(size)
    
    # Altair Dynamic Time-Series Plot
    st.markdown("##### **Multi-Channel Telemetry Signals**")
    chart = alt.Chart(frame).transform_fold(
        ["strain_µε", "tilt_mrad"], as_=["signal", "value"]
    ).mark_line(size=2).encode(
        x=alt.X("time:T", title="Timestamp"), 
        y=alt.Y("value:Q", title="Sensor Output Signal"), 
        color=alt.Color("signal:N", title="Sensor Channel", scale=alt.Scale(range=['#38bdf8', '#f59e0b'])), 
        tooltip=["time:T", "signal:N", "value:Q"]
    ).properties(height=360).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Spectral Power Density Chart (Frequency Analysis)
    st.markdown("##### **Vibration Spectral Power Density (g²/Hz)**")
    fft_freqs = np.linspace(0, 50, 100)
    fft_power = np.exp(-0.1 * (fft_freqs - 12)**2) + 0.1 * np.random.normal(0, 0.2, 100)
    fft_df = pd.DataFrame({"Frequency_Hz": fft_freqs, "Power_g2_Hz": np.maximum(0, fft_power)})
    
    fft_chart = alt.Chart(fft_df).mark_area(
        line={'color': '#34d399'}, 
        color=alt.Gradient(gradient='linear', stops=[alt.GradientStop(color='#34d399', offset=0), alt.GradientStop(color='transparent', offset=1)], x1=1, x2=1, y1=1, y2=0)
    ).encode(
        x=alt.X("Frequency_Hz:Q", title="Frequency (Hz)"),
        y=alt.Y("Power_g2_Hz:Q", title="Spectral Power Density (g²/Hz)")
    ).properties(height=220)
    
    st.altair_chart(fft_chart, use_container_width=True)
    
    st.subheader("Sensor Channel Inventory")
    inventory = pd.DataFrame([
        ["STR-C2-01", "Level 01 Column C-2", "Microstrain Gauge", "Online", 87, "180 µε"],
        ["TILT-RF-03", "Roof Framing Span", "MEMS Tiltmeter", "Online", 91, "0.52 mrad"],
        ["WL-BASE-01", "Foundation Sump Drain", "Submersible Hydrostatic", "Attention", 64, "0.45 m"],
        ["ACC-C3-02", "Level 03 Slab Edge", "3-Axis Accelerometer", "Online", 95, "0.018 g"]
    ], columns=["Channel Tag", "Location", "Sensor Type", "Status", "Data Quality Score", "Current Reading"])
    
    st.dataframe(
        inventory, 
        hide_index=True, 
        use_container_width=True, 
        column_config={"Data Quality Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d%%")}
    )

def iot_telemetry():
    st.title("Live IoT Telemetry & CCTV AI Monitor")
    st.caption("Real-time sensor node telemetry paired with computer vision surface inspection feeds.")
    
    col_cctv, col_telemetry = st.columns([1.25, 1])

    # Left Column: CCTV Live Camera Feed & AI Defect Overlay
    with col_cctv:
        with st.container(border=True):
            st.subheader("📹 CCTV Visual Inspection Feed")
            st.caption("Camera Zone: Level 01 Ground Columns (SNS-COL-03)")
            
            cam_source = st.radio("Camera Source:", ["Live WebCam / Mobile Camera", "Site RTSP/CCTV Stream"], horizontal=True)
            
            if cam_source == "Live WebCam / Mobile Camera":
                st.camera_input("Capture Visual Inspection Snapshot")
            else:
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                
            st.info("AI Inspection Overlay: 0 Defects Detected on Surface · Crack Width < 0.1 mm (Safe)", icon="ℹ️")

    # Right Column: Live IoT Telemetry & Trend Chart
    with col_telemetry:
        with st.container(border=True):
            st.markdown("### 📍 Sensor Telemetry")
            st.markdown("#### **Channel: SNS-COL-03 (Strain Gauge)**")
            st.error("Warning: High Strain Surge Recorded", icon="⚠️")
            
            st.metric("Current Microstrain", "977.96 µε", delta="+14.2 µε vs baseline")
            
            # Live Plotly Strain Trend
            times = pd.date_range(end=pd.Timestamp.now(), periods=15, freq='3s').strftime('%H:%M:%S')
            strain_values = np.array([880, 910, 890, 1020, 800, 990, 720, 980, 870, 820, 1030, 780, 850, 1010, 977.96])
            
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=times, 
                    y=strain_values, 
                    mode='lines+markers', 
                    line=dict(color='#F97316', width=2), 
                    marker=dict(size=6)
                )
            )
            fig.update_layout(
                title="Live Strain Trend — Ground Column C3", 
                template="plotly_dark", 
                height=260, 
                margin=dict(l=10, r=10, t=35, b=10), 
                yaxis=dict(title="Microstrain (µε)")
            )
            st.plotly_chart(fig, use_container_width=True)

            # Download CSV Button
            csv_data = pd.DataFrame({"Timestamp": times, "Sensor_Tag": "SNS-COL-03", "Strain_µε": strain_values}).to_csv(index=False)
            st.download_button(
                label="📥 Download SNS-COL-03 Telemetry Log (CSV)", 
                data=csv_data, 
                file_name="SNS-COL-03_Telemetry_Log.csv", 
                mime="text/csv", 
                type="primary"
            )

def integration():
    st.title("Deployment & Structural Solver Integrations")
    st.caption("Configure IoT MQTT broker endpoints, REST APIs, and external FEA/CFD HPC solver compute queues.")
    
    with st.container(border=True):
        st.subheader("Field Data Ingestion Terminal")
        st.code(
            "mqtts://gateway.constructvision.ai/site/CV-HQ-01/telemetry\n"
            "POST /api/v1/telemetry  {\n"
            "  \"timestamp\": \"2026-08-25T01:30:00Z\",\n"
            "  \"sensor_id\": \"STR-C2-01\",\n"
            "  \"value\": 977.96,\n"
            "  \"unit\": \"µε\",\n"
            "  \"quality\": \"VALIDATED\"\n"
            "}", 
            language="json"
        )
        st.caption("Recommended Configuration: MQTT over TLS v1.3 with X.509 client certificate authentication.")
        
    a, b = st.columns(2)
    with a:
        with st.container(border=True):
            st.subheader("Structural FEA Solver Queue")
            st.write("OpenSees / CalculiX HPC Worker")
            st.caption("🟢 Connected & Ready")
            st.button("Test OpenSees Endpoint", icon="⚙️")
            
    with b:
        with st.container(border=True):
            st.subheader("Environmental CFD Solver Queue")
            st.write("OpenFOAM / CFD Wind Tunnel Worker")
            st.caption("🟠 Standby Queue")
            st.button("Configure CFD Boundary Endpoint", icon="💨")
            
    st.info(
        "Animated vector arrows communicate wind direction in Twin Studio. "
        "High-fidelity turbulence, vortex shedding, and pressure distribution require a CFD mesh solver job.", 
        icon="💨"
    )

workspace_router = {
    "Portfolio": portfolio, 
    "Command center": hero, 
    "Twin studio": studio, 
    "Capture & reconstruction": capture, 
    "Asset health": health, 
    "IoT Telemetry & CCTV": iot_telemetry, 
    "Integration": integration
}

workspace_router[view]()
