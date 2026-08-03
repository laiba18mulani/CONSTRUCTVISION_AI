import streamlit as st

st.title("📖 Tutorial")

st.header("How to Use CONSTRUCTVISION AI")

steps = [
    "Create New Project",
    "Explore 3D Building",
    "Learn Construction Materials",
    "Perform Virtual Practical",
    "Upload Building Images",
    "Run AI Inspection",
    "View Damage Analysis",
    "Estimate Repair Cost",
    "Generate PDF Report"
]

for i, step in enumerate(steps, start=1):
    st.write(f"{i}. {step}")
    