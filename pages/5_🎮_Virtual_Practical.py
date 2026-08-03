import streamlit as st

st.set_page_config(page_title="Virtual Practical", layout="wide")

st.title("🎮 Virtual Construction Practical")

st.write(
    "Learn the complete residential building construction process step by step."
)

steps = {
    "1️⃣ Site Preparation": {
        "Description": "Cleaning the site, marking layout and preparing land.",
        "Materials": "Survey Equipment, Marking Chalk",
        "Machines": "Excavator, Total Station",
        "Safety": "Wear helmet and safety shoes."
    },

    "2️⃣ Excavation": {
        "Description": "Digging foundation trenches.",
        "Materials": "Earthwork",
        "Machines": "JCB, Excavator",
        "Safety": "Support trench walls."
    },

    "3️⃣ Foundation": {
        "Description": "Constructing RCC footing.",
        "Materials": "Concrete M20, Steel Fe500",
        "Machines": "Concrete Mixer",
        "Safety": "Check reinforcement before concreting."
    },

    "4️⃣ Columns": {
        "Description": "Casting RCC columns.",
        "Materials": "Steel, Concrete",
        "Machines": "Concrete Vibrator",
        "Safety": "Proper shuttering."
    },

    "5️⃣ Beams": {
        "Description": "Constructing RCC beams.",
        "Materials": "Concrete, Steel",
        "Machines": "Concrete Mixer",
        "Safety": "Check beam reinforcement."
    },

    "6️⃣ Slab": {
        "Description": "Roof slab concreting.",
        "Materials": "Concrete M25",
        "Machines": "Concrete Pump",
        "Safety": "Proper curing after casting."
    },

    "7️⃣ Brick Work": {
        "Description": "Wall construction.",
        "Materials": "Bricks, Cement Mortar",
        "Machines": "Brick Cutter",
        "Safety": "Maintain alignment."
    },

    "8️⃣ Plaster": {
        "Description": "Internal and external plaster.",
        "Materials": "Cement Mortar",
        "Machines": "Hand Tools",
        "Safety": "Use protective gloves."
    },

    "9️⃣ Flooring": {
        "Description": "Tile laying.",
        "Materials": "Tiles, Adhesive",
        "Machines": "Tile Cutter",
        "Safety": "Keep floor level."
    },

    "🔟 Painting": {
        "Description": "Final painting work.",
        "Materials": "Primer, Paint",
        "Machines": "Roller, Spray Gun",
        "Safety": "Wear mask while painting."
    }
}

selected = st.selectbox(
    "Select Construction Stage",
    list(steps.keys())
)

data = steps[selected]

st.markdown("---")

st.subheader(selected)

st.info(data["Description"])

col1, col2 = st.columns(2)

with col1:
    st.success("🧱 Materials")
    st.write(data["Materials"])

    st.warning("⚠ Safety")
    st.write(data["Safety"])

with col2:
    st.success("🚜 Equipment")
    st.write(data["Machines"])

st.markdown("---")

st.button("▶ Next Step")
