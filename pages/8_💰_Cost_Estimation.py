import streamlit as st

st.set_page_config(page_title="Cost Estimation", layout="wide")

st.title("💰 AI Repair Cost Estimation")

st.markdown("Estimate repair cost based on the detected damage.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    damage = st.selectbox(
        "Damage Type",
        [
            "Hairline Crack",
            "Deep Crack",
            "Corrosion",
            "Spalling",
            "Leakage"
        ]
    )

    area = st.number_input(
        "Damage Area (sq.ft)",
        min_value=1.0,
        value=10.0
    )

with col2:

    labour = st.number_input(
        "Labour Cost (₹)",
        min_value=500,
        value=5000
    )

    misc = st.number_input(
        "Miscellaneous Cost (₹)",
        min_value=0,
        value=2000
    )

material_cost = {
    "Hairline Crack":300,
    "Deep Crack":900,
    "Corrosion":1200,
    "Spalling":1500,
    "Leakage":600
}

repair_material = {
    "Hairline Crack":"Crack Sealant",
    "Deep Crack":"Epoxy Injection",
    "Corrosion":"Anti Corrosion Coating",
    "Spalling":"Polymer Repair Mortar",
    "Leakage":"Waterproof Coating"
}

cost = area * material_cost[damage]

total = cost + labour + misc

st.markdown("---")

st.subheader("📊 Estimation Result")

st.metric(
    "Material",
    repair_material[damage]
)

st.metric(
    "Material Cost",
    f"₹ {cost:,.0f}"
)

st.metric(
    "Labour",
    f"₹ {labour:,.0f}"
)

st.metric(
    "Miscellaneous",
    f"₹ {misc:,.0f}"
)

st.metric(
    "Total Cost",
    f"₹ {total:,.0f}"
)

st.success("AI Cost Estimation Completed")
