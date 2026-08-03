import streamlit as st

# -------------------- HERO SECTION --------------------

# st.image("assets/images/hero_building.jpg", use_container_width=True)

st.markdown("""
# 🏗️ CONSTRUCTVISION AI

### AI Powered Residential Construction Inspection Platform

Welcome to the next generation of residential building inspection.
""")

st.success("Welcome to CONSTRUCTVISION AI")

# -------------------- BUTTONS --------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("🏠 Start Project")

with col2:
    st.button("🏗️ Explore Building")

with col3:
    st.button("📚 Material Library")

with col4:
    st.button("🤖 AI Inspection")

st.markdown("---")

# -------------------- FEATURES --------------------

st.header("✨ Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
- 🏗️ 3D Building Explorer
- 📚 Material Library
- 🎮 Virtual Practical
- 🤖 AI Inspection
""")

with col2:
    st.markdown("""
- 📊 Damage Analysis
- 💰 Cost Estimation
- 📄 PDF Reports
- 📡 IoT Monitoring
""")
    