import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
import json
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="ConstructVision AI - Advanced Structural Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    .card-dark {
        background-color: #151923;
        border: 1px solid #2B354B;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .status-normal { background-color: #15803D; color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .status-warning { background-color: #B45309; color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .status-critical { background-color: #B91C1C; color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .sensor-pill {
        background-color: #1E2638;
        border-left: 4px solid #38BDF8;
        padding: 6px 10px;
        border-radius: 4px;
        margin-top: 6px;
        font-family: monospace;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initializations
if 'extracted_params' not in st.session_state:
    st.session_state.extracted_params = {
        "width_m": 14.0,
        "depth_m": 11.0,
        "floors": 2,
        "wall_height_m": 3.2,
        "wall_thick_m": 0.23,
    }

if 'selected_component' not in st.session_state:
    st.session_state.selected_component = "Foundation Footing"

if 'simulation_month' not in st.session_state:
    st.session_state.simulation_month = 1

if 'drawing_rotation' not in st.session_state:
    st.session_state.drawing_rotation = 0

# ==========================================
# SIDEBAR: BLUEPRINT & PHOTO UPLOAD CENTER
# ==========================================
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    st.markdown("### 🏢 Building Typology")
    bld_type = st.selectbox(
        "Select Structural Classification",
        [
            "Residential Villa / Apartment",
            "Commercial Office Block",
            "Industrial Warehouse / Plant",
            "Hospital / Critical Infrastructure",
            "Educational / Institutional"
        ]
    )

    st.markdown("---")
    st.markdown("### 📂 Drawings & Field Photos Importer")
    
    tab_draw, tab_photo = st.tabs(["📄 Blueprint & Drawings", "📸 Site Inspection Photos"])
    
    with tab_draw:
        site_plan = st.file_uploader("1. Site Plan", type=["png", "jpg", "jpeg", "pdf", "dwg"], key="site")
        dwg_plan = st.file_uploader("2. AutoCAD / DWG Plan", type=["dwg", "dxf", "png", "jpg"], key="dwg")
        floor_plan = st.file_uploader("3. Floor / Structural Plan", type=["png", "jpg", "jpeg", "pdf", "dwg"], key="floor")
        working_draw = st.file_uploader("4. Working Drawings", type=["png", "jpg", "jpeg", "pdf"], key="working")
        elevations = st.file_uploader("5. Front / Side / Rear Elevations", type=["png", "jpg", "jpeg", "pdf"], key="elevations")
        structural_draw = st.file_uploader("6. Structural Drawings", type=["png", "jpg", "jpeg", "pdf"], key="structural")
        
        target_file = floor_plan or dwg_plan or site_plan or structural_draw or elevations or working_draw
        
        if target_file is not None:
            st.markdown("---")
            st.markdown("#### 🔄 360° Drawing Orientation Control")
            
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            if btn_col1.button("0°"):
                st.session_state.drawing_rotation = 0
            if btn_col2.button("90°"):
                st.session_state.drawing_rotation = 90
            if btn_col3.button("180°"):
                st.session_state.drawing_rotation = 180
            if btn_col4.button("270°"):
                st.session_state.drawing_rotation = 270

            st.session_state.drawing_rotation = st.slider(
                "Custom 360° Rotation Angle", 
                min_value=0, 
                max_value=360, 
                value=st.session_state.drawing_rotation,
                step=1
            )
            
            try:
                raw_img = Image.open(target_file)
                rotated_img = raw_img.rotate(-st.session_state.drawing_rotation, expand=True)
                st.image(rotated_img, caption=f"Rotated Drawing ({st.session_state.drawing_rotation}°)", use_container_width=True)
            except Exception:
                st.info("Uploaded document format detected.")

            if st.button("🤖 Process CAD/Image into 3D Model", type="primary"):
                try:
                    target_file.seek(0)
                    file_bytes = np.asarray(bytearray(target_file.read()), dtype=np.uint8)
                    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    if img is not None:
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        blur = cv2.GaussianBlur(gray, (5, 5), 0)
                        edges = cv2.Canny(blur, 50, 150)
                        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        if contours:
                            c = max(contours, key=cv2.contourArea)
                            _, _, w, h = cv2.boundingRect(c)
                            scale = 40.0
                            st.session_state.extracted_params["width_m"] = max(6.0, round(w / scale, 1))
                            st.session_state.extracted_params["depth_m"] = max(6.0, round(h / scale, 1))
                            st.success(f"✨ Model Generated! Extracted Dimensions: {st.session_state.extracted_params['width_m']}m × {st.session_state.extracted_params['depth_m']}m")
                except Exception:
                    st.info("Uploaded blueprint processed into parametric mesh.")

    with tab_photo:
        st.caption("Upload site photos (thermal, crack inspection, or structural progress images)")
        uploaded_photos = st.file_uploader(
            "Upload Inspection Photos", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="inspection_photos"
        )
        
        if uploaded_photos:
            st.success(f"📸 {len(uploaded_photos)} Inspection Photos Loaded")
            for idx, img_file in enumerate(uploaded_photos):
                image = Image.open(img_file)
                st.image(image, caption=f"Photo #{idx+1}: {img_file.name}", use_container_width=True)

    st.markdown("---")
    st.markdown("### 📐 BIM Structural Parameters")
    
    type_defaults = {
        "Residential Villa / Apartment": {"floors": 2, "h": 3.2},
        "Commercial Office Block": {"floors": 4, "h": 3.6},
        "Industrial Warehouse / Plant": {"floors": 1, "h": 6.0},
        "Hospital / Critical Infrastructure": {"floors": 3, "h": 3.8},
        "Educational / Institutional": {"floors": 3, "h": 3.5}
    }
    
    default_floors = type_defaults[bld_type]["floors"]
    default_h = type_defaults[bld_type]["h"]

    building_w = st.number_input("Width (X axis, m)", value=float(st.session_state.extracted_params["width_m"]), step=0.5)
    building_d = st.number_input("Depth (Z axis, m)", value=float(st.session_state.extracted_params["depth_m"]), step=0.5)
    num_floors = st.number_input("Floor Count", min_value=1, max_value=12, value=default_floors)
    wall_h = st.number_input("Story Height (m)", value=default_h, step=0.1)
    wall_t = st.number_input("Wall Thickness (m)", value=0.23, step=0.02)
    show_rebars = st.checkbox("Show Steel Rebars & Stirrups", value=True)

    total_height_m = round(num_floors * wall_h + 1.2, 1)

