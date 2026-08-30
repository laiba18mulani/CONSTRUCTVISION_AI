import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D Building Digital Twin Engine",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Civil Engineering Digital Twin Engine</title>
  
  <!-- External Libraries -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; }
    html, body { background: #070a12; color: #e2e8f0; width: 100%; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }

    /* Top Navigation Bar */
    #navbar {
      height: 54px;
      background: #0f172a;
      border-bottom: 1px solid #1e293b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 18px;
      z-index: 20;
      flex-shrink: 0;
    }
    .brand { font-size: 1.05rem; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 10px; }
    .brand-tag { background: #0284c7; color: #fff; font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .nav-stats { display: flex; gap: 18px; align-items: center; font-size: 0.8rem; color: #94a3b8; }
    .nav-stat-item { display: flex; align-items: center; gap: 6px; }
    .nav-stat-val { font-weight: 600; color: #f8fafc; }

    /* Main Container Split */
    #main-wrapper { flex: 1; display: flex; position: relative; overflow: hidden; }
    #canvas-container { flex: 1; height: 100%; position: relative; background: #070a12; }

    /* Floating Viewport Overlays */
    #viewport-tools {
      position: absolute;
      top: 14px;
      left: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 10;
    }
    .tool-group {
      background: rgba(15, 23, 42, 0.90);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 6px;
      display: flex;
      gap: 6px;
      backdrop-filter: blur(10px);
      align-items: center;
      flex-wrap: wrap;
    }
    .layer-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #94a3b8;
      padding: 7px 11px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .layer-btn:hover, .layer-btn.active {
      background: #0284c7;
      color: #fff;
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(2, 132, 199, 0.4);
    }

    .struct-select-label { font-size: 0.75rem; color: #38bdf8; font-weight: 700; padding: 0 4px; text-transform: uppercase; }

    #camera-tools {
      position: absolute;
      bottom: 20px;
      left: 14px;
      z-index: 10;
    }

    /* Sidebars */
    .sidebar {
      width: 380px;
      background: rgba(15, 23, 42, 0.95);
      border-left: 1px solid #1e293b;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      height: 100%;
      overflow-y: auto;
      flex-shrink: 0;
    }
    
    .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; transition: border-color 0.2s; }
    .card:hover { border-color: #475569; }
    .card-title { font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.08em; margin-bottom: 8px; font-weight: 700; display: flex; justify-space-between; align-items: center; }
    .metric-val { font-size: 1.5rem; font-weight: 700; color: #38bdf8; display: flex; align-items: baseline; gap: 6px; }
    .status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; background: #065f46; color: #34d399; }
    .status-badge.alert { background: #881337; color: #fecdd3; }
    .status-badge.warning { background: #78350f; color: #fde68a; }

    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .sub-metric { font-size: 0.75rem; color: #94a3b8; }
    .sub-val { font-size: 0.95rem; font-weight: 600; color: #f8fafc; }

    select, input[type="range"] {
      width: 100%;
      background: #0f172a;
      border: 1px solid #334155;
      color: #e2e8f0;
      padding: 8px;
      border-radius: 6px;
      outline: none;
      font-size: 0.8rem;
    }

    .btn { background: #2563eb; color: #fff; border: none; padding: 9px 12px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.8rem; width: 100%; transition: 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; }
    .btn:hover { background: #1d4ed8; }
    .btn-alert { background: #dc2626; }
    .btn-alert:hover { background: #b91c1c; }
    .btn-warning { background: #d97706; }
    .btn-warning:hover { background: #b45309; }
    .btn-water { background: #0284c7; }
    .btn-water:hover { background: #0369a1; }
    .btn-secondary { background: #334155; color: #cbd5e1; }
    .btn-secondary:hover { background: #475569; color: #fff; }

    .chart-container { position: relative; height: 70px; width: 100%; background: #0f172a; border-radius: 6px; border: 1px solid #1e293b; margin-top: 6px; }
    canvas.chart-canvas { width: 100%; height: 100%; display: block; }

    #tooltip {
      position: absolute;
      display: none;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #38bdf8;
      color: #fff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      pointer-events: none;
      z-index: 100;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
    }

    #modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(7, 10, 18, 0.8);
      backdrop-filter: blur(6px);
      z-index: 200;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .modal-box {
      background: #0f172a;
      border: 1px solid #38bdf8;
      width: 500px;
      max-width: 90vw;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }
  </style>
</head>
<body>

<div id="navbar">
  <div class="brand">
    <i class="fa-solid fa-cubes-stacked text-sky-400"></i>
    CIVIL-TWIN ENGINE <span class="brand-tag">v6.0 Ultimate</span>
  </div>
  
  <div class="nav-stats">
    <div class="nav-stat-item">
      <i class="fa-solid fa-building"></i>
      <span>Asset:</span> <span class="nav-stat-val" id="nav-asset-name">2 BHK Residential House</span>
    </div>
    <div class="nav-stat-item">
      <i class="fa-solid fa-wind"></i>
      <span>Wind Speed:</span> <span class="nav-stat-val" id="nav-wind">12.4 km/h</span>
    </div>
    <div class="nav-stat-item">
      <i class="fa-solid fa-bullhorn" id="siren-icon" style="color: #64748b;"></i>
      <span>Siren Alert:</span> <span class="nav-stat-val" id="siren-status-lbl">Standby</span>
    </div>
  </div>

  <div style="display: flex; gap: 8px;">
    <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 0.75rem;" onclick="toggleSirenMute(this)">
      <i class="fa-solid fa-volume-high" id="mute-btn-icon"></i> Audio Siren
    </button>
    <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 0.75rem;" onclick="generateAIReport()">
      <i class="fa-solid fa-file-pdf"></i> Export Audit
    </button>
  </div>
</div>

<div id="main-wrapper">
  <div id="canvas-container">
    <div id="viewport-tools">
      <div class="tool-group">
        <span class="struct-select-label"><i class="fa-solid fa-city"></i> Asset Model:</span>
        <select id="structure-type-select" style="width: 240px; font-weight: 600;" onchange="changeStructureType(this.value)">
          <optgroup label="🏡 Residential">
            <option value="house2bhk" selected>🏡 2 BHK Residential House</option>
            <option value="luxuryVilla">🏰 Luxury Villa (Pool & Garden)</option>
          </optgroup>
          <optgroup label="🏢 Commercial">
            <option value="officeSkyscraper">🏢 Office Skyscraper</option>
            <option value="shoppingMall">🛍️ Shopping Mall & Food Court</option>
          </optgroup>
          <optgroup label="🏭 Industrial">
            <option value="industrialWarehouse">🏭 Warehouse & Construction Crane</option>
            <option value="dataCenter">💻 High-Density Data Center</option>
          </optgroup>
          <optgroup label="🌉 Infrastructure">
            <option value="highwayInfrastructure">🛣️ Smart Highway Infrastructure</option>
            <option value="trussBridge">🌉 Truss Highway Bridge Span</option>
          </optgroup>
          <optgroup label="🏨 Hospitality">
            <option value="luxuryHotel">🏨 Grand Resort Hotel & Pool</option>
          </optgroup>
        </select>
      </div>

      <div class="tool-group">
        <button class="layer-btn active" onclick="setLayer('normal', this)"><i class="fa-solid fa-cubes"></i> BIM Model</button>
        <button class="layer-btn" onclick="setLayer('wireframe', this)"><i class="fa-solid fa-border-all"></i> Wireframe</button>
        <button class="layer-btn" onclick="setLayer('rcc', this)"><i class="fa-solid fa-bars-staggered"></i> RCC Rebar</button>
        <button class="layer-btn" onclick="setLayer('bricks', this)"><i class="fa-solid fa-cubes-stacked"></i> Bricks & Masonry</button>
        <button class="layer-btn" onclick="setLayer('concrete', this)"><i class="fa-solid fa-square"></i> Concrete Core</button>
      </div>
    </div>

    <div id="camera-tools">
      <div class="tool-group">
        <button class="layer-btn" onclick="setCameraView('iso')"><i class="fa-solid fa-camera"></i> Iso</button>
        <button class="layer-btn" onclick="setCameraView('top')"><i class="fa-solid fa-arrows-up-down-left-right"></i> Top</button>
        <button class="layer-btn" onclick="setCameraView('front')"><i class="fa-solid fa-table-cells-large"></i> Elevation</button>
        
        <div style="display:flex; align-items:center; gap:8px; padding-left:10px; border-left:1px solid #334155;">
          <span style="font-size:0.75rem; color:#cbd5e1; font-weight:600;"><i class="fa-solid fa-layer-group text-sky-400"></i> Exploded View:</span>
          <input type="range" id="explode-slider" min="0" max="100" value="0" style="width:100px;" oninput="setExplodeLevel(this.value)" />
        </div>
      </div>
    </div>

    <div id="tooltip"></div>
  </div>

  <div class="sidebar">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h2 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc;" id="sidebar-struct-title">2 BHK Structural Health</h2>
      <span class="status-badge" id="ai-status"><i class="fa-solid fa-circle-check"></i> AI Nominal</span>
    </div>

    <div class="card">
      <div class="card-title">Overall Structural Integrity <i class="fa-solid fa-shield-halved"></i></div>
      <div class="metric-val" id="health-score">
        99.1% <small style="font-size: 0.8rem; color: #34d399; font-weight: normal;">(+0.1%)</small>
      </div>
      <div style="width: 100%; background: #0f172a; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;">
        <div id="health-bar" style="width: 99.1%; background: #0284c7; height: 100%; transition: width 0.5s;"></div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Zone / Sub-System Inspector</div>
      <select id="zone-select" onchange="selectZoneFromDropdown(this.value)"></select>
    </div>

    <div class="card">
      <div class="card-title">Live Telemetry (<span id="zone-name">Entire Structure</span>)</div>
      <div class="grid-2">
        <div>
          <div class="sub-metric">Microstrain (µε)</div>
          <div class="sub-val" id="strain-val">180 µε</div>
        </div>
        <div>
          <div class="sub-metric">Peak Acceleration</div>
          <div class="sub-val" id="vibe-val">0.018 g</div>
        </div>
        <div>
          <div class="sub-metric">Temperature</div>
          <div class="sub-val" id="temp-val">23.1 °C</div>
        </div>
        <div>
          <div class="sub-metric">Active Live Load</div>
          <div class="sub-val" id="occ-val">650 kg</div>
        </div>
      </div>

      <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 8px;">Microstrain Signal (µε)</div>
      <div class="chart-container">
        <canvas id="strainChart" class="chart-canvas"></canvas>
      </div>

      <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 6px;">Vibration Spectral Power ($g/\text{Hz}$)</div>
      <div class="chart-container">
        <canvas id="fftChart" class="chart-canvas"></canvas>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Environmental Hazards & Extreme Stress</div>
      
      <div style="margin-bottom: 8px;">
        <div style="display:flex; justify-content:space-between;" class="sub-metric">
          <span>Lateral Wind Pressure</span>
          <span id="wind-lbl">12% (30 km/h)</span>
        </div>
        <input type="range" id="wind-slider" min="0" max="100" value="12" oninput="updateWindLoad(this.value)" />
      </div>

      <div class="grid-2" style="margin-top: 10px;">
        <button class="btn btn-alert" id="seismic-toggle-btn" onclick="toggleSeismicOscillation()"><i class="fa-solid fa-house-crack"></i> Seismic Test</button>
        <button class="btn btn-water" id="flood-toggle-btn" onclick="toggleFloodSimulation()"><i class="fa-solid fa-water"></i> Flood Rise</button>
      </div>

      <div class="grid-2" style="margin-top: 8px;">
        <button class="btn btn-warning" id="heat-toggle-btn" onclick="toggleHeatwaveSimulation()"><i class="fa-solid fa-sun"></i> Heatwave Stress</button>
        <button class="btn btn-secondary" onclick="turnOffAllSimulations()"><i class="fa-solid fa-power-off"></i> Reset Hazards</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title">BIM Structural Hierarchy</div>
      <div id="bim-hierarchy-tree" style="max-height: 110px; overflow-y: auto; display: flex; flex-direction: column; gap: 2px;"></div>
    </div>

    <div class="card">
      <div class="card-title">AI Predictive Diagnostics</div>
      <p style="font-size: 0.78rem; color: #cbd5e1; line-height: 1.4;" id="ai-insight">
        Structure displays linear elastic response within safe IS 456 stress envelopes.
      </p>
    </div>
  </div>
</div>

<div id="modal-overlay">
  <div class="modal-box">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
      <h3 style="font-size: 1.05rem; color: #38bdf8;" id="modal-title">IoT Sensor Diagnostics</h3>
      <button class="btn btn-secondary" style="width: auto; padding: 4px 8px;" onclick="closeModal()">✕</button>
    </div>
    <div class="grid-2" style="margin-bottom: 12px;">
      <div class="card">
        <div class="sub-metric">Hardware Tag</div>
        <div class="sub-val" id="modal-id">SN-HS2BHK-001</div>
      </div>
      <div class="card">
        <div class="sub-metric">Battery Reserve</div>
        <div class="sub-val">99% (LiFePO4)</div>
      </div>
      <div class="card">
        <div class="sub-metric">Signal Strength</div>
        <div class="sub-val">-62 dBm</div>
      </div>
      <div class="card">
        <div class="sub-metric">Standard</div>
        <div class="sub-val">ISO 17025</div>
      </div>
    </div>
    <button class="btn" onclick="closeModal()">Dismiss Diagnostic View</button>
  </div>
</div>

<script>
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  let audioCtx = null;
  let sirenOsc = null;
  let sirenGain = null;
  let sirenInterval = null;
  let isSirenMuted = false;

  function playTone(freq, type = 'sine', duration = 0.12) {
    if (isSirenMuted) return;
    try {
      if (!audioCtx) audioCtx = new AudioCtx();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch(e) {}
  }

  function startEmergencySiren() {
    if (sirenOsc || isSirenMuted) return;
    try {
      if (!audioCtx) audioCtx = new AudioCtx();
      sirenOsc = audioCtx.createOscillator();
      sirenGain = audioCtx.createGain();
      sirenOsc.type = 'sawtooth';
      sirenOsc.frequency.setValueAtTime(440, audioCtx.currentTime);
      sirenGain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      sirenOsc.connect(sirenGain);
      sirenGain.connect(audioCtx.destination);
      sirenOsc.start();

      let high = false;
      sirenInterval = setInterval(() => {
        if (!sirenOsc) return;
        const targetFreq = high ? 440 : 880;
        sirenOsc.frequency.exponentialRampToValueAtTime(targetFreq, audioCtx.currentTime + 0.35);
        high = !high;
      }, 400);

      document.getElementById('siren-icon').style.color = '#ef4444';
      document.getElementById('siren-status-lbl').innerText = 'SIREN ACTIVE';
      document.getElementById('siren-status-lbl').style.color = '#ef4444';
    } catch(e) {}
  }

  function stopEmergencySiren() {
    if (sirenInterval) { clearInterval(sirenInterval); sirenInterval = null; }
    if (sirenOsc) {
      try { sirenOsc.stop(); sirenOsc.disconnect(); } catch(e) {}
      sirenOsc = null;
    }
    document.getElementById('siren-icon').style.color = '#64748b';
    document.getElementById('siren-status-lbl').innerText = 'Standby';
    document.getElementById('siren-status-lbl').style.color = '#f8fafc';
  }

  function toggleSirenMute(btn) {
    isSirenMuted = !isSirenMuted;
    if (isSirenMuted) {
      stopEmergencySiren();
      btn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i> Muted';
    } else {
      btn.innerHTML = '<i class="fa-solid fa-volume-high"></i> Audio Siren';
    }
  }

  const container = document.getElementById('canvas-container');
  const tooltip = document.getElementById('tooltip');
  
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x070a12);

  const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.set(28, 22, 32);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.maxPolarAngle = Math.PI / 2 - 0.02;

  const grid = new THREE.GridHelper(70, 70, 0x334155, 0x1e293b);
  grid.position.y = -0.01;
  scene.add(grid);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
  scene.add(ambientLight);

  const dirLight = new THREE.DirectionalLight(0x38bdf8, 1.1);
  dirLight.position.set(35, 50, 25);
  dirLight.castShadow = true;
  scene.add(dirLight);

  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1e293b, 0.6);
  scene.add(hemiLight);

  let isFloodActive = false;
  let isHeatwaveActive = false;
  let floodWaterLevel = -10.0;

  const floodGeo = new THREE.BoxGeometry(100, 4, 100);
  const floodMat = new THREE.MeshPhysicalMaterial({ color: 0x0284c7, transparent: true, opacity: 0.6, roughness: 0.1 });
  const floodMesh = new THREE.Mesh(floodGeo, floodMat);
  floodMesh.position.set(0, -10.0, 0);
  floodMesh.visible = false;
  scene.add(floodMesh);

  let currentStructureType = 'house2bhk';
  let activeStructureGroup = new THREE.Group();
  scene.add(activeStructureGroup);

  const sensorNodes = [];
  const animatedParts = [];
  let activeLayer = 'normal';
  let explodeFactor = 0;

  function generateBrickTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 512;
    const ctx = canvas.getContext('2d');
    
    // Mortar background
    ctx.fillStyle = '#e5e7eb'; 
    ctx.fillRect(0, 0, 512, 512);

    const rows = 16; 
    const rowHeight = 512 / rows; 
    const brickWidth = 64;
    const mortar = 4;

    for (let r = 0; r < rows; r++) {
      const y = r * rowHeight;
      const offsetX = (r % 2 === 0) ? 0 : brickWidth / 2;
      for (let x = -brickWidth; x < 512 + brickWidth; x += brickWidth + mortar) {
        // Red terracotta brick variations
        ctx.fillStyle = (r % 3 === 0) ? '#b91c1c' : ((r % 3 === 1) ? '#991b1b' : '#c2410c');
        ctx.fillRect(x + offsetX, y + mortar, brickWidth, rowHeight - mortar);
        
        // Brick edge bevel shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(x + offsetX, y + rowHeight - mortar - 2, brickWidth, 2);
      }
    }
    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping; 
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 2);
    return tex;
  }
  const brickTexture = generateBrickTexture();

  function createSolidBox(group, x, y, z, w, h, d, color = 0x475569, name = 'Box') {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.6 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(x, y, z);
    mesh.castShadow = true; mesh.receiveShadow = true;
    mesh.name = name;
    mesh.userData = { originalColor: color };
    
    // Add internal steel rebar cage representation for structural members
    if (h > 0.5 && w >= 0.2 && d >= 0.2 && !name.toLowerCase().includes('glass')) {
      const rebarCage = new THREE.Group();
      rebarCage.name = 'RebarCage';
      rebarCage.visible = false;
      const rebarMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.1 });
      const barRad = 0.03;

      const xCount = Math.max(2, Math.min(5, Math.ceil(w / 1.0)));
      const zCount = Math.max(2, Math.min(5, Math.ceil(d / 1.0)));

      // Main longitudinal bars
      for (let ix = 0; ix < xCount; ix++) {
        for (let iz = 0; iz < zCount; iz++) {
          if (ix === 0 || ix === xCount - 1 || iz === 0 || iz === zCount - 1) {
            const bx = -w/2 + 0.1 + ix * ((w - 0.2) / (xCount - 1 || 1));
            const bz = -d/2 + 0.1 + iz * ((d - 0.2) / (zCount - 1 || 1));
            const bar = new THREE.Mesh(new THREE.CylinderGeometry(barRad, barRad, h - 0.1, 4), rebarMat);
            bar.position.set(bx, 0, bz);
            rebarCage.add(bar);
          }
        }
      }

      // Horizontal Stirrup Hoops (Full Rectangle)
      const stirrupCount = Math.floor((h - 0.2) / 0.6);
      for (let s = 0; s <= stirrupCount; s++) {
        const hoop = new THREE.Group();
        const hoopY = -h/2 + 0.15 + s * 0.6;
        const hMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xf59e0b, emissiveIntensity: 0.5 });
        
        const h1 = new THREE.Mesh(new THREE.BoxGeometry(w - 0.1, 0.03, 0.03), hMat); h1.position.set(0, hoopY, -d/2 + 0.1); hoop.add(h1);
        const h2 = new THREE.Mesh(new THREE.BoxGeometry(w - 0.1, 0.03, 0.03), hMat); h2.position.set(0, hoopY, d/2 - 0.1); hoop.add(h2);
        const h3 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, d - 0.1), hMat); h3.position.set(-w/2 + 0.1, hoopY, 0); hoop.add(h3);
        const h4 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, d - 0.1), hMat); h4.position.set(w/2 - 0.1, hoopY, 0); hoop.add(h4);
        
        rebarCage.add(hoop);
      }
      mesh.add(rebarCage);
    }

    group.add(mesh);
    return mesh;
  }

  function addIoTNode(group, x, y, z, id, desc) {
    const node = new THREE.Mesh(
      new THREE.SphereGeometry(0.35, 16, 16),
      new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 0.8 })
    );
    node.position.set(x, y, z);
    node.name = `SensorNode_${id}`;
    node.userData = { id: id, desc: desc };
    group.add(node);
    sensorNodes.push(node);
    return node;
  }

  function buildStructure(type) {
    while (activeStructureGroup.children.length > 0) {
      activeStructureGroup.remove(activeStructureGroup.children[0]);
    }
    sensorNodes.length = 0; animatedParts.length = 0;

    if (type === 'house2bhk') create2BHKHouseModel();
    else if (type === 'luxuryVilla') createLuxuryVillaModel();
    else if (type === 'officeSkyscraper') createCommercialTowerModel();
    else if (type === 'shoppingMall') createShoppingMallModel();
    else if (type === 'industrialWarehouse') createIndustrialWarehouseModel();
    else if (type === 'dataCenter') createDataCenterModel();
    else if (type === 'highwayInfrastructure') createHighwayInfrastructureModel();
    else if (type === 'trussBridge') createTrussBridgeModel();
    else if (type === 'luxuryHotel') createLuxuryHotelModel();

    updateUIForStructureType(type);
    setLayer(activeLayer);
    applyExplodeLevel(explodeFactor);
  }

  // 1. 🏡 2 BHK RESIDENTIAL HOUSE MODEL
  function create2BHKHouseModel() {
    const houseGroup = activeStructureGroup;
    createSolidBox(houseGroup, 0, 0.25, 0, 20, 0.5, 16, 0x334155, 'Foundation_Slab');

    const gfGroup = new THREE.Group();
    gfGroup.name = 'Zone_GF_Living_Kitchen';
    gfGroup.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Ground Floor (Living, Kitchen & Utility)', strain: 135, vibe: 0.011, temp: '23.4 °C', load: '780 kg' };

    createSolidBox(gfGroup, 0, 1.75, -7.8, 19.6, 2.5, 0.4, 0x475569, 'GF_Rear_Wall');
    createSolidBox(gfGroup, -9.6, 1.75, 0, 0.4, 2.5, 15.2, 0x475569, 'GF_Left_Wall');
    createSolidBox(gfGroup, 9.6, 1.75, 0, 0.4, 2.5, 15.2, 0x475569, 'GF_Right_Wall');
    createSolidBox(gfGroup, 1, 1.75, 0, 0.3, 2.5, 15, 0x334155, 'GF_Partition_Wall');

    // Living Room Sofa & Dining
    const sofa = createSolidBox(gfGroup, -4.5, 0.9, -3.5, 3.5, 0.8, 1.6, 0x0369a1, 'Living_Room_Sofa');
    const dining = createSolidBox(gfGroup, -4.5, 0.9, 2, 2.2, 0.85, 1.4, 0x78350f, 'Dining_Table');
    const kitchen = createSolidBox(gfGroup, 5.5, 0.9, -5.5, 4.5, 0.9, 1.4, 0x0f172a, 'Kitchen_Counter');

    // Staircase
    const stair = createSolidBox(gfGroup, -1.5, 1.75, 5, 1.6, 2.5, 3.5, 0x64748b, 'Staircase_Core');
    stair.rotation.x = -0.3;

    houseGroup.add(gfGroup);

    const ffGroup = new THREE.Group();
    ffGroup.name = 'Zone_FF_Bedrooms';
    ffGroup.userData = { explodeOffset: 3.5, zoneIndex: 2, name: '1st Floor (Master & Guest Suites)', strain: 185, vibe: 0.015, temp: '22.8 °C', load: '450 kg' };

    createSolidBox(ffGroup, 0, 3.2, 0, 20, 0.4, 16, 0x1e293b, 'FF_Slab');
    createSolidBox(ffGroup, 0, 4.6, -7.8, 19.6, 2.4, 0.4, 0x475569, 'FF_Rear_Wall');
    createSolidBox(ffGroup, -9.6, 4.6, 0, 0.4, 2.4, 15.2, 0x475569, 'FF_Left_Wall');
    createSolidBox(ffGroup, 9.6, 4.6, 0, 0.4, 2.4, 15.2, 0x475569, 'FF_Right_Wall');
    
    // Beds
    createSolidBox(ffGroup, -5, 3.7, -4, 2.5, 0.6, 2.6, 0x0284c7, 'Master_Bed');
    createSolidBox(ffGroup, 5, 3.7, -4, 2.2, 0.6, 2.4, 0x34d399, 'Guest_Bed');

    houseGroup.add(ffGroup);

    const roofGroup = new THREE.Group();
    roofGroup.name = 'Zone_Roof_Utilities';
    roofGroup.userData = { explodeOffset: 7.0, zoneIndex: 3, name: 'Terrace, Water Tank & Solar', strain: 85, vibe: 0.007, temp: '26.8 °C', load: '620 kg' };

    createSolidBox(roofGroup, 0, 5.9, 0, 20.4, 0.4, 16.4, 0x0f172a, 'Roof_Terrace_Slab');
    
    // Water Tank
    const waterTank = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 2.2, 16), new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.3 }));
    waterTank.position.set(-6, 7.2, 4); waterTank.name = 'Overhead_Water_Tank';
    roofGroup.add(waterTank);

    // Solar PV Array
    const solar = createSolidBox(roofGroup, 0, 6.4, -2, 6, 0.1, 4, 0x1e1b4b, 'Rooftop_Solar_Array');
    solar.rotation.x = -0.25;

    houseGroup.add(roofGroup);

    addIoTNode(gfGroup, -9, 1, 6, 'SN-2BHK-GF', 'Living Room Strain Node');
    addIoTNode(ffGroup, 9, 3.8, -6, 'SN-2BHK-FF', 'Master Bedroom Deflection Node');
  }

  // 2. 🏰 LUXURY VILLA MODEL
  function createLuxuryVillaModel() {
    const villaGroup = activeStructureGroup;
    createSolidBox(villaGroup, 0, 0.2, 0, 38, 0.4, 30, 0x14532d, 'Villa_Landscaped_Site');

    // Pool & Deck
    createSolidBox(villaGroup, 11, 0.5, 6, 12, 0.2, 8, 0x78350f, 'Pool_Deck');
    const pool = new THREE.Mesh(new THREE.BoxGeometry(10, 0.1, 6), new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.85, roughness: 0.1 }));
    pool.position.set(11, 0.55, 6); pool.name = 'Villa_Swimming_Pool';
    villaGroup.add(pool);

    const mainVilla = new THREE.Group();
    mainVilla.name = 'Zone_Villa_Main';
    mainVilla.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Main Residence & Pavilion', strain: 115, vibe: 0.009, temp: '22.1 °C', load: '1.2 Tons' };

    createSolidBox(mainVilla, -5, 0.65, -2, 20, 0.5, 16, 0x1e293b, 'Villa_GF_Slab');
    createSolidBox(mainVilla, -5, 2.5, -2, 19.6, 3.2, 15.6, 0x334155, 'Villa_GF_Walls');
    villaGroup.add(mainVilla);

    addIoTNode(mainVilla, -5, 1, -2, 'SN-VILLA-GF', 'Villa Foundation Strain Node');
  }

  // 3. 🏢 COMMERCIAL OFFICE TOWER MODEL
  function createCommercialTowerModel() {
    const towerGroup = activeStructureGroup;
    const floorHeight = 3.6;

    // Concrete Core
    const core = createSolidBox(towerGroup, 0, (5 * floorHeight) / 2, 0, 4.5, 6 * floorHeight, 4.5, 0x334155, 'Elevator_Core_Shaft');

    for (let i = 0; i < 5; i++) {
      const flGroup = new THREE.Group();
      const y = i * floorHeight;
      flGroup.userData = { explodeOffset: i * 2.2, zoneIndex: i + 1, name: `Floor 0${i+1} Office Workstations`, strain: 200 + i * 40, vibe: 0.018 + i * 0.004, temp: `${(21.5 + i*0.4).toFixed(1)} °C`, load: `${160 - i*15} Pax` };

      createSolidBox(flGroup, 0, y, 0, 16, 0.4, 12, 0x1e293b, `Floor_0${i+1}_Slab`);
      
      // Steel Columns
      [[-7, -5], [7, -5], [-7, 5], [7, 5]].forEach(pos => {
        createSolidBox(flGroup, pos[0], y + floorHeight / 2, pos[1], 0.6, floorHeight - 0.4, 0.6, 0x475569, `Steel_Column`);
      });

      addIoTNode(flGroup, 7.5, y + 0.6, 5.5, `SN-TOWER-F${i+1}`, `Floor 0${i+1} Column Sensor`);
      towerGroup.add(flGroup);
    }
  }

  // 4. 🛍️ SHOPPING MALL MODEL
  function createShoppingMallModel() {
    const mallGroup = activeStructureGroup;
    const mallZone = new THREE.Group();
    mallZone.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Level 1 Anchor Showrooms & Food Court', strain: 150, vibe: 0.016, temp: '21.8 °C', load: '450 Pax' };

    createSolidBox(mallZone, 0, 0.2, 0, 28, 0.4, 18, 0x1e293b, 'Mall_Base_Slab');
    createSolidBox(mallZone, 0, 2.2, 0, 27.6, 3.6, 17.6, 0x475569, 'Retail_Showrooms');
    mallGroup.add(mallZone);

    addIoTNode(mallZone, -12, 2, 7, 'SN-MALL-L1', 'Atrium Load Cell');
  }

  // 5. 🏭 INDUSTRIAL WAREHOUSE & TOWER CRANE MODEL
  function createIndustrialWarehouseModel() {
    const whGroup = activeStructureGroup;
    const mainZone = new THREE.Group();
    mainZone.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Logistics Bay & High-Bay Racking', strain: 165, vibe: 0.024, temp: '20.8 °C', load: '18.5 Tons' };

    createSolidBox(mainZone, 0, 0.2, 0, 26, 0.4, 18, 0x1e293b, 'Warehouse_Pad');
    
    // Racks
    for (let r = -5; r <= 5; r += 5) {
      createSolidBox(mainZone, r, 2.7, 0, 1.2, 5, 12, 0xd97706, `Storage_Rack_${r}`);
    }
    whGroup.add(mainZone);

    // Construction Tower Crane
    const craneGroup = new THREE.Group();
    craneGroup.position.set(16, 0, 0);
    createSolidBox(craneGroup, 0, 0.6, 0, 4, 1.2, 4, 0x334155, 'Crane_Base');
    
    // Crane Mast
    const mast = createSolidBox(craneGroup, 0, 9.2, 0, 1.0, 16, 1.0, 0xf59e0b, 'Crane_Mast');
    mast.material.wireframe = true;

    // Crane Jib
    const jibGroup = new THREE.Group();
    jibGroup.position.y = 18;
    createSolidBox(jibGroup, -6, 0, 0, 16, 0.8, 0.8, 0xf59e0b, 'Crane_Jib_Arm');
    craneGroup.add(jibGroup);

    whGroup.add(craneGroup);
    animatedParts.push({ obj: jibGroup, type: 'crane' });

    addIoTNode(whGroup, 16, 18, 0, 'SN-CRANE-TENSION', 'Crane Jib Tension Sensor');
  }

  // 6. 💻 DATA CENTER FACILITY MODEL
  function createDataCenterModel() {
    const dcGroup = activeStructureGroup;
    const hall = new THREE.Group();
    hall.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Server Hall & CRAH Chillers', strain: 110, vibe: 0.012, temp: '19.2 °C', load: '1.4 MW' };

    createSolidBox(hall, 0, 0.25, 0, 24, 0.5, 16, 0x0f172a, 'Raised_Floor_Slab');
    
    // Server Racks
    for (let x = -8; x <= 8; x += 4) {
      for (let z = -5; z <= 5; z += 2.5) {
        createSolidBox(hall, x, 1.8, z, 1.0, 2.6, 1.8, 0x1e293b, 'Server_Cabinet');
      }
    }
    dcGroup.add(hall);
    addIoTNode(hall, 0, 1.8, 0, 'SN-DC-TEMP', 'Aisle Thermal Node');
  }

  // 7. 🛣️ SMART HIGHWAY INFRASTRUCTURE MODEL
  function createHighwayInfrastructureModel() {
    const hwGroup = activeStructureGroup;
    const hwZone = new THREE.Group();
    hwZone.userData = { explodeOffset: 0, zoneIndex: 1, name: '4-Lane Highway & Signage Gantry', strain: 220, vibe: 0.035, temp: '27.4 °C', load: '68 Veh/min' };

    createSolidBox(hwZone, 0, 0.2, 0, 45, 0.4, 14, 0x1e293b, 'Asphalt_Roadbed');
    createSolidBox(hwZone, 0, 0.6, 0, 45, 0.8, 0.6, 0x64748b, 'Median_Barrier');

    // Moving Car
    const car = createSolidBox(hwZone, -20, 0.95, -3.5, 3, 1.1, 1.6, 0xef4444, 'Traffic_Sedan');
    animatedParts.push({ obj: car, type: 'vehicle', minX: -20, maxX: 20 });

    hwGroup.add(hwZone);
    addIoTNode(hwZone, 0, 2.7, 0, 'SN-HW-GANTRY', 'Highway Structural Strain Node');
  }

  // 8. 🌉 TRUSS HIGHWAY BRIDGE SPAN MODEL
  function createTrussBridgeModel() {
    const bridgeGroup = activeStructureGroup;
    const bridgeZone = new THREE.Group();
    bridgeZone.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Truss Superstructure & Deck', strain: 320, vibe: 0.048, temp: '20.1 °C', load: '34.2 Tons' };

    // Piers
    createSolidBox(bridgeZone, -12, -3.8, 0, 3, 8, 3, 0x334155, 'Bridge_Pier_1');
    createSolidBox(bridgeZone, 12, -3.8, 0, 3, 8, 3, 0x334155, 'Bridge_Pier_2');

    // Deck
    createSolidBox(bridgeZone, 0, 0.3, 0, 40, 0.6, 9, 0x1e293b, 'Bridge_Road_Deck');

    // Steel Warren Trusses
    for (let side = -1; side <= 1; side += 2) {
      const z = side * 4.3;
      createSolidBox(bridgeZone, 0, 7, z, 38, 0.4, 0.4, 0x0284c7, 'Top_Truss_Chord');
      for (let x = -17; x <= 17; x += 4) {
        const diag = createSolidBox(bridgeZone, x, 3.5, z, 0.3, 7.8, 0.3, 0x0284c7, 'Truss_Diagonal');
        diag.rotation.z = (x % 8 === 0) ? 0.45 : -0.45;
      }
    }

    bridgeGroup.add(bridgeZone);
    addIoTNode(bridgeZone, 0, 0.4, 4.1, 'SN-BRG-MID', 'Mid-Span Strain Gauge');
  }

  // 9. 🏨 GRAND RESORT HOTEL MODEL
  function createLuxuryHotelModel() {
    const hotelGroup = activeStructureGroup;

    // Ground Landscaped Base Pad
    createSolidBox(hotelGroup, 0, 0.2, 0, 32, 0.4, 22, 0x14532d, 'Resort_Grounds_Pad');

    // Porte-Cochère Entrance Canopy
    const canopy = createSolidBox(hotelGroup, 0, 3.2, 9, 12, 0.4, 8, 0x0284c7, 'Porte_Cochere_Canopy');
    createSolidBox(hotelGroup, -5, 1.5, 12, 0.6, 3.0, 0.6, 0x94a3b8, 'Canopy_Pillar_Left');
    createSolidBox(hotelGroup, 5, 1.5, 12, 0.6, 3.0, 0.6, 0x94a3b8, 'Canopy_Pillar_Right');

    // Ground Floor Double-Height Reception Lobby
    const lobbyGroup = new THREE.Group();
    lobbyGroup.name = 'Zone_Hotel_Lobby';
    lobbyGroup.userData = { explodeOffset: 0, zoneIndex: 1, name: 'Ground Floor Lobby & Grand Entrance', strain: 140, vibe: 0.012, temp: '22.4 °C', load: '210 Pax' };

    createSolidBox(lobbyGroup, 0, 0.6, 0, 26, 0.4, 16, 0x1e293b, 'Lobby_Base_Slab');
    createSolidBox(lobbyGroup, 0, 2.2, -7.8, 25.6, 2.8, 0.4, 0x475569, 'Lobby_Rear_Wall');
    createSolidBox(lobbyGroup, -12.8, 2.2, 0, 0.4, 2.8, 15.6, 0x475569, 'Lobby_Left_Wall');
    createSolidBox(lobbyGroup, 12.8, 2.2, 0, 0.4, 2.8, 15.6, 0x475569, 'Lobby_Right_Wall');
    hotelGroup.add(lobbyGroup);

    // 4 Guest Suite Floors
    for (let f = 1; f <= 4; f++) {
      const roomGroup = new THREE.Group();
      const y = f * 3.2;
      roomGroup.userData = { explodeOffset: f * 2.5, zoneIndex: f + 1, name: `Floor 0${f} Guest Suite Balconies`, strain: 170 + f * 20, vibe: 0.015, temp: `${(22 + f*0.3).toFixed(1)} °C`, load: `${80 - f*5} Rooms` };

      createSolidBox(roomGroup, 0, y, 0, 26, 0.4, 16, 0x0f172a, `Floor_0${f}_Slab`);
      createSolidBox(roomGroup, 0, y + 1.4, -7.8, 25.6, 2.4, 0.4, 0x475569, `Floor_0${f}_Rear_Wall`);
      createSolidBox(roomGroup, -12.8, y + 1.4, 0, 0.4, 2.4, 15.6, 0x475569, `Floor_0${f}_Left_Wall`);
      createSolidBox(roomGroup, 12.8, y + 1.4, 0, 0.4, 2.4, 15.6, 0x475569, `Floor_0${f}_Right_Wall`);

      // Glass Balcony Railings
      const balcony = new THREE.Mesh(new THREE.BoxGeometry(25.6, 0.9, 0.1), new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.45 }));
      balcony.position.set(0, y + 0.85, 7.95);
      balcony.name = `Floor_0${f}_Glass_Balcony`;
      roomGroup.add(balcony);

      hotelGroup.add(roomGroup);
    }

    // Rooftop Sky Lounge & Infinity Pool Deck
    const roofPoolGroup = new THREE.Group();
    roofPoolGroup.name = 'Zone_Rooftop_Pool';
    roofPoolGroup.userData = { explodeOffset: 12.5, zoneIndex: 6, name: 'Rooftop Infinity Pool & Sky Lounge', strain: 125, vibe: 0.010, temp: '26.1 °C', load: '12.8 Tons Water' };

    createSolidBox(roofPoolGroup, 0, 16.2, 0, 26.4, 0.4, 16.4, 0x78350f, 'Rooftop_Teak_Deck');
    
    // Infinity Pool
    const infinityPool = new THREE.Mesh(new THREE.BoxGeometry(16, 0.2, 7), new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.85, roughness: 0.1 }));
    infinityPool.position.set(0, 16.5, 2);
    infinityPool.name = 'Rooftop_Infinity_Pool';
    roofPoolGroup.add(infinityPool);

    hotelGroup.add(roofPoolGroup);

    addIoTNode(lobbyGroup, 0, 1.5, 7.5, 'SN-HOTEL-LOBBY', 'Lobby Entrance Sensor');
    addIoTNode(roofPoolGroup, 0, 16.5, 2, 'SN-HOTEL-POOL', 'Rooftop Pool Hydrostatic Sensor');
  }

  function updateUIForStructureType(type) {
    const structNames = {
      'house2bhk': '2 BHK Residential House',
      'luxuryVilla': 'Luxury Villa (Pool & Garden)',
      'officeSkyscraper': 'Commercial Office Skyscraper',
      'shoppingMall': 'Shopping Mall & Food Court',
      'industrialWarehouse': 'Warehouse & Construction Crane',
      'dataCenter': 'High-Density Data Center',
      'highwayInfrastructure': 'Smart Highway Infrastructure',
      'trussBridge': 'Truss Highway Bridge Span',
      'luxuryHotel': 'Grand Resort Hotel & Pool'
    };

    const name = structNames[type] || 'Civil Asset Twin';
    document.getElementById('nav-asset-name').innerText = name;
    document.getElementById('sidebar-struct-title').innerText = `${name} Twin`;

    const zoneSelect = document.getElementById('zone-select');
    zoneSelect.innerHTML = '<option value="all">Entire Structure (Global Assembly)</option>';

    const treeContainer = document.getElementById('bim-hierarchy-tree');
    treeContainer.innerHTML = '';

    activeStructureGroup.traverse(child => {
      if (child.userData && child.userData.zoneIndex !== undefined) {
        const opt = document.createElement('option');
        opt.value = child.userData.zoneIndex;
        opt.innerText = child.userData.name;
        zoneSelect.appendChild(opt);

        const treeNode = document.createElement('div');
        treeNode.style.cssText = 'font-size:0.78rem; padding:4px 6px; cursor:pointer; color:#cbd5e1; border-radius:4px; display:flex; justify-content:space-between; align-items:center;';
        treeNode.innerHTML = `<span><i class="fa-solid fa-layer-group text-sky-400"></i> ${child.userData.name}</span>`;
        treeNode.onclick = () => selectZoneFromDropdown(child.userData.zoneIndex);
        treeContainer.appendChild(treeNode);
      }
    });
  }

  function changeStructureType(val) {
    playTone(680);
    currentStructureType = val;
    buildStructure(val);
  }

  function setExplodeLevel(val) {
    explodeFactor = val / 100;
    applyExplodeLevel(explodeFactor);
  }

  function applyExplodeLevel(factor) {
    activeStructureGroup.traverse(child => {
      if (child.userData && child.userData.explodeOffset !== undefined) {
        child.position.y = child.userData.explodeOffset * factor * 1.5;
      }
    });
  }

  function setLayer(layer, btnElement) {
    activeLayer = layer;
    playTone(750);
    if (btnElement) {
      document.querySelectorAll('.layer-btn').forEach(b => b.classList.remove('active'));
      btnElement.classList.add('active');
    }

    activeStructureGroup.traverse(c => {
      if (c.isMesh) {
        const nameLower = c.name ? c.name.toLowerCase() : '';
        const isWallOrPartition = nameLower.includes('wall') || nameLower.includes('partition') || 
                                  nameLower.includes('core') || nameLower.includes('rear') || 
                                  nameLower.includes('left') || nameLower.includes('right') || 
                                  nameLower.includes('facade') || nameLower.includes('showroom') ||
                                  nameLower.includes('building') || nameLower.includes('suite');

        const cage = c.getObjectByName ? c.getObjectByName('RebarCage') : null;

        if (layer === 'wireframe') {
          c.material.wireframe = true;
          c.material.map = null;
          c.material.transparent = false;
          c.material.opacity = 1.0;
          if (cage) cage.visible = false;
        } else if (layer === 'rcc') {
          c.material.wireframe = false;
          c.material.map = null;
          c.material.transparent = true;
          c.material.opacity = (c.material.transmission > 0 || nameLower.includes('glass')) ? 0.2 : 0.25;
          if (c.userData && c.userData.originalColor !== undefined) {
            c.material.color.setHex(c.userData.originalColor);
          }
          if (cage) cage.visible = true;
        } else if (layer === 'bricks') {
          c.material.wireframe = false;
          if (cage) cage.visible = false;

          if (isWallOrPartition) {
            c.material.transparent = false;
            c.material.opacity = 1.0;
            c.material.map = brickTexture;
            c.material.color.setHex(0xffffff); // Allows bright clay brick texture colors to display
          } else {
            c.material.map = null;
            c.material.transparent = (c.material.transmission > 0 || nameLower.includes('glass') || nameLower.includes('pool'));
            c.material.opacity = c.material.transparent ? 0.4 : 1.0;
            if (c.userData && c.userData.originalColor !== undefined) {
              c.material.color.setHex(c.userData.originalColor);
            }
          }
        } else if (layer === 'concrete') {
          c.material.wireframe = false;
          c.material.map = null;
          if (cage) cage.visible = false;
          
          if (!nameLower.includes('glass') && !nameLower.includes('pool') && !nameLower.includes('water')) {
            c.material.transparent = false;
            c.material.opacity = 1.0;
            c.material.color.setHex(0x64748b);
          } else if (c.userData && c.userData.originalColor !== undefined) {
            c.material.color.setHex(c.userData.originalColor);
          }
        } else { // 'normal' BIM View
          c.material.wireframe = false;
          c.material.map = null;
          if (cage) cage.visible = false;

          c.material.transparent = (c.material.transmission > 0 || nameLower.includes('glass') || nameLower.includes('pool'));
          c.material.opacity = c.material.transparent ? 0.4 : 1.0;
          if (c.userData && c.userData.originalColor !== undefined) {
            c.material.color.setHex(c.userData.originalColor);
          }
        }
        c.material.needsUpdate = true;
      }
    });
  }

  function setCameraView(view) {
    playTone(520);
    if (view === 'top') camera.position.set(0, 45, 0.1);
    else if (view === 'front') camera.position.set(0, 15, 45);
    else camera.position.set(28, 22, 32);
    controls.update();
  }

  let isOscillating = false;
  let windForce = 0.012;
  let animTime = 0;

  function toggleSeismicOscillation() {
    isOscillating = !isOscillating;
    const btn = document.getElementById('seismic-toggle-btn');
    if (isOscillating) {
      if (btn) btn.innerHTML = '<i class="fa-solid fa-house-crack"></i> Stop Seismic';
      document.getElementById('ai-status').className = 'status-badge alert';
      document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-house-crack"></i> Seismic Shock Active';
      document.getElementById('vibe-val').innerText = '0.418 g (Critical)';
      document.getElementById('strain-val').innerText = '485 µε';
      document.getElementById('ai-insight').innerText = 'AI Shock Alert: Multi-axis ground motion exceeding peak acceleration threshold.';
      startEmergencySiren();
    } else {
      if (btn) btn.innerHTML = '<i class="fa-solid fa-house-crack"></i> Seismic Test';
      document.getElementById('ai-status').className = 'status-badge';
      document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-circle-check"></i> AI Nominal';
      document.getElementById('vibe-val').innerText = '0.018 g';
      document.getElementById('strain-val').innerText = '180 µε';
      stopEmergencySiren();
    }
  }

  function toggleFloodSimulation() {
    isFloodActive = !isFloodActive;
    const btn = document.getElementById('flood-toggle-btn');
    if (isFloodActive) {
      floodMesh.visible = true;
      if (btn) btn.innerHTML = '<i class="fa-solid fa-water"></i> Drain Flood';
      document.getElementById('ai-status').className = 'status-badge warning';
      document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-water"></i> Flood Warning';
      document.getElementById('ai-insight').innerText = 'Hydrostatic surge detected around foundation footings.';
    } else {
      if (btn) btn.innerHTML = '<i class="fa-solid fa-water"></i> Flood Rise';
      document.getElementById('ai-status').className = 'status-badge';
      document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-circle-check"></i> AI Nominal';
    }
  }

  function toggleHeatwaveSimulation() {
    isHeatwaveActive = !isHeatwaveActive;
    const btn = document.getElementById('heat-toggle-btn');
    if (isHeatwaveActive) {
      if (btn) btn.innerHTML = '<i class="fa-solid fa-sun"></i> Cool Down';
      document.getElementById('temp-val').innerText = '48.5 °C (Extreme)';
      document.getElementById('strain-val').innerText = '540 µε';
      document.getElementById('ai-status').className = 'status-badge warning';
      document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-sun"></i> Thermal Alert';
      document.getElementById('ai-insight').innerText = 'Thermal expansion stress detected across solar-exposed structural facade.';
    } else {
      if (btn) btn.innerHTML = '<i class="fa-solid fa-sun"></i> Heatwave Stress';
      document.getElementById('temp-val').innerText = '23.1 °C';
      document.getElementById('strain-val').innerText = '180 µε';
      document.getElementById('ai-status').className = 'status-badge';
      document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-circle-check"></i> AI Nominal';
    }
  }

  function turnOffAllSimulations() {
    isOscillating = false;
    isFloodActive = false;
    isHeatwaveActive = false;
    windForce = 0.012;
    floodWaterLevel = -10.0;
    floodMesh.visible = false;
    floodMesh.position.y = -10.0;

    const sBtn = document.getElementById('seismic-toggle-btn'); if (sBtn) sBtn.innerHTML = '<i class="fa-solid fa-house-crack"></i> Seismic Test';
    const fBtn = document.getElementById('flood-toggle-btn'); if (fBtn) fBtn.innerHTML = '<i class="fa-solid fa-water"></i> Flood Rise';
    const hBtn = document.getElementById('heat-toggle-btn'); if (hBtn) hBtn.innerHTML = '<i class="fa-solid fa-sun"></i> Heatwave Stress';
    const wSlider = document.getElementById('wind-slider'); if (wSlider) wSlider.value = 12;
    const wLbl = document.getElementById('wind-lbl'); if (wLbl) wLbl.innerText = '12% (30 km/h)';

    document.getElementById('ai-status').className = 'status-badge';
    document.getElementById('ai-status').innerHTML = '<i class="fa-solid fa-circle-check"></i> AI Nominal';
    document.getElementById('health-score').innerText = '99.1%';
    document.getElementById('health-bar').style.width = '99.1%';
    document.getElementById('strain-val').innerText = '180 µε';
    document.getElementById('vibe-val').innerText = '0.018 g';
    document.getElementById('temp-val').innerText = '23.1 °C';
    document.getElementById('ai-insight').innerText = 'Structure displays linear elastic response within safe IS 456 stress envelopes.';
    stopEmergencySiren();
  }

  function updateWindLoad(val) {
    windForce = (val / 100) * 0.15;
    document.getElementById('wind-lbl').innerText = `${val}% (${(val*2.5).toFixed(0)} km/h)`;
  }

  const strainCanvas = document.getElementById('strainChart');
  const strainCtx = strainCanvas.getContext('2d');
  const strainData = Array(30).fill(180);

  const fftCanvas = document.getElementById('fftChart');
  const fftCtx = fftCanvas.getContext('2d');
  const fftData = Array(30).fill(0.018);

  function resizeCanvas(canvas) {
    if (canvas && canvas.parentElement) {
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
    }
  }

  function drawCharts() {
    resizeCanvas(strainCanvas);
    resizeCanvas(fftCanvas);

    if (strainCtx) {
      strainCtx.clearRect(0, 0, strainCanvas.width, strainCanvas.height);
      strainCtx.beginPath(); strainCtx.strokeStyle = '#38bdf8'; strainCtx.lineWidth = 2;
      const step = strainCanvas.width / (strainData.length - 1);
      strainData.forEach((val, idx) => {
        const y = strainCanvas.height - ((val - 50) / 550) * strainCanvas.height;
        if (idx === 0) strainCtx.moveTo(0, y); else strainCtx.lineTo(idx * step, y);
      });
      strainCtx.stroke();
    }

    if (fftCtx) {
      fftCtx.clearRect(0, 0, fftCanvas.width, fftCanvas.height);
      fftCtx.beginPath(); fftCtx.strokeStyle = '#34d399'; fftCtx.lineWidth = 2;
      const step = fftCanvas.width / (fftData.length - 1);
      fftData.forEach((val, idx) => {
        const y = fftCanvas.height - (val / 0.5) * fftCanvas.height;
        if (idx === 0) fftCtx.moveTo(0, y); else fftCtx.lineTo(idx * step, y);
      });
      fftCtx.stroke();
    }
  }

  function pushTelemetryData(strainVal, vibeVal) {
    strainData.shift(); strainData.push(strainVal);
    fftData.shift(); fftData.push(vibeVal);
    drawCharts();
  }

  function animate() {
    requestAnimationFrame(animate);
    animTime += 0.04;

    activeStructureGroup.traverse((c) => {
      const cage = c.getObjectByName && c.getObjectByName('RebarCage');
      if (cage && cage.visible) {
        cage.children.forEach((child, idx) => {
          if (child.children && child.children.length > 0) {
            child.children.forEach(s => {
              if (s.material) s.material.emissive = new THREE.Color(0xf59e0b).multiplyScalar(0.4 + 0.3 * Math.sin(animTime * 5 + idx));
            });
          }
        });
      }
    });

    if (isFloodActive) {
      floodMesh.visible = true;
      if (floodWaterLevel < 2.2) floodWaterLevel += 0.015;
    } else {
      if (floodWaterLevel > -10.0) floodWaterLevel -= 0.05;
      if (floodWaterLevel <= -9.5) floodMesh.visible = false;
    }
    if (floodMesh.visible) {
      floodMesh.position.y = floodWaterLevel + Math.sin(animTime * 2) * 0.08;
    }

    if (isOscillating) {
      grid.position.x = Math.sin(animTime * 12) * 0.15;
      grid.position.z = Math.cos(animTime * 10) * 0.15;
    } else {
      grid.position.x = 0;
      grid.position.z = 0;
    }

    animatedParts.forEach(item => {
      if (item.type === 'vehicle') {
        item.obj.position.x += 0.14;
        if (item.obj.position.x > item.maxX) item.obj.position.x = item.minX;
      } else if (item.type === 'crane') {
        item.obj.rotation.y = Math.sin(animTime * 0.4) * 0.8;
      }
    });

    activeStructureGroup.traverse((c) => {
      if (c.userData && c.userData.zoneIndex) {
        const idx = c.userData.zoneIndex;
        let sway = Math.sin(animTime * 1.5 + idx * 0.4) * windForce * idx;
        if (isOscillating) sway += Math.sin(animTime * 7 + idx * 0.8) * (0.12 * idx);
        c.position.x = sway;
      }
    });

    if (Math.random() < 0.2) {
      const currentStrain = isHeatwaveActive ? 540 + Math.random() * 20 : (isOscillating ? 485 + Math.random() * 40 : 180 + (Math.random() * 12 - 6));
      const currentVibe = isOscillating ? 0.418 + Math.random() * 0.08 : 0.018 + Math.random() * 0.004;
      pushTelemetryData(currentStrain, currentVibe);
    }

    controls.update();
    renderer.render(scene, camera);
  }

  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  window.addEventListener('mousemove', (e) => {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / container.clientWidth) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / container.clientHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
      const obj = intersects[0].object;
      if (obj.name.startsWith('SensorNode_') || obj.name.startsWith('Zone_') || obj.userData.zoneIndex) {
        tooltip.style.display = 'block';
        tooltip.style.left = e.clientX + 12 + 'px';
        tooltip.style.top = e.clientY + 12 + 'px';
        tooltip.innerHTML = `<strong>${obj.name.replace(/_/g, ' ')}</strong><br/><small>Click to inspect telemetry</small>`;
        document.body.style.cursor = 'pointer';
        return;
      }
    }
    tooltip.style.display = 'none';
    document.body.style.cursor = 'default';
  });

  window.addEventListener('click', () => {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);
    if (intersects.length > 0) {
      const hitObj = intersects[0].object;
      if (hitObj.name.startsWith('SensorNode_')) {
        openModal(hitObj.userData, hitObj.name);
        playTone(880);
      }
    }
  });

  function selectZoneFromDropdown(val) {
    playTone(500);
    const zoneSelect = document.getElementById('zone-select');
    zoneSelect.value = val;

    if (val === 'all') {
      document.getElementById('zone-name').innerText = 'Entire Structure';
      document.getElementById('strain-val').innerText = '180 µε';
      document.getElementById('vibe-val').innerText = '0.018 g';
      document.getElementById('temp-val').innerText = '23.1 °C';
      document.getElementById('occ-val').innerText = '650 kg';
    } else {
      activeStructureGroup.traverse(child => {
        if (child.userData && child.userData.zoneIndex === parseInt(val)) {
          const d = child.userData;
          document.getElementById('zone-name').innerText = d.name;
          document.getElementById('strain-val').innerText = `${d.strain} µε`;
          document.getElementById('vibe-val').innerText = `${d.vibe} g`;
          document.getElementById('temp-val').innerText = `${d.temp}`;
          document.getElementById('occ-val').innerText = `${d.load}`;
          pushTelemetryData(d.strain, d.vibe);
        }
      });
    }
  }

  function openModal(data, name) {
    document.getElementById('modal-id').innerText = data.id || 'SN-NOD-001';
    document.getElementById('modal-title').innerText = `Sensor Diagnostics (${data.desc || name})`;
    document.getElementById('modal-overlay').style.display = 'flex';
  }

  function closeModal() {
    document.getElementById('modal-overlay').style.display = 'none';
  }

  function generateAIReport() {
    playTone(900);
    const reportText = `CIVIL DIGITAL TWIN AUDIT REPORT\n=========================================\nStructure: ${document.getElementById('nav-asset-name').innerText}\nHealth Score: ${document.getElementById('health-score').innerText}\nStatus: ${document.getElementById('ai-status').innerText}\nMicrostrain: ${document.getElementById('strain-val').innerText}\nPeak Acceleration: ${document.getElementById('vibe-val').innerText}\nTimestamp: ${new Date().toISOString()}\n\nAudit Statement: Structural load path verified against IS 456 / Eurocode safety standards.`;
    const blob = new Blob([reportText], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `BIM_Audit_${currentStructureType}_${Date.now()}.txt`;
    link.click();
  }

  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
    drawCharts();
  });

  window.onload = function() {
    buildStructure('house2bhk');
    drawCharts();
    animate();
  };
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
