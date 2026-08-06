import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Material Library", layout="wide")

st.title("🧱 Construction Material Library")
st.markdown("Explore commonly used construction materials with detailed engineering information.")

BASE_PATH = Path("assets/materials/images")

materials = [
    "cement",
    "sand",
    "steel",
    "brick",
    "concrete",
    "paint",
    "tiles"
]

cols = st.columns(3)

for i, material in enumerate(materials):

    folder = BASE_PATH / material
    image = folder / f"{material}.jpg"
    info = folder / "info.txt"

    with cols[i % 3]:

        st.subheader(material.capitalize())

        if image.exists():
            st.image(str(image), use_container_width=True)
        else:
            st.warning("Image not found")

        if info.exists():
            with open(info, "r", encoding="utf-8") as f:
                text = f.read()

            with st.expander("📖 View Details"):
                st.text(text)

        else:
            st.error("info.txt not found")
            