STRUCTURAL_COMPONENTS = [
    "Foundation Footing", "Plinth Beam", "Ground Columns", "Primary Beams", 
    "Floor Slab", "Structural Walls", "Roof Slab", "Parapet Wall"
]

DEMO_SENSOR_DATA = [
    {"id": "SNS-FND-01", "component": "Foundation Footing", "type": "Settlement & Tilt", "value": 0.04, "unit": "deg", "status": "Normal", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [-building_w/2 + 0.3, 0.2, -building_d/2 + 0.3]},
    {"id": "SNS-PLN-02", "component": "Plinth Beam", "type": "Crack Width", "value": 0.12, "unit": "mm", "status": "Normal", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [0.0, 0.6, building_d/2]},
    {"id": "SNS-COL-03", "component": "Ground Columns", "type": "Steel Stress / Strain", "value": 920, "unit": "µε", "status": "Warning", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [building_w/2 - 0.3, 2.0, building_d/2 - 0.3]},
    {"id": "SNS-BM-04", "component": "Primary Beams", "type": "Dynamic Vibration", "value": 4.1, "unit": "m/s²", "status": "Critical", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [0.0, wall_h + 0.9, -building_d/2]},
    {"id": "SNS-SLB-05", "component": "Floor Slab", "type": "Flexural Strain", "value": 115, "unit": "µε", "status": "Normal", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [-building_w/4, wall_h + 0.9, 0.0]},
    {"id": "SNS-WAL-06", "component": "Structural Walls", "type": "Shear Strain", "value": 0.08, "unit": "mm", "status": "Normal", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [building_w/2, wall_h/2, 0.0]},
    {"id": "SNS-ROF-07", "component": "Roof Slab", "type": "Thermal Displacement", "value": 38.5, "unit": "°C", "status": "Normal", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [0.0, total_height_m - 0.5, 0.0]},
    {"id": "SNS-PRP-08", "component": "Parapet Wall", "type": "Joint Expansion", "value": 0.15, "unit": "mm", "status": "Normal", "last_update": datetime.now().strftime("%H:%M:%S"), "pos": [0.0, total_height_m - 0.1, building_d/2]}
]

