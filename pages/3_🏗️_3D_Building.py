import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(layout="wide")

st.title("🏗️ 3D Residential Building")
st.write("Rotate, zoom and explore the house.")

model_path = Path("assets/models3d/house.glb").resolve().as_uri()

html = f"""
<!DOCTYPE html>
<html>
<head>
<script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
<style>
body {{
    margin:0;
    background:white;
}}
model-viewer {{
    width:100%;
    height:700px;
}}
</style>
</head>
<body>

<model-viewer
src="{model_path}"
camera-controls
auto-rotate
shadow-intensity="1">
</model-viewer>

</body>
</html>
"""

components.html(html, height=720)


