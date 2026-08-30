from datetime import datetime, timedelta
import json
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Live IoT & Wireless Sensor Telemetry Hub | CONSTRUCTVISION AI",
    page_icon="📡",
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
    .badge-warning { background: rgba(249, 115, 22, 0.25); color: #FDBA74; border: 1px solid #F97316; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
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

gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road",
    "type": "Commercial High-Rise",
    "risk_score": 88
})

inspection_data = st.session_state.get("latest_inspection", None)

if "sensor_history" not in st.session_state:
    st.session_state.sensor_history = {}

if "trigger_stress_surge" not in st.session_state:
    st.session_state.trigger_stress_surge = False

FULL_SENSOR_NETWORK = [
    {
        "id": "SNS-FND-01",
        "component": "Foundation Footing (F-01)",
        "type": "MEMS Settlement Tiltmeter",
        "location": "Plinth Base Grid A1",
        "value": 0.04,
        "unit": "deg",
        "threshold": 0.25,
        "status": "Normal",
        "protocol": "LoRaWAN 868MHz"
    },
    {
        "id": "SNS-COL-12",
        "component": "RCC Column C-12",
        "type": "Vibrating Wire Strain Gauge",
        "location": "Level 01 Shear Zone",
        "value": 284.5 if (inspection_data and inspection_data.get("max_crack_width_mm", 0) > 0.3) else 184.2,
        "unit": "µε",
        "threshold": 250.0,
        "status": "Warning" if (inspection_data and inspection_data.get("max_crack_width_mm", 0) > 0.3) else "Normal",
        "protocol": "MQTT / TLS v1.3"
    },
    {
        "id": "SNS-BEAM-04",
        "component": "Flexural Beam B-04",
        "type": "Optical Fiber FBG Strain",
        "location": "Level 03 Mid-Span",
        "value": 142.8,
        "unit": "µε",
        "threshold": 200.0,
        "status": "Normal",
        "protocol": "MQTT / TLS v1.3"
    },
    {
        "id": "SNS-SLAB-09",
        "component": "Floor Slab S-09",
        "type": "3-Axis MEMS Accelerometer",
        "location": "Deck Soffit Center",
        "value": 0.018,
        "unit": "g",
        "threshold": 0.050,
        "status": "Normal",
        "protocol": "ZigBee Mesh"
    },
    {
        "id": "SNS-WALL-02",
        "component": "Masonry Wall W-02",
        "type": "Displacement Tell-Tale Sensor",
        "location": "East Face Joint",
        "value": 0.22,
        "unit": "mm",
        "threshold": 0.50,
        "status": "Normal",
        "protocol": "LoRaWAN 868MHz"
    },
    {
        "id": "SNS-SUMP-01",
        "component": "Foundation Sump Drain",
        "type": "Submersible Hydrostatic Pressure",
        "location": "Basement Sump Well",
        "value": 0.45,
        "unit": "m",
        "threshold": 0.80,
        "status": "Normal",
        "protocol": "RS-485 Modbus"
    }
]

with st.sidebar:
    st.markdown("### ⚙️ **IoT Telemetry Controls**")
    st.caption("Hardware Nodes & Communication Protocol Settings")
    st.divider()

    live_stream_active = st.checkbox("⚡ Enable Real-time Data Streaming", value=True)
    refresh_rate_sec = st.slider("Stream Update Interval (sec):", min_value=1, max_value=10, value=2, step=1)

    st.divider()
    st.markdown("#### 🚨 Simulation & Stress Testing")
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        if st.button("⚡ Inject Surge", use_container_width=True):
            st.session_state.trigger_stress_surge = True
            st.toast("⚠️ Temporary Load & Microstrain Surge Injected!")
    with col_sim2:
        if st.button("🟢 Normal", use_container_width=True):
            st.session_state.trigger_stress_surge = False
            st.toast("✅ Baseline Telemetry Restored.")

    st.divider()
    st.markdown("#### 🌐 Network Protocol Bridge")
    st.caption("• **Broker:** `mqtts://gateway.constructvision.ai`")
    st.caption("• **Security:** TLS v1.3 / X.509 Client Certs")
    st.caption("• **Ingest Latency:** 14 ms")

    st.caption("Department of Civil Engineering © 2026")

st.title("📡 Live IoT Telemetry & Wireless Sensor Hub")
st.caption("Real-time wireless strain gauge monitoring, MEMS tiltmeter tracking, accelerometers, and IS 456 threshold telemetry.")