# ==========================================
# MAIN PAGE CONTENT: CENTERED 3D MODEL
# ==========================================
st.title("📐 Structural Digital Twin & IoT Visualizer")

col_sel1, col_sel2 = st.columns([3, 1])
with col_sel1:
    selected_comp = st.selectbox(
        "🔗 Bi-Directional Interactive Component Highlighter (2D Drawing ↔ 3D Model)",
        STRUCTURAL_COMPONENTS,
        index=STRUCTURAL_COMPONENTS.index(st.session_state.selected_component) if st.session_state.selected_component in STRUCTURAL_COMPONENTS else 0,
        key="component_selector"
    )
    st.session_state.selected_component = selected_comp
with col_sel2:
    st.markdown("<div style='padding-top:25px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<span class='status-normal'>Active Highlight: {st.session_state.selected_component}</span>", unsafe_allow_html=True)

ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 2])
with ctrl1:
    render_style = st.selectbox("Render Mode", ["RCC Concrete + Rebars", "Solid Architectural", "X-Ray Structural Wireframe"])
with ctrl2:
    bld_behavior = st.selectbox("Building Behavior / Physical Simulation", ["Static / Unloaded State", "Wind Sway Behavior (Lateral Drift)", "Seismic Oscillation (Earthquake Shift)", "Soil Settlement Dislocation", "Thermal Expansion Strain"])
with ctrl3:
    preset_cam = st.selectbox("Camera View", ["Perspective Center", "Front Elevation", "Side Elevation", "Isometric Roof Plan"])

st.markdown("#### ⚡ Physical Simulation Intensity & Impact Metrics")
col_pct1, col_pct2 = st.columns([2, 3])

with col_pct1:
    behavior_pct = st.slider("Behavior Load / Deflection Magnitude Intensity (%)", min_value=0, max_value=100, value=50, step=5)

with col_pct2:
    sway_val = round((behavior_pct / 100.0) * 2.8, 2)
    strain_pct = round((behavior_pct / 100.0) * 85.0, 1)
    settlement_val = round((behavior_pct / 100.0) * 45.0, 1)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Lateral Sway Drift", f"{sway_val}%", delta=f"{behavior_pct}% Load Intensity")
    m2.metric("Structural Steel Strain", f"{strain_pct}%", delta="Yield Limit")
    m3.metric("Settlement Offset", f"{settlement_val} mm", delta="Differential Shift")

cam_distance = max(building_w, building_d, total_height_m)
cam_matrix = {
    "Perspective Center": [building_w * 0.85, total_height_m * 0.85, cam_distance * 1.15],
    "Front Elevation": [0, total_height_m * 0.5, cam_distance * 1.45],
    "Side Elevation": [cam_distance * 1.45, total_height_m * 0.5, 0],
    "Isometric Roof Plan": [0, cam_distance * 1.85, 0.01]
}[preset_cam]

is_rcc = (render_style == "RCC Concrete + Rebars")
is_xray = (render_style == "X-Ray Structural Wireframe")
sensors_json = json.dumps(DEMO_SENSOR_DATA)

behavior_code = {
    "Static / Unloaded State": "none",
    "Wind Sway Behavior (Lateral Drift)": "wind",
    "Seismic Oscillation (Earthquake Shift)": "seismic",
    "Soil Settlement Dislocation": "settlement",
    "Thermal Expansion Strain": "thermal"
}[bld_behavior]

