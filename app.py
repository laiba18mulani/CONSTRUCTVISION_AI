import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="CONSTRUCTVISION AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CSS ------------------

st.markdown("""
<style>

.main{
    background-color:#F5F7FA;
}

.big-title{
    font-size:48px;
    font-weight:bold;
    color:#1E3A8A;
}

.subtitle{
    font-size:22px;
    color:gray;
}

.card{
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0px 4px 18px rgba(0,0,0,0.08);
    text-align:center;
}

.card h3{
    color:#1E3A8A;
}

div.stButton>button{
    width:100%;
    border-radius:12px;
    height:55px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------

with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942925.png", width=120)

    selected = option_menu(
        "CONSTRUCTVISION AI",
        [
            "Home",
            "Tutorial",
            "3D Building",
            "Materials",
            "Virtual Practical",
            "AI Inspection",
            "Damage Analysis",
            "Cost Estimation",
            "Reports",
            "History",
            "Settings"
        ],
        icons=[
            "house",
            "book",
            "building",
            "bricks",
            "play-circle",
            "robot",
            "bar-chart",
            "currency-rupee",
            "file-earmark",
            "clock-history",
            "gear"
        ],
        default_index=0,
    )

# ---------------- HOME ----------------

if selected=="Home":

    st.markdown(
        "<div class='big-title'>🏗️ CONSTRUCTVISION AI</div>",
        unsafe_allow_html=True)

    st.markdown(
        "<div class='subtitle'>AI Powered Residential Construction Inspection Platform</div>",
        unsafe_allow_html=True)

    st.write("")

    st.success("Welcome to the Future of Smart Construction Inspection")

    st.write("")

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.metric("Projects","25","+5")

    with c2:
        st.metric("Inspections","132","+16")

    with c3:
        st.metric("AI Accuracy","98.7%")

    with c4:
        st.metric("Reports","210")

    st.write("")
    st.write("")

    col1,col2,col3=st.columns(3)

    with col1:

        st.markdown("""
        <div class="card">
        <h3>🏠 Residential Building</h3>
        Explore realistic 3D residential buildings.
        </div>
        """,unsafe_allow_html=True)

        st.button("Open Building Explorer")

    with col2:

        st.markdown("""
        <div class="card">
        <h3>🤖 AI Inspection</h3>
        Upload construction images for AI damage detection.
        </div>
        """,unsafe_allow_html=True)

        st.button("Start AI Inspection")

    with col3:

        st.markdown("""
        <div class="card">
        <h3>📚 Material Library</h3>
        Learn all materials used in residential construction.
        </div>
        """,unsafe_allow_html=True)

        st.button("Open Material Library")

    st.write("")
    st.write("")

    st.header("Project Modules")

    m1,m2,m3,m4=st.columns(4)

    m1.info("🏗️ 3D Building")
    m2.info("📷 AI Detection")
    m3.info("💰 Cost Estimation")
    m4.info("📄 PDF Reports")

else:

    st.title(selected)
    st.info(f"{selected} module is under development.")
    
