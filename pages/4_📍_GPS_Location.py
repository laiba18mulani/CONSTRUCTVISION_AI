from datetime import datetime
import json
import folium
from folium.plugins import HeatMap, MarkerCluster, MiniMap, MeasureControl
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

# =========================================================
# 1. PAGE CONFIGURATION & DARK GLASS THEME
# =========================================================
st.set_page_config(
    page_title="GPS Site Operations & GIS Hub | CONSTRUCTVISION AI",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Glass UI CSS
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

# =========================================================
# 2. SOLAPUR & REGIONAL GEOSPATIAL REGISTRY DATABASE
# =========================================================
SOLAPUR_LOCATIONS = {
    "CV-RES-01: Navi Peth Commercial Center": {
        "lat": 17.6599, "lon": 75.9064, "road": "Rupa Bhavani Road", "type": "Commercial High-Rise",
        "risk_score": 88, "critical_defects": 3, "sensors_online": 12, "drone_zone_m": 350
    },
    "CV-INST-02: Sangameshwar Campus Tower": {
        "lat": 17.6585, "lon": 75.9045, "road": "VIP Road", "type": "Institutional Facility",
        "risk_score": 94, "critical_defects": 1, "sensors_online": 8, "drone_zone_m": 250
    },
    "CV-FLY-03: Saat Rasta Traffic Flyover": {
        "lat": 17.6650, "lon": 75.9090, "road": "Saat Rasta Circle", "type": "Bridge & Infrastructure",
        "risk_score": 72, "critical_defects": 7, "sensors_online": 18, "drone_zone_m": 500
    },
    "CV-RES-04: Hotgi Road Residential Estate": {
        "lat": 17.6420, "lon": 75.9220, "road": "Hotgi Road Expressway", "type": "Residential Complex",
        "risk_score": 98, "critical_defects": 0, "sensors_online": 15, "drone_zone_m": 300
    },
    "CV-IND-05: MIDC Chemical & Logistics Hub": {
        "lat": 17.6810, "lon": 75.9350, "road": "MIDC Central Avenue", "type": "Industrial Warehouse",
        "risk_score": 81, "critical_defects": 4, "sensors_online": 24, "drone_zone_m": 600
    },
    "CV-RAIL-06: Solapur Central Railway Terminal": {
        "lat": 17.6688, "lon": 75.9030, "road": "Station Terminal Approach", "type": "Transit Infrastructure",
        "risk_score": 85, "critical_defects": 2, "sensors_online": 16, "drone_zone_m": 450
    }
}

# Cross-page session state synchronization
if "active_site_name" not in st.session_state:
    st.session_state["active_site_name"] = "CV-RES-01: Navi Peth Commercial Center"

if "selected_location_info" not in st.session_state:
    default_data = SOLAPUR_LOCATIONS["CV-RES-01: Navi Peth Commercial Center"]
    st.session_state["selected_location_info"] = {
        "site_code": "CV-RES-01",
        "label": "Navi Peth Commercial Center",
        "lat": default_data["lat"],
        "lon": default_data["lon"],
        "road": default_data["road"],
        "type": default_data["type"],
        "risk_score": default_data["risk_score"],
        "critical_defects": default_data["critical_defects"],
        "sensors_online": default_data["sensors_online"],
        "drone_zone_m": default_data["drone_zone_m"]
    }

# =========================================================
# 3. SIDEBAR CONTROLS & CROSS-PAGE WORKFLOW BRIDGE
# =========================================================
with st.sidebar:
    st.markdown("### 📍 **CONSTRUCTVISION GIS**")
    st.caption("v2.6 GIS Spatial Command & Drone Hub")
    st.divider()

    st.markdown("#### 🗺️ GIS Layer & Overlay Controls")
    tile_provider = st.selectbox(
        "Base Map Style:",
        ["Dark Matter (CartoDB)", "OpenStreetMap Standard", "Satellite Aerial (Esri)", "Terrain Topography"],
        index=0
    )

    show_drone_zone = st.checkbox("Show Drone Geofence Radius Circle", value=True)
    show_defect_heatmap = st.checkbox("Show Structural Risk Heatmap", value=True)
    show_sensor_nodes = st.checkbox("Show Live IoT Telemetry Pins", value=True)

    st.divider()
    st.markdown("#### 🔗 Cross-Page Module Sync")
    st.success(f"Active Sync Site: **{st.session_state['selected_location_info']['site_code']}**")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📷 AI Inspection", use_container_width=True):
            st.toast("Syncing coordinates to 5_🔬_AI_Inspection.py...")
    with col_btn2:
        if st.button("🏗️ 3D Digital Twin", use_container_width=True):
            st.toast("Syncing coordinates to 7_🏗️_3D_Building.py...")

    st.caption("Department of Civil Engineering © 2026")

# =========================================================
# 4. MAIN DASHBOARD HEADER & SITE SELECTOR
# =========================================================
st.title("📍 GPS Geographical Location & Drone Flight GIS")
st.caption("Real-time site spatial intelligence, drone audit flight perimeters, and cross-module structural state synchronization.")

col_sel, col_custom, col_kpi = st.columns([2.2, 1.2, 1.6])

with col_sel:
    selected_site_key = st.selectbox(
        "📍 Choose Active Construction / Infrastructure Site:",
        options=list(SOLAPUR_LOCATIONS.keys()),
        index=list(SOLAPUR_LOCATIONS.keys()).index(st.session_state["active_site_name"]) if st.session_state["active_site_name"] in SOLAPUR_LOCATIONS else 0
    )

    # Update session state on dropdown selection
    loc_info = SOLAPUR_LOCATIONS[selected_site_key]
    st.session_state["active_site_name"] = selected_site_key
    st.session_state["selected_location_info"] = {
        "site_code": selected_site_key.split(":")[0],
        "label": selected_site_key.split(":")[1].strip(),
        "lat": loc_info["lat"],
        "lon": loc_info["lon"],
        "road": loc_info["road"],
        "type": loc_info["type"],
        "risk_score": loc_info["risk_score"],
        "critical_defects": loc_info["critical_defects"],
        "sensors_online": loc_info["sensors_online"],
        "drone_zone_m": loc_info["drone_zone_m"]
    }

current_target = st.session_state["selected_location_info"]

with col_custom:
    st.markdown("**Custom Coordinate Entry**")
    with st.popover("➕ Add Custom Lat/Lon"):
        c_lat = st.number_input("Custom Latitude (°N):", min_value=8.0, max_value=37.0, value=current_target["lat"], format="%.4f")
        c_lon = st.number_input("Custom Longitude (°E):", min_value=68.0, max_value=97.0, value=current_target["lon"], format="%.4f")
        c_label = st.text_input("Site Identifier Tag:", "Custom Field Site X")
        if st.button("Set Active Custom Location", type="primary"):
            st.session_state["selected_location_info"] = {
                "site_code": "CV-CUST-99",
                "label": c_label,
                "lat": c_lat,
                "lon": c_lon,
                "road": "Field Inspection Road",
                "type": "Custom Target",
                "risk_score": 90,
                "critical_defects": 1,
                "sensors_online": 4,
                "drone_zone_m": 300
            }
            st.rerun()

with col_kpi:
    risk_val = current_target["risk_score"]
    badge_cls = "badge-success" if risk_val >= 90 else ("badge-blue" if risk_val >= 80 else "badge-critical")
    status_text = "NOMINAL COMPLIANCE" if risk_val >= 90 else ("ACTION MONITORED" if risk_val >= 80 else "HIGH HAZARD ALERT")
    
    st.markdown(f"""
    <div class="dark-card" style="padding: 12px 18px !important; margin-bottom: 0 !important;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="{badge_cls}">{status_text}</span>
            <span style="font-size:12px; color:#94A3B8;">Health Index</span>
        </div>
        <h2 style="font-size: 28px; margin: 4px 0 0 0;" class="accent-cyan">{risk_val} / 100</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# 5. ADVANCED FOLIUM MAP ENGINE & OVERLAY CONTROLS
# =========================================================
col_map, col_spatial_info = st.columns([2.4, 1])

with col_map:
    st.markdown(f"### 🗺️ GIS Spatial Map View — {current_target['label']}")

    # Base Tile Mapping Selection
    tile_dict = {
        "Dark Matter (CartoDB)": ("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", "CartoDB dark_all"),
        "OpenStreetMap Standard": ("OpenStreetMap", "OpenStreetMap"),
        "Satellite Aerial (Esri)": ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", "Esri WorldImagery"),
        "Terrain Topography": ("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", "OpenTopoMap")
    }
    
    tile_url, tile_attr = tile_dict[tile_provider]

    # Initialize Folium Map
    m = folium.Map(
        location=[current_target["lat"], current_target["lon"]],
        zoom_start=16,
        tiles=tile_url if "http" in tile_url else tile_url,
        attr=tile_attr if "http" in tile_url else None
    )

    # Add MiniMap & Measurement Tools
    MiniMap(toggle_display=True, tile_layer="OpenStreetMap").add_to(m)
    MeasureControl(position='topright', active_color='#38BDF8', completed_color='#10B981').add_to(m)

    # 1. Active Targeted Pin Marker
    folium.Marker(
        [current_target["lat"], current_target["lon"]],
        popup=folium.Popup(f"""
            <div style="font-family: sans-serif; font-size:13px; width:200px;">
                <b style="color:#0284C7;">{current_target['site_code']}: {current_target['label']}</b><br>
                <b>Road:</b> {current_target['road']}<br>
                <b>Typology:</b> {current_target['type']}<br>
                <b>Health Score:</b> {current_target['risk_score']}/100<br>
                <b>Critical Defects:</b> {current_target['critical_defects']}
            </div>
        """, max_width=250),
        tooltip=f"🎯 Active Target: {current_target['label']}",
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

    # 2. Drone Geofence Audit Radius Circle
    if show_drone_zone:
        folium.Circle(
            radius=current_target["drone_zone_m"],
            location=[current_target["lat"], current_target["lon"]],
            popup=f"Drone Autonomous Scan Radius: {current_target['drone_zone_m']}m",
            color="#38BDF8",
            fill=True,
            fill_color="#0284C7",
            fill_opacity=0.18
        ).add_to(m)

    # 3. Structural Defect Heatmap Layer
    if show_defect_heatmap:
        # Generating realistic spatial defect clusters around Solapur sites
        np.random.seed(42)
        heat_data = []
        for name, info in SOLAPUR_LOCATIONS.items():
            num_points = info["critical_defects"] * 6 + 4
            lats = info["lat"] + np.random.normal(0, 0.0015, num_points)
            lons = info["lon"] + np.random.normal(0, 0.0015, num_points)
            weights = np.random.uniform(0.4, 1.0, num_points)
            for la, lo, w in zip(lats, lons, weights):
                heat_data.append([la, lo, w])
        
        HeatMap(heat_data, radius=15, blur=12, min_opacity=0.3, max_val=1.0).add_to(m)

    # 4. Live IoT Telemetry Pin Cluster Layer
    if show_sensor_nodes:
        sensor_cluster = MarkerCluster(name="Live IoT Sensor Nodes").add_to(m)
        for name, info in SOLAPUR_LOCATIONS.items():
            for i in range(2):
                s_lat = info["lat"] + (i * 0.0008 - 0.0004)
                s_lon = info["lon"] + (i * 0.0008 - 0.0004)
                folium.CircleMarker(
                    location=[s_lat, s_lon],
                    radius=6,
                    popup=f"IoT Node SNS-{info['type'][:3].upper()}-0{i+1}<br>Microstrain: {180 + i*45} µε",
                    color="#10B981",
                    fill=True,
                    fill_color="#34D399",
                    fill_opacity=0.9
                ).add_to(sensor_cluster)

    # Render Map in Streamlit with dynamic click interaction key
    map_output = st_folium(m, width="100%", height=480, key=f"gis_map_{current_target['lat']}_{current_target['lon']}_{tile_provider}")

    # Check for user click event on the map
    if map_output and map_output.get("last_clicked"):
        clicked_lat = map_output["last_clicked"]["lat"]
        clicked_lon = map_output["last_clicked"]["lng"]
        st.info(f"📍 Map Click Captured: Lat {clicked_lat:.5f}° N, Lon {clicked_lon:.5f}° E. Click 'Set Active Custom Location' above to inspect.")

with col_spatial_info:
    st.markdown("### 📌 Spatial Target Telemetry")

    st.markdown(f"""
    <div class="dark-card">
        <h4 class="accent-cyan" style="margin-top:0;">{current_target['site_code']}</h4>
        <h3 style="font-size:18px; margin: 4px 0 12px 0;">{current_target['label']}</h3>
        <p><b>Road / Route:</b> <span style="color:#38BDF8;">{current_target['road']}</span></p>
        <p><b>Latitude Coordinate:</b> {current_target['lat']:.5f}° N</p>
        <p><b>Longitude Coordinate:</b> {current_target['lon']:.5f}° E</p>
        <p><b>Asset Typology:</b> {current_target['type']}</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <p><b>Drone Geofence Perimeter:</b> {current_target['drone_zone_m']} m radius</p>
        <p><b>Deployed IoT Sensors:</b> <span class="accent-green">{current_target['sensors_online']} Nodes Active</span></p>
        <p><b>Active Critical Defects:</b> <span style="color:#EF4444; font-weight:bold;">{current_target['critical_defects']} Anomalies</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ⚡ GIS Quick Actions")
    if st.button("🚀 Launch AI Crack Segmentation for Site", use_container_width=True, type="primary"):
        st.success(f"Site {current_target['site_code']} loaded into AI Inspection Workspace!")

st.divider()

# =========================================================
# 6. REGIONAL INFRASTRUCTURE REGISTRY & DATA EXPORT
# =========================================================
st.markdown("### 📋 Solapur Infrastructure Asset Registry")

registry_data = [
    {
        "Site Code": name.split(":")[0],
        "Site Name / Facility": name.split(":")[1].strip(),
        "Road / Access Route": info["road"],
        "Typology": info["type"],
        "Latitude (°N)": info["lat"],
        "Longitude (°E)": info["lon"],
        "Health Score": info["risk_score"],
        "Critical Defects": info["critical_defects"],
        "IoT Nodes": info["sensors_online"],
        "Inspection Status": "ACTIVE TARGET" if name == selected_site_key else "Registered Site"
    }
    for name, info in SOLAPUR_LOCATIONS.items()
]

registry_df = pd.DataFrame(registry_data)

st.dataframe(
    registry_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Health Score": st.column_config.ProgressColumn("Health Score", min_value=0, max_value=100, format="%d / 100")
    }
)

# Export Capabilities
st.markdown("#### 📥 Export Spatial Site Registry")
col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.download_button(
        label="💾 Download Site Registry (.CSV)",
        data=registry_df.to_csv(index=False),
        file_name=f"Solapur_GIS_Registry_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_exp2:
    # GeoJSON generation
    geojson_features = []
    for row in registry_data:
        geojson_features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [row["Longitude (°E)"], row["Latitude (°N)"]]},
            "properties": row
        })
    geojson_data = json.dumps({"type": "FeatureCollection", "features": geojson_features}, indent=2)

    st.download_button(
        label="🌐 Download GeoJSON Layer (.GEOJSON)",
        data=geojson_data,
        file_name=f"Solapur_GIS_Sites_{datetime.now().strftime('%Y%m%d')}.geojson",
        mime="application/json",
        use_container_width=True
    )

# =========================================================
# FOOTER
# =========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI GIS HUB</b> | Solapur Geographical Site Command System<br>
    Developed by <b>Ritika Bhumkar</b> & <b>Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