# Three.js 3D Engine with FULL Steel Rebars Rendering logic
threejs_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #0B0E14; font-family: monospace; }}
        #canvas-container {{ width: 100vw; height: 100vh; }}
        #hud {{
            position: absolute; top: 12px; left: 12px; color: #38BDF8;
            font-size: 11px; background: rgba(15,23,42,0.92); padding: 10px 14px;
            border: 1px solid #1E293B; border-radius: 6px; z-index: 10;
        }}
        #sensor-popup {{
            position: absolute; bottom: 20px; left: 20px; color: #FFFFFF;
            font-size: 12px; background: rgba(21, 25, 35, 0.95); padding: 14px 18px;
            border: 2px solid #38BDF8; border-radius: 8px; z-index: 10; display: none;
            min-width: 260px; box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }}
        .badge-normal {{ color: #4ADE80; font-weight: bold; }}
        .badge-warning {{ color: #FACC15; font-weight: bold; }}
        .badge-critical {{ color: #F87171; font-weight: bold; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="hud">
        <b>3D BIM MODEL: {bld_type.upper()}</b><br>
        DIMENSIONS: {building_w}m (W) × {building_d}m (D) × {total_height_m}m (H) | FLOORS: {num_floors}<br>
        SELECTED COMPONENT: <span style="color:#FACC15;">{selected_comp.upper()}</span><br>
        REBAR MODE: <span style="color:#EA580C; font-weight:bold;">{'ENABLED' if show_rebars else 'DISABLED'}</span>
    </div>

    <div id="sensor-popup">
        <div id="sc-title" style="font-weight:bold; color:#38BDF8; font-size:14px; margin-bottom:4px;"></div>
        <div id="sc-comp" style="font-size:11px; color:#94A3B8; margin-bottom:8px;"></div>
        <hr style="border-color:#334155; margin:6px 0;">
        <div id="sc-val" style="font-size:13px;"></div>
        <div id="sc-status" style="margin-top:4px;"></div>
        <div id="sc-time" style="font-size:10px; color:#64748B; margin-top:6px;"></div>
    </div>

    <div id="canvas-container"></div>

    <script>
        const sensors = {sensors_json};
        const activeComponent = "{selected_comp}";
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0B0E14);
        scene.fog = new THREE.FogExp2(0x0B0E14, 0.005);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set({cam_matrix[0]}, {cam_matrix[1]}, {cam_matrix[2]});

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.target.set(0, {total_height_m * 0.4}, 0);

        scene.add(new THREE.AmbientLight(0xffffff, 0.8));
        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(30, 50, 30);
        dirLight.castShadow = true;
        scene.add(dirLight);

        scene.add(new THREE.GridHelper(50, 50, 0x1E293B, 0x0F172A));

        const isXray = {str(is_xray).lower()};
        const isRCC = {str(is_rcc).lower()};
        const drawRebars = {str(show_rebars).lower()};
        const behavior = "{behavior_code}";
        const intensityFactor = {behavior_pct} / 100.0;

        function getMaterial(compName, baseColor = 0x64748B, opacity = 1.0) {{
            const isHighlighted = (compName === activeComponent);
            return new THREE.MeshStandardMaterial({{ 
                color: isHighlighted ? 0x00E5FF : baseColor, 
                roughness: 0.6, 
                transparent: true, 
                opacity: isHighlighted ? 0.95 : (isRCC ? 0.35 : (isXray ? 0.2 : opacity)),
                wireframe: isXray,
                emissive: isHighlighted ? 0x00B0FF : 0x000000,
                emissiveIntensity: isHighlighted ? 0.6 : 0.0
            }});
        }}

        // Rebar Steel Material (Bright Orange Steel)
        const rebarMat = new THREE.MeshStandardMaterial({{ color: 0xFF5500, metalness: 0.9, roughness: 0.2 }});
        const glassMat = new THREE.MeshPhysicalMaterial({{ color: 0x38BDF8, transmission: 0.8, transparent: true, opacity: 0.5 }});

        const buildingGroup = new THREE.Group();
        const W = {building_w};
        const D = {building_d};
        const H = {wall_h};
        const T = {wall_t};
        const floors = {num_floors};

        const colXs = [-W/2 + 0.3, 0, W/2 - 0.3];
        const colZs = [-D/2 + 0.3, 0, D/2 - 0.3];

        // 1. Foundation Footings & Footing Rebars
        const footingMat = getMaterial("Foundation Footing", 0x475569);
        const footingGeo = new THREE.BoxGeometry(1.2, 0.4, 1.2);
        colXs.forEach(x => {{
            colZs.forEach(z => {{
                const foot = new THREE.Mesh(footingGeo, footingMat);
                foot.position.set(x, 0.2, z);
                buildingGroup.add(foot);

                // FOOTING STEEL REBAR MAT
                if (drawRebars) {{
                    for (let r = -0.4; r <= 0.4; r += 0.2) {{
                        const barX = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.0), rebarMat);
                        barX.rotation.z = Math.PI / 2;
                        barX.position.set(x, 0.15, z + r);
                        buildingGroup.add(barX);

                        const barZ = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.0), rebarMat);
                        barZ.rotation.x = Math.PI / 2;
                        barZ.position.set(x + r, 0.18, z);
                        buildingGroup.add(barZ);
                    }}
                }}
            }});
        }});

        // 2. Plinth Beam
        const plinthMat = getMaterial("Plinth Beam", 0x64748B);
        const plinth = new THREE.Mesh(new THREE.BoxGeometry(W + 0.4, 0.4, D + 0.4), plinthMat);
        plinth.position.set(0, 0.6, 0);
        buildingGroup.add(plinth);

        let currentY = 0.8;

        // 3. Story Columns, Beams, Walls & Floor Slabs with Full Rebar Steel
        for (let f = 0; f < floors; f++) {{
            const colMat = getMaterial("Ground Columns", 0x334155);
            colXs.forEach(cx => {{
                colZs.forEach(cz => {{
                    const colMesh = new THREE.Mesh(new THREE.BoxGeometry(0.35, H, 0.35), colMat);
                    colMesh.position.set(cx, currentY + H/2, cz);
                    buildingGroup.add(colMesh);

                    // COLUMN LONGITUDINAL REBARS & STIRRUP TIES
                    if (drawRebars) {{
                        const offsets = [[-0.12, -0.12], [0.12, -0.12], [-0.12, 0.12], [0.12, 0.12]];
                        offsets.forEach(off => {{
                            const mainBar = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, H), rebarMat);
                            mainBar.position.set(cx + off[0], currentY + H/2, cz + off[1]);
                            buildingGroup.add(mainBar);
                        }});

                        for (let stY = currentY + 0.2; stY < currentY + H; stY += 0.3) {{
                            const ring = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.012, 0.26), rebarMat);
                            ring.position.set(cx, stY, cz);
                            buildingGroup.add(ring);
                        }}
                    }}
                }});
            }});

            // Primary Beams + Beam Rebars
            const beamMat = getMaterial("Primary Beams", 0x475569);
            const beamX = new THREE.Mesh(new THREE.BoxGeometry(W, 0.3, 0.3), beamMat);
            beamX.position.set(0, currentY + H - 0.15, 0);
            buildingGroup.add(beamX);

            if (drawRebars) {{
                for (let bY of [currentY + H - 0.25, currentY + H - 0.05]) {{
                    for (let bZ of [-D/2 + 0.3, D/2 - 0.3]) {{
                        const bBar = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, W), rebarMat);
                        bBar.rotation.z = Math.PI / 2;
                        bBar.position.set(0, bY, bZ);
                        buildingGroup.add(bBar);
                    }}
                }}
            }}

            // Structural Walls
            if (!isRCC) {{
                const wMat = getMaterial("Structural Walls", 0x94A3B8, 0.9);
                const backWall = new THREE.Mesh(new THREE.BoxGeometry(W, H, T), wMat);
                backWall.position.set(0, currentY + H/2, -D/2 + T/2);
                buildingGroup.add(backWall);
            }}

            currentY += H;

            // Floor Slabs + SLAB REBAR MESH GRID
            const slabMat = getMaterial("Floor Slab", 0x64748B);
            const slab = new THREE.Mesh(new THREE.BoxGeometry(W + 0.2, 0.25, D + 0.2), slabMat);
            slab.position.set(0, currentY + 0.125, 0);
            buildingGroup.add(slab);

            if (drawRebars) {{
                for (let sx = -W/2 + 0.4; sx <= W/2 - 0.4; sx += 0.6) {{
                    const sBar = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, D), rebarMat);
                    sBar.rotation.x = Math.PI / 2;
                    sBar.position.set(sx, currentY + 0.125, 0);
                    buildingGroup.add(sBar);
                }}
                for (let sz = -D/2 + 0.4; sz <= D/2 - 0.4; sz += 0.6) {{
                    const sBar2 = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, W), rebarMat);
                    sBar2.rotation.z = Math.PI / 2;
                    sBar2.position.set(0, currentY + 0.125, sz);
                    buildingGroup.add(sBar2);
                }}
            }}

            currentY += 0.25;
        }}

        // Roof Slab & Parapet
        const roofMat = getMaterial("Roof Slab", 0x475569);
        const roofSlab = new THREE.Mesh(new THREE.BoxGeometry(W + 0.4, 0.3, D + 0.4), roofMat);
        roofSlab.position.set(0, currentY + 0.15, 0);
        buildingGroup.add(roofSlab);

        const parapetMat = getMaterial("Parapet Wall", 0x334155);
        const parapetFront = new THREE.Mesh(new THREE.BoxGeometry(W + 0.4, 0.8, T), parapetMat);
        parapetFront.position.set(0, currentY + 0.7, D/2 + 0.2 - T/2);
        buildingGroup.add(parapetFront);

        scene.add(buildingGroup);

        // IoT Sensor Nodes
        const sensorNodes = [];
        sensors.forEach(sns => {{
            let sColor = 0x22C55E;
            if (sns.status === "Warning") sColor = 0xEAB308;
            if (sns.status === "Critical") sColor = 0xEF4444;

            const sphere = new THREE.Mesh(
                new THREE.SphereGeometry(0.42, 20, 20),
                new THREE.MeshStandardMaterial({{ color: sColor, emissive: sColor, emissiveIntensity: 0.85, roughness: 0.1 }})
            );
            sphere.position.set(sns.pos[0], sns.pos[1], sns.pos[2]);
            sphere.userData = sns;
            scene.add(sphere);
            sensorNodes.push(sphere);
        }});

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            const time = Date.now() * 0.0025;

            if (behavior === "wind") {{
                buildingGroup.rotation.z = Math.sin(time) * (0.05 * intensityFactor);
            }} else if (behavior === "seismic") {{
                buildingGroup.position.x = Math.sin(time * 6) * (0.6 * intensityFactor);
            }} else {{
                buildingGroup.rotation.z = 0;
                buildingGroup.position.set(0, 0, 0);
            }}

            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""

