import streamlit as st
import time
import cv2
import numpy as np
from PIL import Image
import plotly.graph_objects as go

# =========================================================
# 1. PAGE CONFIGURATION & DARK THEME
# =========================================================
st.set_page_config(
    page_title="Real-Time AI Construction Inspection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .badge-critical { background-color: #DA3633; color: white; padding: 3px 8px; border-radius: 10px; font-weight: bold; }
    .badge-warning { background-color: #D97706; color: white; padding: 3px 8px; border-radius: 10px; font-weight: bold; }
    .badge-low { background-color: #238636; color: white; padding: 3px 8px; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. REAL OPENCV DEFECT DETECTION ENGINE
# =========================================================
def analyze_real_image(pil_image, sensitivity_threshold=100, min_area=300):
    """
    Performs real pixel analysis using OpenCV to find actual structural anomalies:
    - Cracks/Gaps: Using Canny Edge Detection & Contours
    - Moisture/Stains: Using Color & Intensity Thresholding
    """
    # Convert PIL Image to OpenCV format (BGR)
    img_np = np.array(pil_image.convert("RGB"))
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    annotated_cv = img_cv.copy()
    
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    defects = []
    
    # -----------------------------------------------------
    # A. REAL CRACK & LINE DEFECT DETECTION (Canny Edge)
    # -----------------------------------------------------
    # Sensitivity adjusts threshold limits
    low_thresh = int(sensitivity_threshold * 0.5)
    high_thresh = int(sensitivity_threshold * 1.5)
    edges = cv2.Canny(blurred, low_thresh, high_thresh)
    
    # Dilate edges to connect broken crack contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    crack_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Filter out non-crack shapes (cracks are usually elongated or branched)
            if aspect_ratio > 1.2 or aspect_ratio < 0.8 or area > 1000:
                crack_count += 1
                defect_id = f"Crack #{crack_count}"
                
                # Draw RED Bounding Box & Label
                cv2.rectangle(annotated_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(annotated_cv, (x, max(0, y - 25)), (x + 180, y), (0, 0, 255), -1)
                cv2.putText(annotated_cv, f"CRACK ({int(area)}px)", (x + 5, max(15, y - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                defects.append({
                    "type": "Structural Crack / Gap",
                    "bbox": [x, y, w, h],
                    "area_px": area,
                    "severity": "CRITICAL" if area > 1200 else "MODERATE",
                    "confidence": f"{min(98.5, 80.0 + (area / 100)):.1f}%"
                })

    # -----------------------------------------------------
    # B. REAL DAMPNESS / STAIN DETECTION (Color Threshold)
    # -----------------------------------------------------
    # Detect abnormally dark/discolored patches
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 21, 5)
    
    damp_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    leak_count = 0
    for cnt in damp_contours:
        area = cv2.contourArea(cnt)
        # Look for large, patchy discolored surfaces
        if area > (min_area * 3):
            x, y, w, h = cv2.boundingRect(cnt)
            # Avoid duplicating already marked crack boxes
            already_marked = any(abs(x - d["bbox"][0]) < 20 and abs(y - d["bbox"][1]) < 20 for d in defects)
            
            if not already_marked and leak_count < 3:
                leak_count += 1
                
                # Draw AMBER Bounding Box
                cv2.rectangle(annotated_cv, (x, y), (x + w, y + h), (0, 165, 255), 2)
                cv2.rectangle(annotated_cv, (x, max(0, y - 25)), (x + 180, y), (0, 165, 255), -1)
                cv2.putText(annotated_cv, "LEAKAGE / STAIN", (x + 5, max(15, y - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                defects.append({
                    "type": "Moisture / Discoloration",
                    "bbox": [x, y, w, h],
                    "area_px": area,
                    "severity": "MODERATE",
                    "confidence": f"{min(94.0, 75.0 + (area / 200)):.1f}%"
                })

    # Convert annotated image back to PIL
    result_pil = Image.fromarray(cv2.cvtColor(annotated_cv, cv2.COLOR_BGR2RGB))
    return result_pil, defects

# =========================================================
# 3. DYNAMIC 3D TWIN GENERATOR (BASED ON REAL DEFECTS)
# =========================================================
def generate_dynamic_3d_twin(defects, img_width, img_height):
    """Maps actual detected bounding boxes into 3D spatial points on the building model."""
    
    # 3D Building Box Framework
    x_wire = [0, 10, 10, 0, 0, 0, 10, 10, 0, 0, 10, 10, 10, 10, 0, 0]
    y_wire = [0, 0, 10, 10, 0, 0, 0, 10, 10, 0, 0, 0, 10, 10, 10, 10]
    z_wire = [0, 0, 0, 0, 0, 12, 12, 12, 12, 12, 0, 12, 12, 0, 0, 12]
    
    fig = go.Figure()
    
    # Structural Wireframe
    fig.add_trace(go.Scatter3d(
        x=x_wire, y=y_wire, z=z_wire,
        mode='lines',
        line=dict(color='#30363D', width=5),
        name='BIM Skeleton'
    ))
    
    # Map pixel X, Y coords into 3D Spatial X, Z coords
    d_x, d_y, d_z, d_labels, d_colors = [], [], [], [], []
    
    for d in defects:
        bx, by, bw, bh = d["bbox"]
        
        # Scale image coordinates into 3D space (0 to 10m wide, 0 to 12m high)
        norm_x = (bx + bw / 2) / img_width * 10.0
        norm_z = (1.0 - (by + bh / 2) / img_height) * 12.0
        norm_y = 0.0 # Mapped on front facade
        
        d_x.append(norm_x)
        d_y.append(norm_y)
        d_z.append(norm_z)
        d_labels.append(f"{d['type']} ({d['severity']})")
        d_colors.append("#DA3633" if d['severity'] == "CRITICAL" else "#D97706")
        
    if d_x:
        fig.add_trace(go.Scatter3d(
            x=d_x, y=d_y, z=d_z,
            mode='markers+text',
            marker=dict(size=10, color=d_colors, symbol='diamond'),
            text=d_labels,
            textposition="top center",
            name='Mapped Defects'
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X (m)', backgroundcolor='#0E1117', gridcolor='#21262D'),
            yaxis=dict(title='Y (m)', backgroundcolor='#0E1117', gridcolor='#21262D'),
            zaxis=dict(title='Z (Height m)', backgroundcolor='#0E1117', gridcolor='#21262D'),
        ),
        paper_bgcolor='#0E1117',
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# =========================================================
# 4. APP INTERFACE & WORKFLOW
# =========================================================
st.title("🤖 Real Computer Vision Inspection & 3D Twin")
st.caption("Upload any building image for live pixel-level anomaly, crack, and discolored region detection.")
st.divider()

# Sidebar Controls
st.sidebar.title("🎛️ Vision Fine-Tuning")
sensitivity = st.sidebar.slider("Detection Sensitivity (Lower = More Sensitive)", 30, 200, 90)
min_size = st.sidebar.slider("Minimum Defect Size (Pixels)", 100, 2000, 300)

uploaded_file = st.file_uploader("📷 Upload Real Building / Structural Wall Image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file)
    w, h = raw_img.size
    
    with st.spinner("🔬 Scanning image pixels with computer vision algorithms..."):
        annotated_img, detected_defects = analyze_real_image(raw_img, sensitivity, min_size)
    
    t1, t2, t3 = st.tabs(["📸 Live Pixel Detection", "🌐 Real-Time 3D Twin Map", "📋 Defect & Cost Report"])
    
    # ---------------------------------------------------------
    # TAB 1: REAL PIXEL DETECTION OVERLAY
    # ---------------------------------------------------------
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 1. Original Uploaded Image")
            st.image(raw_img, use_container_width=True)
            
        with c2:
            st.markdown(f"##### 2. Dynamic CV Detection ({len(detected_defects)} Found)")
            st.image(annotated_img, use_container_width=True)
            
        if not detected_defects:
            st.success("🎉 No structural anomalies detected at current sensitivity levels! Try lowering the sensitivity threshold in the sidebar if defects were missed.")

    # ---------------------------------------------------------
    # TAB 2: SPATIAL 3D TWIN
    # ---------------------------------------------------------
    with t2:
        st.subheader("🌐 Mapped 3D Spatial Digital Twin")
        twin_fig = generate_dynamic_3d_twin(detected_defects, w, h)
        st.plotly_chart(twin_fig, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 3: DYNAMIC REPORT
    # ---------------------------------------------------------
    with t3:
        st.subheader("📋 Detected Defect Log & Costing")
        
        if detected_defects:
            report_rows = []
            total_repair_cost = 0
            
            for idx, d in enumerate(detected_defects, 1):
                cost = 15000 if d["severity"] == "CRITICAL" else 6000
                total_repair_cost += cost
                
                report_rows.append({
                    "Defect #": idx,
                    "Category": d["type"],
                    "Bounding Box (X, Y, W, H)": str(d["bbox"]),
                    "Affected Area": f"{int(d['area_px'])} sq px",
                    "Severity": d["severity"],
                    "Est Cost (₹)": f"₹ {cost:,}"
                })
                
            st.table(report_rows)
            st.metric("💰 Estimated Total Repair Cost", f"₹ {total_repair_cost:,}")
        else:
            st.info("No defects logged for report generation.")

            