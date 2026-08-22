import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
import json
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import time

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
    .stApp { background-color: #07090E; color: #E2E8F0; }
    .block-container {
        padding-top: 1rem; padding-bottom: 1rem;
        padding-left: 1.5rem; padding-right: 1.5rem;
    }
    .card-dark {
        background-color: #0F172A; border: 1px solid #1E293B;
        border-radius: 8px; padding: 12px; margin-bottom: 10px;
    }
    .status-normal { background-color: #15803D; color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .status-warning { background-color: #B45309; color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .status-critical { background-color: #B91C1C; color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Session State Initializations
if 'extracted_params' not in st.session_state:
    st.session_state.extracted_params = {
        "width_m": 12.0, "depth_m": 16.0, "floors": 2, "wall_height_m": 3.2, "wall_thick_m": 0.23
    }

if 'selected_component' not in st.session_state:
    st.session_state.selected_component = "Ground Columns"

if 'drawing_rotation' not in st.session_state:
    st.session_state.drawing_rotation = 0

# ==========================================
# 1. SIDEBAR: BLUEPRINT & CONTROLS
# ==========================================
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    st.markdown("### 🏢 Building Typology")
    bld_type = st.selectbox(
        "Select Structural Classification",
        ["Residential Villa / Apartment", "Commercial Office Block", "Industrial Warehouse / Plant", "Hospital / Critical Infrastructure"]
    )

    st.markdown("---")
    st.markdown("### 📂 Blueprint & Site Data")
    
    tab_draw, tab_photo = st.tabs(["📄 Blueprint", "📸 Site Photos"])
    
    with tab_draw:
        uploaded_plan = st.file_uploader("Upload Floor / Structural Plan", type=["png", "jpg", "jpeg"], key="plan_upload")
        
        if uploaded_plan is not None:
            st.markdown("#### 🔄 360° Drawing Orientation")
            st.session_state.drawing_rotation = st.slider("Rotation Angle", 0, 360, st.session_state.drawing_rotation, 90)
            
            raw_img = Image.open(uploaded_plan)
            rotated_img = raw_img.rotate(-st.session_state.drawing_rotation, expand=True)
            st.image(rotated_img, caption="Aligned Blueprint", use_container_width=True)

            if st.button("🤖 Generate 3D BIM Model", type="primary"):
                try:
                    uploaded_plan.seek(0)
                    file_bytes = np.asarray(bytearray(uploaded_plan.read()), dtype=np.uint8)
                    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    
                    if img is not None:
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                        clean_walls = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                        contours, _ = cv2.findContours(clean_walls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        
                        if contours:
                            main_c = max(contours, key=cv2.contourArea)
                            x, y, w, h = cv2.boundingRect(main_c)
                            scale = 35.0
                            calc_w = max(8.0, round(w / scale, 1))
                            calc_d = max(10.0, round(h / scale, 1))
                            st.session_state.extracted_params["width_m"] = min(calc_w, 24.0)
                            st.session_state.extracted_params["depth_m"] = min(calc_d, 24.0)
                            st.success(f"✅ Extracted Dimensions: {calc_w}m × {calc_d}m")
                except Exception as e:
                    st.error(f"Error parsing blueprint: {e}")

    with tab_photo:
        uploaded_photos = st.file_uploader("Upload Field Photos", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        if uploaded_photos:
            for idx, img_file in enumerate(uploaded_photos):
                file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                edges = cv2.Canny(blur, 50, 150)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                result_img = img.copy()
                
                defects_found = 0
                for c in contours:
                    if cv2.contourArea(c) > 60:
                        x, y, w, h = cv2.boundingRect(c)
                        cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(result_img, "DEFECT", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                        defects_found += 1
                
                c1, c2 = st.columns(2)
                with c1: st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption=f"Raw #{idx+1}")
                with c2: st.image(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB), caption=f"AI Scan: {defects_found} Anomalies")

    st.markdown("---")
    st.markdown("### 📐 BIM Structural Parameters")
    building_w = st.number_input("Building Width (m)", value=float(st.session_state.extracted_params["width_m"]), step=0.5)
    building_d = st.number_input("Building Depth (m)", value=float(st.session_state.extracted_params["depth_m"]), step=0.5)
    num_floors = st.number_input("Floor Count", min_value=1, max_value=8, value=2)
    wall_h = st.number_input("Story Height (m)", value=3.2, step=0.1)
    wall_t = st.number_input("Wall Thickness (m)", value=0.23, step=0.02)
    show_rebars = st.checkbox("Show Steel Rebars", value=True)

    total_height_m = round(num_floors * wall_h + 1.2, 1)

# ==========================================
# 2. MAIN PAGE CONTROLS
# ==========================================
st.title("📐 Structural Digital Twin & IoT Visualizer")

STRUCTURAL_COMPONENTS = [
    "Foundation Footing", "Plinth Beam", "Ground Columns", "Primary Beams", 
    "Floor Slab", "Structural Walls", "Roof Slab", "Parapet Wall"
]

col_sel1, col_sel2 = st.columns([3, 1])
with col_sel1:
    selected_comp = st.selectbox("🔗 Interactive Component Highlighter", STRUCTURAL_COMPONENTS, index=STRUCTURAL_COMPONENTS.index(st.session_state.selected_component) if st.session_state.selected_component in STRUCTURAL_COMPONENTS else 2)
    st.session_state.selected_component = selected_comp
with col_sel2:
    st.markdown("<div style='padding-top:25px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<span class='status-normal'>Highlighted: {st.session_state.selected_component}</span>", unsafe_allow_html=True)

ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 2])
with ctrl1: render_style = st.selectbox("Render Mode", ["Architectural Section (Cutaway)", "Realistic Architectural 3D", "RCC Concrete + Rebars", "X-Ray Structural Wireframe"])
with ctrl2: bld_behavior = st.selectbox("Simulation", ["Static / Unloaded State", "Wind Sway Behavior", "Seismic Oscillation", "Soil Settlement"])
with ctrl3: preset_cam = st.selectbox("Camera View", ["Architectural Perspective", "Front Elevation", "Side Elevation", "Isometric Aerial"])

behavior_pct = st.slider("Behavior Load / Deflection Magnitude Intensity (%)", 0, 100, 50, 5)

cam_distance = max(building_w, building_d, total_height_m) * 1.5
cam_matrix = {
    "Architectural Perspective": [building_w * 1.3, total_height_m * 1.15, cam_distance * 0.95],
    "Front Elevation": [0, total_height_m * 0.5, cam_distance * 1.2],
    "Side Elevation": [cam_distance * 1.2, total_height_m * 0.5, 0],
    "Isometric Aerial": [building_w * 1.1, cam_distance * 1.3, building_d * 1.1]
}[preset_cam]

is_rcc = (render_style == "RCC Concrete + Rebars")
is_xray = (render_style == "X-Ray Structural Wireframe")
is_cutaway = (render_style == "Architectural Section (Cutaway)")

DEMO_SENSOR_DATA = [
    {"id": "SNS-FND-01", "component": "Foundation Footing", "type": "Settlement", "value": 0.04, "unit": "deg", "status": "Normal", "pos": [-building_w/2 + 0.5, 0.2, -building_d/2 + 0.5]},
    {"id": "SNS-COL-03", "component": "Ground Columns", "type": "Strain", "value": 920, "unit": "µε", "status": "Warning", "pos": [building_w/2 - 0.5, 2.0, building_d/2 - 0.5]},
    {"id": "SNS-BM-04", "component": "Primary Beams", "type": "Vibration", "value": 4.1, "unit": "m/s²", "status": "Critical", "pos": [0.0, wall_h + 0.9, -building_d/2]}
]
sensors_json = json.dumps(DEMO_SENSOR_DATA)
behavior_code = {"Static / Unloaded State": "none", "Wind Sway Behavior": "wind", "Seismic Oscillation": "seismic", "Soil Settlement": "settlement"}[bld_behavior]

# ==========================================
# 3. HIGH-DETAILED THREE.JS 3D ENGINE
# ==========================================
threejs_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; overflow: hidden; background: radial-gradient(circle at center, #111827 0%, #030712 100%); font-family: monospace; }}
        #canvas-container {{ width: 100vw; height: 100vh; }}
        #hud {{
            position: absolute; top: 12px; left: 12px; color: #38BDF8;
            font-size: 11px; background: rgba(15,23,42,0.92); padding: 10px 14px;
            border: 1px solid #1E293B; border-radius: 6px; z-index: 10;
            backdrop-filter: blur(8px); box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }}
        #mode-badge {{
            position: absolute; top: 12px; right: 12px; color: #FACC15; font-weight: bold;
            font-size: 11px; background: rgba(15,23,42,0.92); padding: 6px 12px;
            border: 1px solid #FACC15; border-radius: 4px; z-index: 10;
            display: { 'block' if is_cutaway else 'none' };
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="hud">
        <b>3D BIM DIGITAL TWIN: {bld_type.upper()}</b><br>
        DIMENSIONS: {building_w}m (W) × {building_d}m (D) × {total_height_m}m (H) | FLOORS: {num_floors}<br>
        ACTIVE SELECTION: <span style="color:#00E5FF; font-weight:bold;">{selected_comp.upper()}</span>
    </div>
    <div id="mode-badge">⚠️ CUTAWAY SECTION ACTIVE (INTERIOR VISIBLE)</div>
    <div id="canvas-container"></div>
    <script>
        const sensors = {sensors_json};
        const activeComponent = "{selected_comp}";
        const container = document.getElementById('canvas-container');
        
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x030712, 0.008);

        const camera = new THREE.PerspectiveCamera(42, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set({cam_matrix[0]}, {cam_matrix[1]}, {cam_matrix[2]});

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, powerPreference: "high-performance" }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.15;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.target.set(0, {total_height_m * 0.4}, 0);
        controls.maxPolarAngle = Math.PI / 2 + 0.05;

        // Lighting
        scene.add(new THREE.HemisphereLight(0xF8FAFC, 0x0F172A, 0.9));

        const sunLight = new THREE.DirectionalLight(0xFFFBEB, 1.8);
        sunLight.position.set(40, 80, 50);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 4096;
        sunLight.shadow.mapSize.height = 4096;
        sunLight.shadow.camera.near = 0.5;
        sunLight.shadow.camera.far = 200;
        const d = 35;
        sunLight.shadow.camera.left = -d; sunLight.shadow.camera.right = d;
        sunLight.shadow.camera.top = d; sunLight.shadow.camera.bottom = -d;
        sunLight.shadow.bias = -0.0001;
        scene.add(sunLight);

        const fillLight = new THREE.DirectionalLight(0x38BDF8, 0.5);
        fillLight.position.set(-40, 30, -30);
        scene.add(fillLight);

        // Ground
        const ground = new THREE.Mesh(
            new THREE.PlaneGeometry(150, 150),
            new THREE.MeshStandardMaterial({{ color: 0x0B1120, roughness: 0.9, metalness: 0.1 }})
        );
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.05;
        ground.receiveShadow = true;
        scene.add(ground);
        scene.add(new THREE.GridHelper(60, 60, 0x1E293B, 0x0F172A));

        const isXray = {str(is_xray).lower()};
        const isRCC = {str(is_rcc).lower()};
        const isCutaway = {str(is_cutaway).lower()};
        const drawRebars = {str(show_rebars).lower()};
        const behavior = "{behavior_code}";
        const intensityFactor = {behavior_pct} / 100.0;

        function getMaterial(compName, baseColor = 0xE2E8F0, roughness = 0.65, metalness = 0.05) {{
            const isHighlighted = (compName === activeComponent);
            return new THREE.MeshPhysicalMaterial({{ 
                color: isHighlighted ? 0x00FFFF : baseColor, 
                metalness: isHighlighted ? 0.2 : metalness,
                roughness: isHighlighted ? 0.3 : roughness,
                clearcoat: isHighlighted ? 0.9 : 0.04,
                transparent: true,
                opacity: isHighlighted ? 0.98 : (isRCC ? 0.35 : (isXray ? 0.15 : 1.0)),
                wireframe: isXray,
                emissive: isHighlighted ? 0x0088FF : 0x000000,
                emissiveIntensity: isHighlighted ? 0.5 : 0.0
            }});
        }}

        function createBIMMesh(geometry, material, addEdge=true) {{
            const mesh = new THREE.Mesh(geometry, material);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            if (addEdge && !isXray) {{
                const edges = new THREE.EdgesGeometry(geometry, 28);
                const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({{ color: 0x1E293B, transparent: true, opacity: 0.4 }}));
                mesh.add(line);
            }}
            return mesh;
        }}

        const glassMat = new THREE.MeshPhysicalMaterial({{ color: 0x7DD3FC, transmission: 0.95, opacity: 1.0, transparent: true, roughness: 0.05, ior: 1.5, thickness: 0.05 }});
        const darkFrameMat = new THREE.MeshStandardMaterial({{ color: 0x0F172A, roughness: 0.4, metalness: 0.8 }});
        const woodDoorMat = new THREE.MeshStandardMaterial({{ color: 0x3E2723, roughness: 0.8, metalness: 0.1 }});
        const rebarMat = new THREE.MeshStandardMaterial({{ color: 0xFF5500, metalness: 0.95, roughness: 0.2 }});
        const woodFloorMat = new THREE.MeshStandardMaterial({{ color: 0x8D6E63, roughness: 0.7 }});
        const furnitureMat = new THREE.MeshStandardMaterial({{ color: 0x607D8B, roughness: 0.8 }});
        
        const stirrupGeo = new THREE.EdgesGeometry(new THREE.BoxGeometry(0.32, 0.01, 0.32));
        const stirrupMat = new THREE.LineBasicMaterial({{ color: 0xFF5500 }});

        const buildingGroup = new THREE.Group();
        const W = {building_w}; const D = {building_d}; const H = {wall_h}; const T = {wall_t}; const floors = {num_floors};
        
        const colXs = [-W/2 + 0.35, 0, W/2 - 0.35];
        const colZs = [-D/2 + 0.35, 0, D/2 - 0.35];

        // 1. Foundation Footings
        const footingMat = getMaterial("Foundation Footing", 0x334155, 0.9);
        const footingGeo = new THREE.BoxGeometry(1.4, 0.45, 1.4);
        colXs.forEach(x => {{ colZs.forEach(z => {{ 
            const foot = createBIMMesh(footingGeo, footingMat);
            foot.position.set(x, 0.22, z);
            buildingGroup.add(foot); 
        }}); }});

        // 2. Stepped Plinth Platform & Steps
        const plinthBase = createBIMMesh(new THREE.BoxGeometry(W + 1.0, 0.25, D + 1.0), getMaterial("Plinth Beam", 0x1E293B, 0.8));
        plinthBase.position.set(0, 0.35, 0); buildingGroup.add(plinthBase);

        const plinth = createBIMMesh(new THREE.BoxGeometry(W + 0.4, 0.4, D + 0.4), getMaterial("Plinth Beam", 0x475569, 0.7));
        plinth.position.set(0, 0.68, 0); buildingGroup.add(plinth);

        if(!isXray) {{
            for(let i=0; i<3; i++) {{
                const stepW = W * 0.25;
                const step = createBIMMesh(new THREE.BoxGeometry(stepW, 0.15, 0.3), getMaterial("Plinth Beam", 0x475569));
                step.position.set(0, 0.15/2 + i*0.15, D/2 + 0.2 + (3-i)*0.3 - 0.15);
                buildingGroup.add(step);
            }}
        }}

        let currentY = 0.88;

        // 3. Multi-Floor Construction with Real Internal Structures
        for (let f = 0; f < floors; f++) {{
            if (!isXray && !isRCC) {{
                const roomLight = new THREE.PointLight(0xFDF8E1, 1.0, W * 1.8);
                roomLight.position.set(0, currentY + H/2 + 0.5, 0);
                buildingGroup.add(roomLight);

                const woodFloor = createBIMMesh(new THREE.BoxGeometry(W - T, 0.04, D - T), woodFloorMat);
                woodFloor.position.set(0, currentY + 0.02, 0);
                buildingGroup.add(woodFloor);

                const spineWall = createBIMMesh(new THREE.BoxGeometry(T, H, D * 0.65), getMaterial("Structural Walls", 0xF1F5F9));
                spineWall.position.set(-W * 0.1, currentY + H/2, -D * 0.1);
                buildingGroup.add(spineWall);

                const bedWall = createBIMMesh(new THREE.BoxGeometry(W * 0.38, H, T), getMaterial("Structural Walls", 0xF1F5F9));
                bedWall.position.set(-W * 0.3, currentY + H/2, 0);
                buildingGroup.add(bedWall);

                const bed = createBIMMesh(new THREE.BoxGeometry(2.0, 0.45, 1.8), furnitureMat, false);
                bed.position.set(-W/2 + 1.3, currentY + 0.225, -D/2 + 1.3);
                buildingGroup.add(bed);

                const desk = createBIMMesh(new THREE.BoxGeometry(1.6, 0.75, 0.8), woodDoorMat, false);
                desk.position.set(W/2 - 1.4, currentY + 0.375, -D/2 + 1.3);
                buildingGroup.add(desk);

                const stairSteps = 15;
                const stepH = H / stairSteps;
                for (let s = 0; s < stairSteps; s++) {{
                    const stairStep = createBIMMesh(new THREE.BoxGeometry(1.2, stepH, 0.26), getMaterial("Floor Slab", 0xE2E8F0), false);
                    stairStep.position.set(W/2 - 1.4, currentY + stepH/2 + s*stepH, D/2 - 1.2 - s*0.26);
                    buildingGroup.add(stairStep);
                }}
            }}

            const colMat = getMaterial("Ground Columns", 0x475569, 0.5);
            colXs.forEach(cx => {{
                colZs.forEach(cz => {{
                    const colMesh = createBIMMesh(new THREE.BoxGeometry(0.45, H, 0.45), colMat);
                    colMesh.position.set(cx, currentY + H/2, cz); buildingGroup.add(colMesh);
                    
                    if (drawRebars && (isRCC || isXray)) {{
                        [[-0.15,-0.15], [0.15,-0.15], [-0.15,0.15], [0.15,0.15]].forEach(off => {{
                            const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, H + 0.1), rebarMat);
                            bar.position.set(cx + off[0], currentY + H/2, cz + off[1]); buildingGroup.add(bar);
                        }});
                        
                        const numStirrups = Math.floor(H / 0.2);
                        for(let s = 0; s <= numStirrups; s++) {{
                            const stirrup = new THREE.LineSegments(stirrupGeo, stirrupMat);
                            stirrup.position.set(cx, currentY + (s * 0.2) + 0.1, cz);
                            buildingGroup.add(stirrup);
                        }}
                    }}
                }});
            }});

            const beamMat = getMaterial("Primary Beams", 0x334155, 0.6);
            const beamX = createBIMMesh(new THREE.BoxGeometry(W, 0.4, 0.4), beamMat);
            beamX.position.set(0, currentY + H - 0.2, 0); buildingGroup.add(beamX);

            const beamZ = createBIMMesh(new THREE.BoxGeometry(0.4, 0.4, D), beamMat);
            beamZ.position.set(0, currentY + H - 0.2, 0); buildingGroup.add(beamZ);

            const wallMat = getMaterial("Structural Walls", 0xF1F5F9, 0.6);
            const accentMat = getMaterial("Structural Walls", 0x334155, 0.4, 0.2);

            const backWall = createBIMMesh(new THREE.BoxGeometry(W, H, T), wallMat);
            backWall.position.set(0, currentY + H/2, -D/2 + T/2); buildingGroup.add(backWall);

            const buildSideWall = (wallX) => {{
                const wallLower = createBIMMesh(new THREE.BoxGeometry(T, 0.9, D), wallMat);
                wallLower.position.set(wallX, currentY + 0.45, 0); buildingGroup.add(wallLower);

                const wallUpper = createBIMMesh(new THREE.BoxGeometry(T, H - 2.4, D), wallMat);
                wallUpper.position.set(wallX, currentY + H - (H - 2.4)/2, 0); buildingGroup.add(wallUpper);

                if (!isXray && !isRCC) {{
                    const winGlass = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.5, D - 1.6), glassMat);
                    winGlass.position.set(wallX, currentY + 1.65, 0); buildingGroup.add(winGlass);

                    const winFrame = createBIMMesh(new THREE.BoxGeometry(0.12, 1.52, D - 1.56), darkFrameMat, false);
                    winFrame.position.set(wallX, currentY + 1.65, 0); buildingGroup.add(winFrame);
                    
                    const mullionV = createBIMMesh(new THREE.BoxGeometry(0.13, 1.52, 0.06), darkFrameMat, false);
                    mullionV.position.set(wallX, currentY + 1.65, 0); buildingGroup.add(mullionV);

                    const chajja = createBIMMesh(new THREE.BoxGeometry(0.6, 0.08, D - 1.2), accentMat);
                    chajja.position.set(wallX + (wallX > 0 ? 0.3 : -0.3), currentY + 2.45, 0);
                    buildingGroup.add(chajja);
                }}
            }};

            buildSideWall(-W/2 + T/2);

            if (!isCutaway) {{
                buildSideWall(W/2 - T/2);

                const frontWallLeft = createBIMMesh(new THREE.BoxGeometry(W * 0.32, H, T), wallMat);
                frontWallLeft.position.set(-W * 0.34, currentY + H/2, D/2 - T/2); buildingGroup.add(frontWallLeft);

                const frontWallRight = createBIMMesh(new THREE.BoxGeometry(W * 0.32, H, T), wallMat);
                frontWallRight.position.set(W * 0.34, currentY + H/2, D/2 - T/2); buildingGroup.add(frontWallRight);

                const frontLintel = createBIMMesh(new THREE.BoxGeometry(W * 0.36, H - 2.3, T), accentMat);
                frontLintel.position.set(0, currentY + H - (H - 2.3)/2, D/2 - T/2); buildingGroup.add(frontLintel);

                if (!isXray && !isRCC) {{
                    const door = createBIMMesh(new THREE.BoxGeometry(W * 0.15, 2.3, 0.08), woodDoorMat, false);
                    door.position.set(W * -0.08, currentY + 1.15, D/2 - T/2); buildingGroup.add(door);
                    
                    const sideGlass = new THREE.Mesh(new THREE.BoxGeometry(W * 0.15, 2.3, 0.04), glassMat);
                    sideGlass.position.set(W * 0.08, currentY + 1.15, D/2 - T/2); buildingGroup.add(sideGlass);
                    
                    const doorFrame = createBIMMesh(new THREE.BoxGeometry(W * 0.35, 2.3, 0.1), darkFrameMat, false);
                    doorFrame.position.set(0, currentY + 1.15, D/2 - T/2); buildingGroup.add(doorFrame);
                }}
            }}

            currentY += H;

            const slabMat = getMaterial("Floor Slab", 0xCBD5E1, 0.7);
            const slab = createBIMMesh(new THREE.BoxGeometry(W + 0.8, 0.28, D + 0.8), slabMat);
            slab.position.set(0, currentY + 0.14, 0); buildingGroup.add(slab);

            if (!isXray && !isRCC && !isCutaway) {{
                const botRail = createBIMMesh(new THREE.BoxGeometry(W * 0.52, 0.08, 0.1), darkFrameMat, false);
                botRail.position.set(0, currentY + 0.28 + 0.04, D/2 + 0.35); buildingGroup.add(botRail);

                const balconyGlass = new THREE.Mesh(new THREE.BoxGeometry(W * 0.5, 0.9, 0.03), glassMat);
                balconyGlass.position.set(0, currentY + 0.28 + 0.45, D/2 + 0.35); buildingGroup.add(balconyGlass);

                const topRail = createBIMMesh(new THREE.BoxGeometry(W * 0.52, 0.05, 0.12), darkFrameMat, false);
                topRail.position.set(0, currentY + 0.28 + 0.9, D/2 + 0.35); buildingGroup.add(topRail);
            }}

            currentY += 0.28;
        }}

        // 4. Roof Slab & Parapet
        const roofMat = getMaterial("Roof Slab", 0x64748B, 0.6);
        const roofSlab = createBIMMesh(new THREE.BoxGeometry(W + 1.0, 0.35, D + 1.0), roofMat);
        roofSlab.position.set(0, currentY + 0.175, 0); buildingGroup.add(roofSlab);

        const parapetMat = getMaterial("Parapet Wall", 0x1E293B, 0.4, 0.3);
        const parapet = createBIMMesh(new THREE.BoxGeometry(W + 1.0, 0.9, T), parapetMat);
        parapet.position.set(0, currentY + 0.8, D/2 + 0.5 - T/2); buildingGroup.add(parapet);

        const coping = createBIMMesh(new THREE.BoxGeometry(W + 1.1, 0.08, T + 0.1), getMaterial("Parapet Wall", 0x475569));
        coping.position.set(0, currentY + 1.25, D/2 + 0.5 - T/2); buildingGroup.add(coping);

        scene.add(buildingGroup);

        // 5. Sensor Nodes
        const sensorLights = [];
        sensors.forEach(sns => {{
            let sColor = 0x22C55E; if (sns.status === "Warning") sColor = 0xEAB308; if (sns.status === "Critical") sColor = 0xEF4444;
            const sphere = new THREE.Mesh(
                new THREE.SphereGeometry(0.35, 32, 32),
                new THREE.MeshStandardMaterial({{ color: sColor, emissive: sColor, emissiveIntensity: 2.2, roughness: 0.1 }})
            );
            sphere.position.set(sns.pos[0], sns.pos[1], sns.pos[2]); scene.add(sphere);
            const light = new THREE.PointLight(sColor, 2.5, 4.5); light.position.set(sns.pos[0], sns.pos[1], sns.pos[2]); scene.add(light);
            sensorLights.push(light);
        }});

        function animate() {{
            requestAnimationFrame(animate);
            if (behavior === "none" && !isCutaway) {{ controls.autoRotate = true; controls.autoRotateSpeed = 0.5; }} 
            else {{ controls.autoRotate = false; }}
            controls.update();
            const time = Date.now() * 0.0025;

            sensorLights.forEach(l => {{ l.intensity = 1.8 + Math.sin(time * 3) * 0.9; }});

            buildingGroup.rotation.set(0, 0, 0); buildingGroup.position.set(0, 0, 0); buildingGroup.scale.set(1, 1, 1);

            if (behavior === "wind") {{ buildingGroup.rotation.z = Math.sin(time * 1.5) * (0.02 * intensityFactor); buildingGroup.position.x = Math.sin(time * 1.5) * (0.8 * intensityFactor); }} 
            else if (behavior === "seismic") {{ buildingGroup.position.x = Math.sin(time * 14) * (0.35 * intensityFactor); buildingGroup.position.z = Math.cos(time * 11) * (0.2 * intensityFactor); }} 
            else if (behavior === "settlement") {{ buildingGroup.position.y = -0.4 * intensityFactor; buildingGroup.rotation.x = 0.03 * intensityFactor; buildingGroup.rotation.z = 0.02 * intensityFactor; }} 
            
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""
components.html(threejs_code, height=680)

# ==========================================
# 4. LOWER PAGE: 2D BLUEPRINT & LIVE TELEMETRY
# ==========================================
st.markdown("---")
col_dwg1, col_dwg2 = st.columns([1, 1])

with col_dwg1:
    st.markdown("#### 📄 Component Highlight Preview")
    
    # 2D Plotly Blueprint Floor Plan
    fig_bp = go.Figure()
    
    fig_bp.add_shape(type="rect", x0=-building_w/2, y0=-building_d/2, x1=building_w/2, y1=building_d/2, line=dict(color="#334155", width=3))
    fig_bp.add_shape(type="line", x0=-building_w/2, y0=0, x1=0, y1=0, line=dict(color="#334155", width=2))
    fig_bp.add_shape(type="line", x0=-building_w*0.1, y0=-building_d/2, x1=-building_w*0.1, y1=building_d/3, line=dict(color="#334155", width=2))
    fig_bp.add_shape(type="rect", x0=building_w/2 - 1.8, y0=building_d/2 - 3.5, x1=building_w/2 - 0.4, y1=building_d/2 - 0.5, line=dict(color="#475569", width=1, dash="dot"))
    fig_bp.add_annotation(x=building_w/2 - 1.1, y=building_d/2 - 2.0, text="Staircase", showarrow=False, font=dict(color="#64748B", size=10))

    # Highlighting logic matching the 3D scene
    hl_color = "#00E5FF"
    if st.session_state.selected_component == "Ground Columns":
        cols_x = [-building_w/2 + 0.5, 0, building_w/2 - 0.5]
        cols_y = [-building_d/2 + 0.5, 0, building_d/2 - 0.5]
        for cx in cols_x:
            for cy in cols_y:
                fig_bp.add_shape(type="rect", x0=cx-0.35, y0=cy-0.35, x1=cx+0.35, y1=cy+0.35, fillcolor=hl_color, line_color=hl_color)
    elif st.session_state.selected_component == "Structural Walls":
        fig_bp.add_shape(type="rect", x0=-building_w/2, y0=-building_d/2, x1=building_w/2, y1=building_d/2, line=dict(color=hl_color, width=5))
        fig_bp.add_shape(type="line", x0=-building_w/2, y0=0, x1=0, y1=0, line=dict(color=hl_color, width=4))
        fig_bp.add_shape(type="line", x0=-building_w*0.1, y0=-building_d/2, x1=-building_w*0.1, y1=building_d/3, line=dict(color=hl_color, width=4))
    elif "Slab" in st.session_state.selected_component:
        fig_bp.add_shape(type="rect", x0=-building_w/2, y0=-building_d/2, x1=building_w/2, y1=building_d/2, fillcolor="rgba(0, 229, 255, 0.2)", line=dict(color=hl_color, width=2))
    elif st.session_state.selected_component == "Foundation Footing":
        cols_x = [-building_w/2 + 0.5, 0, building_w/2 - 0.5]
        cols_y = [-building_d/2 + 0.5, 0, building_d/2 - 0.5]
        for cx in cols_x:
            for cy in cols_y:
                fig_bp.add_shape(type="rect", x0=cx-0.7, y0=cy-0.7, x1=cx+0.7, y1=cy+0.7, fillcolor="rgba(0, 229, 255, 0.3)", line=dict(color=hl_color, width=2))
    else:
        fig_bp.add_shape(type="rect", x0=-building_w/2, y0=-building_d/2, x1=building_w/2, y1=building_d/2, line=dict(color=hl_color, width=3))

    fig_bp.update_layout(
        plot_bgcolor="#0F172A", paper_bgcolor="#0F172A",
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=10, b=10), height=380
    )
    st.plotly_chart(fig_bp, use_container_width=True)

with col_dwg2:
    st_header, st_toggle = st.columns([2, 1])
    with st_header:
        st.markdown("#### 📍 Live IoT Telemetry")
    with st_toggle:
        live_update = st.toggle("🔴 Live Stream", value=False)

    comp_sensors = [s for s in DEMO_SENSOR_DATA if s["component"] == st.session_state.selected_component]
    
    if comp_sensors:
        if 'sensor_history' not in st.session_state:
            st.session_state.sensor_history = {}

        for s in comp_sensors:
            sensor_id = s['id']
            base_val = s['value']
            status = s['status']
            
            if sensor_id not in st.session_state.sensor_history:
                np.random.seed(hash(sensor_id) % (2**32))
                time_now = datetime.now()
                times = [(time_now - timedelta(seconds=i*2)).strftime('%H:%M:%S') for i in range(30, 0, -1)]
                scale = base_val * (0.05 if status == 'Normal' else (0.15 if status == 'Warning' else 0.3))
                readings = np.random.normal(loc=base_val, scale=scale, size=30).tolist()
                st.session_state.sensor_history[sensor_id] = {"Time": times, "Reading": readings}
            
            history = st.session_state.sensor_history[sensor_id]
            current_time_str = datetime.now().strftime('%H:%M:%S')
            
            if history["Time"][-1] != current_time_str:
                history["Time"].append(current_time_str)
                last_val = history["Reading"][-1]
                next_val = max(0, np.random.normal(loc=last_val, scale=base_val * 0.03))
                history["Reading"].append(next_val)
                if len(history["Time"]) > 30:
                    history["Time"].pop(0)
                    history["Reading"].pop(0)

            df_sensor = pd.DataFrame(history)
            current_reading = round(history["Reading"][-1], 2)

            st.markdown(f"""
            <div class="card-dark">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:bold; color:#38BDF8;">{sensor_id} ({s['type']})</span>
                    <span class="status-{'normal' if status=='Normal' else ('warning' if status=='Warning' else 'critical')}">{status}</span>
                </div>
                <div style="font-size:18px; font-weight:bold; margin-top:8px;">{current_reading} {s['unit']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            fig = px.line(df_sensor, x="Time", y="Reading", title=f"{s['type']} Live Trend ({st.session_state.selected_component})", markers=True)
            line_color = '#22C55E' if status == 'Normal' else ('#EAB308' if status == 'Warning' else '#EF4444')
            fig.update_traces(line_color=line_color, marker=dict(size=5))
            fig.update_layout(
                plot_bgcolor='#07090E', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0',
                margin=dict(l=10, r=10, t=35, b=10), height=220,
                xaxis=dict(showgrid=False, title="", tickangle=-45),
                yaxis=dict(gridcolor='#1E293B', title=f"{s['unit']}")
            )
            st.plotly_chart(fig, use_container_width=True)
            
            csv_data = df_sensor.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {sensor_id} Report (CSV)",
                data=csv_data, file_name=f"{sensor_id}_Inspection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv", use_container_width=True
            )
            
        if live_update:
            time.sleep(2)
            st.rerun()
    else:
        st.info(f"No active direct sensors bound to {st.session_state.selected_component}.")