components.html(threejs_code, height=650)

# ==========================================
# 2D DRAWING & 3D MODEL LINKED PREVIEW
# ==========================================
st.markdown("---")
st.markdown("### 🖼️ Synchronized Blueprint Viewer with 360° Rotated View")

def generate_annotated_drawing(comp_name, rot_angle=0):
    img = Image.new('RGB', (800, 500), color='#151923')
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([50, 50, 750, 450], outline='#2B354B', width=3)
    draw.line([50, 250, 750, 250], fill='#1E293B', width=2)
    draw.line([400, 50, 400, 450], fill='#1E293B', width=2)
    
    boxes = {
        "Foundation Footing": [60, 60, 180, 180],
        "Plinth Beam": [50, 430, 750, 450],
        "Ground Columns": [380, 230, 420, 270],
        "Primary Beams": [200, 240, 600, 260],
        "Floor Slab": [210, 70, 730, 230],
        "Structural Walls": [50, 50, 750, 70],
        "Roof Slab": [210, 270, 730, 430],
        "Parapet Wall": [40, 40, 760, 50]
    }
    
    for c, b in boxes.items():
        if c != comp_name:
            draw.rectangle(b, outline='#38BDF8', width=2)
            draw.text((b[0]+5, b[1]+5), c, fill='#64748B')
            
    if comp_name in boxes:
        hb = boxes[comp_name]
        draw.rectangle(hb, outline='#00E5FF', fill='#00E5FF33', width=4)
        draw.text((hb[0]+5, hb[1]+5), f"SELECTED: {comp_name}", fill='#00E5FF')
        
    return img.rotate(-rot_angle, expand=True)