# Synchronized Site Location Bar
st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-blue">📍 LIVE SYNC TARGET SITE</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">{gps_info.get('site_code', 'CV-SITE')}: {gps_info.get('label', 'Solapur Field Site')}</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>GPS Coordinates:</b> <span style="color:#38BDF8;">{gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E</span> | 
            <b>Online IoT Nodes:</b> <span class="accent-green">{len(FULL_SENSOR_NETWORK)} Channels Active</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

active_warnings = sum(1 for s in FULL_SENSOR_NETWORK if s["status"] in ["Warning", "Critical"])
status_badge_cls = "badge-success" if active_warnings == 0 else ("badge-warning" if active_warnings == 1 else "badge-critical")
status_text = "ALL NODES NOMINAL" if active_warnings == 0 else f"{active_warnings} THRESHOLD ALERTS"

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Network Health</span>
        <h3 style="margin:4px 0 0 0;"><span class="{status_badge_cls}">{status_text}</span></h3>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    peak_col = next((s for s in FULL_SENSOR_NETWORK if "COL" in s["id"]), FULL_SENSOR_NETWORK[1])
    current_strain_val = peak_col["value"] + (85.0 if st.session_state.trigger_stress_surge else 0.0)
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Column C-12 Microstrain</span>
        <h2 class="accent-cyan" style="margin:4px 0 0 0;">{current_strain_val:.1f} µε</h2>
        <span style="font-size:11px; color:#94A3B8;">Limit: {peak_col['threshold']} µε</span>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    tilt_col = next((s for s in FULL_SENSOR_NETWORK if "FND" in s["id"]), FULL_SENSOR_NETWORK[0])
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Plinth Base Tilt</span>
        <h2 class="accent-orange" style="margin:4px 0 0 0;">{tilt_col['value']:.2f}°</h2>
        <span style="font-size:11px; color:#94A3B8;">Limit: {tilt_col['threshold']}°</span>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    vibe_col = next((s for s in FULL_SENSOR_NETWORK if "SLAB" in s["id"]), FULL_SENSOR_NETWORK[3])
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Peak Acceleration</span>
        <h2 class="accent-green" style="margin:4px 0 0 0;">{vibe_col['value']:.3f} g</h2>
        <span style="font-size:11px; color:#94A3B8;">Limit: {vibe_col['threshold']} g</span>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Data Packet Rate</span>
        <h2 style="margin:4px 0 0 0; color:#FFFFFF;">120 Pkts/m</h2>
        <span style="font-size:11px; color:#10B981;">0.00% Packet Loss</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("### 🧱 Filter Telemetry by Structural Element & Node")

component_options = list(dict.fromkeys(s["component"] for s in FULL_SENSOR_NETWORK))
col_filter1, col_filter2 = st.columns([2, 1])

with col_filter1:
    selected_comp = st.selectbox(
        "🔗 Choose Structural Component / 3D BIM Element:",
        options=component_options,
        index=1 if len(component_options) > 1 else 0
    )

with col_filter2:
    st.markdown("**Quick Sync with 3D Twin**")
    if st.button("🏗️ Highlight Node in 3D Building Twin", use_container_width=True):
        st.toast(f"Syncing sensor coordinates for '{selected_comp}' to 7_🏗️_3D_Building.py...")

filtered_sensors = [s for s in FULL_SENSOR_NETWORK if s["component"] == selected_comp]

if not filtered_sensors:
    filtered_sensors = [FULL_SENSOR_NETWORK[1]]

for s in filtered_sensors:
    sensor_id = s["id"]
    base_val = s["value"]
    unit = s["unit"]
    threshold = s["threshold"]

    # Inject temporary surge if trigger active
    if st.session_state.trigger_stress_surge:
        base_val *= 1.45

    # Determine dynamic status based on threshold
    if base_val >= threshold * 1.15:
        node_status = "Critical"
        status_cls = "badge-critical"
    elif base_val >= threshold:
        node_status = "Warning"
        status_cls = "badge-warning"
    else:
        node_status = "Normal"
        status_cls = "badge-success"

    # Initialize time-series sensor history in session state
    if sensor_id not in st.session_state.sensor_history:
        np.random.seed(hash(sensor_id) % (2**32))
        now_time = datetime.now()
        times = [(now_time - timedelta(seconds=i * 2)).strftime("%H:%M:%S") for i in range(30, 0, -1)]
        
        noise_scale = base_val * 0.05 if node_status == "Normal" else base_val * 0.12
        readings = np.random.normal(loc=base_val, scale=noise_scale, size=30).tolist()
        readings = [max(0.001, r) for r in readings]
        
        st.session_state.sensor_history[sensor_id] = {
            "Time": times,
            "Reading": readings
        }

    history = st.session_state.sensor_history[sensor_id]
    curr_time_str = datetime.now().strftime("%H:%M:%S")

    # Append live data point if timestamp changed
    if history["Time"][-1] != curr_time_str:
        history["Time"].append(curr_time_str)
        last_val = history["Reading"][-1]
        next_val = max(0.001, np.random.normal(loc=(base_val * 0.7 + last_val * 0.3), scale=base_val * 0.04))
        history["Reading"].append(next_val)
        
        if len(history["Time"]) > 30:
            history["Time"].pop(0)
            history["Reading"].pop(0)

    df_sensor = pd.DataFrame(history)
    current_reading = round(history["Reading"][-1], 3)

    c_card1, c_card2 = st.columns(2)

    with c_card1:
        st.markdown(f"""
        <div class="dark-card">
            <span style="font-size:11px; color:#94A3B8; font-weight:bold; letter-spacing:1px;">HARDWARE NODE ID</span>
            <h3 class="accent-cyan" style="margin:4px 0 10px 0;">📡 {sensor_id}</h3>
            <p style="margin:2px 0;"><b>Component Element:</b> {s['component']}</p>
            <p style="margin:2px 0;"><b>Measurement Type:</b> {s['type']}</p>
            <p style="margin:2px 0;"><b>Physical Location:</b> {s['location']}</p>
            <p style="margin:2px 0;"><b>Protocol:</b> <span class="badge-blue">{s['protocol']}</span></p>
        </div>
        """, unsafe_allow_html=True)

    with c_card2:
        st.markdown(f"""
        <div class="dark-card">
            <span style="font-size:11px; color:#94A3B8; font-weight:bold; letter-spacing:1px;">REAL-TIME SIGNAL READING</span>
            <h1 style="margin:4px 0 10px 0; font-size:36px;" class="{"accent-red" if node_status=="Critical" else ("accent-orange" if node_status=="Warning" else "accent-green")}">
                {current_reading} <span style="font-size:18px; color:#CBD5E1;">{unit}</span>
            </h1>
            <p style="margin:0 0 6px 0;"><b>Governing Code Limit:</b> {threshold} {unit}</p>
            <span class="{status_cls}">● STATUS: {node_status.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    # Line Chart of Time-Series Reading
    fig_line = px.line(
        df_sensor,
        x="Time",
        y="Reading",
        title=f"Real-Time Time-Series Stream: {s['type']} ({sensor_id})",
        markers=True
    )

    line_color = "#10B981" if node_status == "Normal" else ("#F97316" if node_status == "Warning" else "#EF4444")
    
    fig_line.update_traces(line_color=line_color, marker=dict(size=5))
    fig_line.add_hline(y=threshold, line_dash="dash", line_color="#EF4444", annotation_text=f"Code Safety Limit ({threshold} {unit})")
    
    fig_line.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=35, b=10),
        height=260,
        xaxis=dict(showgrid=False, title=dict(text="Stream Timestamp (HH:MM:SS)"), tickangle=-45),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title=dict(text=f"Signal Magnitude ({unit})"))
    )

    st.plotly_chart(fig_line, use_container_width=True, key=f"chart_{sensor_id}")

    st.markdown("#### 💻 Live MQTT / WebSocket Payload Stream")
    
    payload_sample = {
        "timestamp": datetime.now().isoformat(),
        "gateway_id": "GW-SOLAPUR-HQ-01",
        "sensor_id": sensor_id,
        "site_code": gps_info.get("site_code", "CV-SITE"),
        "component": s["component"],
        "metric": s["type"],
        "value": current_reading,
        "unit": unit,
        "threshold_limit": threshold,
        "status": node_status,
        "quality": "VALIDATED_100%"
    }

    st.code(json.dumps(payload_sample, indent=2), language="json")

    st.markdown("#### 📥 Export Wireless Sensor Telemetry Data")

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        csv_data = df_sensor.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"💾 Download {sensor_id} CSV Log (.CSV)",
            data=csv_data,
            file_name=f"Telemetry_{sensor_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"btn_csv_{sensor_id}"
        )

    with col_exp2:
        st.download_button(
            label=f"🌐 Download {sensor_id} JSON Audit Payload (.JSON)",
            data=json.dumps(payload_sample, indent=2),
            file_name=f"Telemetry_{sensor_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
            key=f"btn_json_{sensor_id}"
        )

if live_stream_active:
    time.sleep(refresh_rate_sec)
    st.rerun()

st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI IOT TELEMETRY HUB</b> | Wireless Structural Health Monitoring Engine<br>
    Developed by <b>Ritika Bhumkar</b> & <b>Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
