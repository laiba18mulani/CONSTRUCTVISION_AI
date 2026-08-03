import streamlit as st
import pandas as pd

st.set_page_config(page_title="Damage Analysis", layout="wide")

st.title("📊 Damage Analysis Dashboard")

st.write("AI Inspection Summary")

damage_data = pd.DataFrame({
    "Damage Type":[
        "Hairline Crack",
        "Corrosion",
        "Leakage",
        "Spalling",
        "Honeycombing"
    ],

    "Severity":[
        "Low",
        "Medium",
        "High",
        "Medium",
        "Low"
    ],

    "Confidence (%)":[
        98,
        94,
        91,
        89,
        86
    ],

    "Repair Material":[
        "Crack Sealant",
        "Anti-Corrosion Coating",
        "Waterproof Coating",
        "Repair Mortar",
        "Grout"
    ],

    "Estimated Cost (₹)":[
        8500,
        25000,
        12000,
        18000,
        6000
    ]
})

st.dataframe(
    damage_data,
    use_container_width=True
)

st.markdown("---")

col1,col2,col3=st.columns(3)

with col1:

    st.metric(
        "Total Damages",
        "5"
    )

with col2:

    st.metric(
        "Average Confidence",
        "91.6%"
    )

with col3:

    st.metric(
        "Estimated Repair",
        "₹69,500"
    )

st.markdown("---")

st.subheader("Repair Recommendation")

damage = st.selectbox(
    "Select Damage",
    damage_data["Damage Type"]
)

row = damage_data[
    damage_data["Damage Type"]==damage
].iloc[0]

st.success(f"Recommended Material : {row['Repair Material']}")

st.info(f"Estimated Cost : ₹{row['Estimated Cost (₹)']}")

st.warning(f"Severity : {row['Severity']}")

st.write(f"AI Confidence : {row['Confidence (%)']}%")