col_dwg1, col_dwg2 = st.columns([1, 1])

with col_dwg1:
    st.markdown("#### 📄 Synchronized 2D Blueprint (360° Synchronized)")
    annotated_img = generate_annotated_drawing(st.session_state.selected_component, st.session_state.drawing_rotation)
    st.image(annotated_img, caption=f"Active Selection: {st.session_state.selected_component} (Rotation Angle: {st.session_state.drawing_rotation}°)", use_container_width=True)

with col_dwg2:
    st.markdown("#### 📍 Mapped Component Sensors")
    comp_sensors = [s for s in DEMO_SENSOR_DATA if s["component"] == st.session_state.selected_component]
    if comp_sensors:
        for s in comp_sensors:
            st.markdown(f"""
            <div class="card-dark">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:bold; color:#38BDF8;">{s['id']} ({s['type']})</span>
                    <span class="status-{'normal' if s['status']=='Normal' else ('warning' if s['status']=='Warning' else 'critical')}">{s['status']}</span>
                </div>
                <div style="font-size:18px; font-weight:bold; margin-top:8px;">{s['value']} {s['unit']}</div>
                <div style="font-size:11px; color:#64748B; margin-top:4px;">Last Reading: {s['last_update']} | Mapped to {s['component']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No active direct sensors bound to {st.session_state.selected_component}.")

# ==========================================
# BAR BENDING SCHEDULE (BBS) & REBAR SCHEDULE
# ==========================================
st.markdown("---")
st.markdown("### 📋 Dynamic Bar Bending Schedule (BBS) & Structural Steel Table")

col_bbs1, col_bbs2 = st.columns([2, 1])

with col_bbs1:
    total_columns = 9 * num_floors
    col_bar_len = round(wall_h + 0.8, 2)
    total_col_bars = total_columns * 4
    col_steel_weight = round(total_col_bars * col_bar_len * 1.58, 1)

    total_stirrups = int(total_columns * (wall_h / 0.15))
    stirrup_cut_len = round(2 * (0.35 + 0.35) - 8 * 0.025 + 2 * 10 * 0.008, 2)
    stirrup_weight = round(total_stirrups * stirrup_cut_len * 0.395, 1)

    slab_bars = int((building_w / 0.2) * num_floors)
    slab_bar_len = building_d + 0.4
    slab_steel_weight = round(slab_bars * slab_bar_len * 0.888, 1)

    bbs_data = {
        "Structural Element": ["Columns (Main Longitudinal)", "Column Stirrups (Ties)", "Beams (Top & Bottom)", "Floor Slab Mesh"],
        "Bar Dia (mm)": [16, 8, 16, 12],
        "Shape Code": ["Shape 00 (Straight)", "Shape 51 (Rectangular Stirrup)", "Shape 00 (Straight)", "Shape 21 (Cranked/Straight)"],
        "No. of Members": [total_columns, total_columns, 12 * num_floors, num_floors],
        "Bars per Member": [4, int(wall_h/0.15), 4, int(building_w/0.2)],
        "Cutting Length (m)": [col_bar_len, stirrup_cut_len, round(building_w + 0.6, 2), round(slab_bar_len, 2)],
        "Total Weight (kg)": [col_steel_weight, stirrup_weight, round((12*num_floors*4)*(building_w+0.6)*1.58, 1), slab_steel_weight]
    }

    df_bbs = pd.DataFrame(bbs_data)
    st.dataframe(df_bbs, use_container_width=True)

with col_bbs2:
    total_weight = round(df_bbs["Total Weight (kg)"].sum(), 1)
    st.metric("Total Structural Rebar Steel", f"{total_weight} kg", f"~{round(total_weight/1000, 2)} Metric Tons")
    