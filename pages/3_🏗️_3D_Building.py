import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import time

# ---------------------------------------------------------
# 1. Page Title & Layout
# ---------------------------------------------------------
st.set_page_config(page_title="Residential Structural Health Monitoring", layout="wide", page_icon="🏗️")

st.title("🏗️ Chatake Innoworks: AI Structural Analysis")
st.write("Upload site photos to automatically generate a 3D digital twin and monitor real-time component stress.")

# ---------------------------------------------------------
# 2. Sidebar Controls (Simulates Weather & Earthquakes)
# ---------------------------------------------------------
st.sidebar.header("🌍 Simulated Environment")
wind = st.sidebar.slider("Wind Speed (km/h)", 0, 200, 30)
seismic = st.sidebar.slider("Seismic Activity (Richter)", 0.0, 8.0, 1.0, step=0.1)
temp = st.sidebar.slider("Temperature (°C)", -10, 50, 28)

st.sidebar.header("🤖 AI System")
self_healing = st.sidebar.toggle("Activate Smart Concrete Healing")

# ---------------------------------------------------------
# 3. Dynamic Sensor Generation Logic
# ---------------------------------------------------------
def generate_sensor_dataframe():
    components_data = [
        {"Name": "Foundation", "Type": "Concrete", "X": 5, "Y": 5, "Z": 0, "Base_Stress": 12},
        {"Name": "Footing", "Type": "RCC", "X": 2, "Y": 2, "Z": 1, "Base_Stress": 10},
        {"Name": "Column 1", "Type": "RCC", "X": 2, "Y": 2, "Z": 4, "Base_Stress": 15},
        {"Name": "Column 2", "Type": "RCC", "X": 8, "Y": 8, "Z": 4, "Base_Stress": 15},
        {"Name": "Brick Wall", "Type": "Bricks", "X": 5, "Y": 2, "Z": 4, "Base_Stress": 8},
        {"Name": "Chajja", "Type": "Concrete", "X": 5, "Y": 0, "Z": 6, "Base_Stress": 5},
        {"Name": "Roof Beam", "Type": "RCC", "X": 5, "Y": 5, "Z": 8, "Base_Stress": 14},
        {"Name": "Slab", "Type": "RCC", "X": 5, "Y": 5, "Z": 9, "Base_Stress": 11},
    ]
    df = pd.DataFrame(components_data)

    # Calculate live stress based on slider values
    df["Current_Stress_MPa"] = df["Base_Stress"] + (wind * 0.1) + (seismic**2 * 1.5) + (abs(temp - 25) * 0.2)

    if self_healing:
        df["Current_Stress_MPa"] = df["Current_Stress_MPa"] * 0.65

    def get_color(stress):
        if stress < 25: return "green"
        elif stress < 45: return "orange"
        else: return "red"

    df["Status_Color"] = df["Current_Stress_MPa"].apply(get_color)
    return df

def create_3d_plot(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=df["X"], y=df["Y"], z=df["Z"],
        mode='markers+text',
        marker=dict(size=14, color=df["Status_Color"], opacity=0.9),
        text=df["Name"],
        textposition="top center"
    ))
    fig.update_layout(
        template="plotly_dark",
        height=500,
        scene=dict(xaxis_title="Width", yaxis_title="Depth", zaxis_title="Height"),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

# ---------------------------------------------------------
# 4. Dashboard Layout
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📸 AI Image Analysis & 3D Twin", "📊 Live Data Table"])

with tab1:
    st.subheader("Upload Photo to Generate Digital Twin")
    
    uploaded_files = st.file_uploader(
        "Upload real building photos (JPG/PNG)", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # Simulate the AI processing time
        with st.spinner('🤖 AI Vision analyzing structural components... Please wait.'):
            time.sleep(2) # Fake delay to simulate computer vision analysis
        
        st.success("✅ Analysis Complete: Extracted columns, beams, and chajjas.")
        
        # Side-by-side layout: Image on left, 3D Plot on right
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Analyzed Building Photo**")
            image = Image.open(uploaded_files[0]) # Display the first uploaded image
            st.image(image, use_container_width=True)
            
        with col2:
            st.markdown("**Generated 3D Sensor Mapping**")
            df = generate_sensor_dataframe()
            fig = create_3d_plot(df)
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.info("💡 Waiting for upload. Upload a photo to trigger the AI structural extraction.")

with tab2:
    st.subheader("Component Health Breakdown")
    if uploaded_files:
        df = generate_sensor_dataframe()
        st.dataframe(df[["Name", "Type", "Current_Stress_MPa"]], use_container_width=True)
    else:
        st.warning("Upload a photo in the first tab to generate data.")