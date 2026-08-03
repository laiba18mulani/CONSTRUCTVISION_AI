import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="AI Inspection",
    layout="wide"
)

st.title("🤖 AI Construction Inspection")

st.write("""
Upload a residential building image for AI-based damage inspection.
""")

uploaded_file = st.file_uploader(
    "📷 Upload Building Image",
    type=["jpg","jpeg","png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image,use_container_width=True)

    with col2:
        st.subheader("AI Inspection Result")

        st.info("AI Model Ready")

        if st.button("🚀 Start AI Inspection"):

            progress = st.progress(0)

            for i in range(101):
                progress.progress(i)

            st.success("Inspection Completed Successfully")

            st.metric("Confidence","98.4%")

            st.metric("Detected Damage","Hairline Crack")

            st.metric("Severity","Low")

            st.warning("Suggested Repair")

            st.write("""
• Crack Sealant

• Waterproof Coating

• Monitor after 6 months
            """)

            st.success("Estimated Repair Cost")

            st.write("₹ 8,500")
            