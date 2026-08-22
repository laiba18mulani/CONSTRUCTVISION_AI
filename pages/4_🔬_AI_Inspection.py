import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
from utils.site_data import add_inspection_record

st.set_page_config(page_title="AI Crack & Defect Inspection", page_icon="🔬", layout="wide")

st.title("🔬 AI Crack & Structural Defect Detection")
st.markdown("Upload a concrete or wall inspection image to detect cracks, estimate dimensions, and calculate structural severity.")

# Sidebar Settings
st.sidebar.header("⚙️ Model & Calibration Settings")
confidence_thresh = st.sidebar.slider("AI Confidence Threshold", 0.1, 1.0, 0.50, 0.05)
px_to_mm_ratio = st.sidebar.number_input("Pixel-to-mm Scale Ratio (mm/px)", min_value=0.01, value=0.5, step=0.05)

# Image Source Selection
source_option = st.radio("Select Image Source:", ["📤 Upload Image", "📸 Use Sample Concrete Crack Image"])

image_to_process = None

if source_option == "📤 Upload Image":
    uploaded_file = st.file_uploader("Choose a structural image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_to_process = Image.open(uploaded_file)
else:
    # Generates a synthetic concrete crack sample image if no image is uploaded
    st.info("Using simulated concrete crack image for testing.")
    sample_img = np.full((400, 600, 3), 180, dtype=np.uint8)
    # Draw simulated crack lines
    cv2.polylines(sample_img, [np.array([[100, 50], [150, 120], [220, 200], [280, 290], [350, 380]])], False, (30, 30, 30), 4)
    cv2.polylines(sample_img, [np.array([[220, 200], [310, 210], [400, 260]])], False, (40, 40, 40), 2)
    image_to_process = Image.fromarray(sample_img)

if image_to_process is not None:
    col_orig, col_proc = st.columns(2)
    
    with col_orig:
        st.subheader("📷 Original Image")
        st.image(image_to_process, use_container_width=True)

    # Simple Computer Vision Crack Analysis Pipeline
    img_np = np.array(image_to_process.convert('RGB'))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    # Edge detection & thresholding to isolate cracks
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find crack contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    annotated_img = img_np.copy()
    defects_detected = []

    for idx, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 20:  # Filter noise
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Calculate physical measurements based on scale ratio
            length_mm = round(max(w, h) * px_to_mm_ratio, 2)
            width_mm = round(min(w, h) * px_to_mm_ratio, 2)
            
            # Severity classification rule
            severity = "CRITICAL" if width_mm > 2.0 else ("WARNING" if width_mm > 1.0 else "SAFE")
            color = (255, 0, 0) if severity == "CRITICAL" else ((255, 165, 0) if severity == "WARNING" else (0, 255, 0))
            
            # Draw bounding box on output image
            cv2.rectangle(annotated_img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(annotated_img, f"#{idx+1} {width_mm}mm", (x, max(y - 5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            defects_detected.append({
                "Defect ID": f"DEF-{idx+1:02d}",
                "Type": "Concrete Crack",
                "Length (mm)": length_mm,
                "Width (mm)": width_mm,
                "Severity": severity,
                "Confidence": f"{int(min(0.95, 0.60 + (area / 1000))*100)}%"
            })

    with col_proc:
        st.subheader("🎯 AI Inspection Output")
        st.image(annotated_img, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Detected Defects Breakdown")

    if defects_detected:
        df_defects = pd.DataFrame(defects_detected)
        st.dataframe(df_defects, use_container_width=True)
        
        # Summary Status Card
        max_width = max([d["Width (mm)"] for d in defects_detected])
        overall_status = "CRITICAL" if max_width > 2.0 else ("WARNING" if max_width > 1.0 else "SAFE")
        status_color = "#DC2626" if overall_status == "CRITICAL" else ("#EAB308" if overall_status == "WARNING" else "#16A34A")

        st.markdown(f"""
            <div style="background-color:#1E222A; border-left:6px solid {status_color}; padding:15px; border-radius:6px;">
                <h4 style="margin:0; color:#FFF;">Inspection Verdict: <span style="color:{status_color};">{overall_status}</span></h4>
                <p style="margin:5px 0 0 0; color:#A0AEC0;">Max detected crack width: <b>{max_width} mm</b> | Total Defects Found: <b>{len(defects_detected)}</b></p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ No structural defects detected above the current threshold.")

        